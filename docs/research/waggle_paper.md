# Waggle: Graph-Backed Persistent Memory for AI Agents with Recursive Context Assembly

**Abstract**

Large language model (LLM) agents lose all conversational context when the context window closes. Existing approaches — raw context dumps, flat note storage, and chunked retrieval-augmented generation (RAG) — either exhaust the context budget at scale, discard relational structure, or fail to surface contradictions and superseded decisions. We present **Waggle**, a local-first persistent memory system built on a typed knowledge graph, and **Recursive Memory Context Assembly (RMCA)**, an algorithm for assembling compact, high-signal context packs from that graph in response to agent queries. RMCA decomposes queries into targeted subqueries, retrieves from multiple evidence lanes, expands the graph along typed edges, resolves update chains and contradictions, and compresses the result to a configurable token budget. We evaluate Waggle on the LongMemEval-S benchmark (500 questions, multi-session retrieval) and on a suite of five synthetic task families adapted from the RLM benchmark taxonomy. On LongMemEval-S, `graph_raw` mode achieves **89.0% Exact@5** and **97.4% R@5** using `all-MiniLM-L6-v2` embeddings, with a held-out test split confirming no overfitting (+1.1pp gap). On pairwise conflict reasoning and codebase understanding tasks, RMCA (`build_context`) achieves perfect scores at all scales (128–2048 nodes) while raw context dump and single-query retrieval both score 0.0. On linear aggregation tasks, RMCA degrades gracefully, exposing a fundamental O(n) coverage limit shared by all fixed-budget retrieval systems. All code, benchmarks, and artifacts are open source.

---

## 1. Introduction

AI coding assistants and conversational agents are stateless by design: each session begins with an empty context window. Practitioners work around this by pasting prior conversation summaries, maintaining hand-curated notes, or relying on the model to infer context from the current session alone. None of these approaches scale.

The core problem has three dimensions:

1. **Volume.** A long-running project accumulates thousands of decisions, constraints, and implementation facts. No context window can hold them all.
2. **Structure.** Decisions depend on constraints; constraints contradict earlier preferences; implementations derive from decisions. Flat text storage discards this relational structure.
3. **Staleness.** Decisions get reversed. Constraints get relaxed. A memory system that cannot distinguish current from superseded information will mislead the agent.

Retrieval-augmented generation (RAG) addresses volume but not structure or staleness. GraphRAG-style systems [CITATION] add community-detection graphs over document chunks but operate on pre-computed summaries and do not model temporal validity or contradiction. Episodic memory systems [CITATION] store conversation turns but do not extract typed relational structure.

We make the following contributions:

- **Waggle**, a local-first persistent memory system built on a typed knowledge graph with temporal validity, contradiction handling, and a git-inspired snapshot vocabulary.
- **RMCA (Recursive Memory Context Assembly)**, an algorithm that assembles compact context packs from the graph via query decomposition, multi-lane retrieval, typed-edge expansion, conflict resolution, and token-budget compression.
- **Empirical evaluation** on LongMemEval-S (500 questions) and five synthetic task families, with held-out splits and explicit overfitting checks.
- **Open-source implementation** as an MCP-compatible server (`waggle-mcp`) deployable with a single `pipx install`.

---

## 2. Background and Related Work

### 2.1 Context Window Limitations

Transformer-based LLMs have fixed context windows. While window sizes have grown (4K → 128K → 1M tokens), the fundamental problem remains: information outside the window is inaccessible, and filling the window with raw history is expensive and degrades attention quality at long ranges [CITATION].

### 2.2 Retrieval-Augmented Generation

RAG [CITATION] retrieves relevant text chunks by semantic similarity and injects them into the prompt. It addresses volume but has three structural weaknesses relevant to agent memory:

- **Flat ranking.** A single similarity query cannot distinguish a current decision from a superseded one.
- **No relational structure.** Chunks are independent; the dependency between a decision and its rationale is not represented.
- **No conflict detection.** Two contradictory chunks are returned with equal weight.

### 2.3 GraphRAG and Knowledge Graph Retrieval

Microsoft GraphRAG [CITATION] builds a community-detection graph over document chunks and retrieves community summaries. This improves coverage for broad queries but pre-computes summaries offline and does not model temporal validity or agent-specific relational types (decisions, constraints, contradictions).

### 2.4 Episodic and Working Memory for Agents

MemGPT [CITATION] introduces a tiered memory architecture with explicit paging between in-context and external storage. Generative Agents [CITATION] use a memory stream with recency, importance, and relevance scoring. These systems focus on retrieval of episodic facts; they do not model typed relational edges or contradiction resolution as first-class operations.

### 2.5 Recursive Language Models

The RLM framework [Zhang et al., 2026] proposes externalising long context into an environment and interacting with it through decomposition and targeted retrieval. Waggle's RMCA algorithm is directly inspired by this decomposition-retrieval loop, applied to a persistent typed graph rather than a document corpus.

---

## 3. System Design

### 3.1 Memory Graph

Waggle stores memory in a persistent typed knowledge graph `G = (V, E)`.

**Node types:** `fact`, `entity`, `concept`, `preference`, `decision`, `question`, `note`

**Edge types:** `relates_to`, `contradicts`, `depends_on`, `part_of`, `updates`, `derived_from`, `similar_to`

Every node carries temporal validity fields `valid_from` and `valid_to`. Nodes whose `valid_to` has passed are excluded from default queries. The `resolve_conflict` operation accepts a `winner` node ID and sets the losing node's `valid_to` to the current time, making supersession explicit and reversible.

The graph is backed by SQLite with WAL mode for local-first deployments, with an optional Neo4j backend for remote or multi-client deployments.

### 3.2 Embeddings

Waggle uses `sentence-transformers` for local embedding with no external API dependency. The default model is `all-MiniLM-L6-v2` (~420 MB, 384-dimensional embeddings). A deterministic SHA-256 fallback is available for offline or resource-constrained environments.

### 3.3 Retrieval Modes

Three retrieval lanes are available:

- **`graph`**: semantic similarity over node embeddings, with typed-edge expansion.
- **`hybrid`**: graph retrieval fused with BM25 lexical scoring.
- **`verbatim`**: semantic search over the raw conversation transcript store.

### 3.4 MCP Tool Surface

Waggle exposes its functionality as an MCP (Model Context Protocol) server. The six core tools used in normal agent operation are:

| Tool | Purpose |
|---|---|
| `observe_conversation` | Ingest a conversation turn; extract nodes and edges automatically |
| `query_graph` | Retrieve a subgraph for a query |
| `prime_context` | Hydrate context at session start |
| `build_context` | Run RMCA for a full recursive context pack |
| `graph_diff` | Show what changed recently |
| `store_node` / `store_edge` | Structured atomic writes |

---

## 4. Recursive Memory Context Assembly (RMCA)

RMCA is the algorithm behind `build_context`. It takes a query `q`, the memory graph `G`, the transcript store `T`, a token budget `B`, expansion depth `d`, and maximum subquery count `k`, and returns a structured context pack `C` with `estimated_tokens(C) ≤ B × 1.15`.

### 4.1 Algorithm

**Step 1 — Decompose.** The query is classified as project/coding or generic. A set of up to `k` targeted subqueries is generated, each with a priority weight and a set of retrieval modes. For project queries, subqueries target: recent decisions, unfinished tasks, constraints and rejected directions, implementation details, conflicts, and the original query. For generic queries, subqueries target: the original query, recent relevant facts, related decisions, contradictions, and transcript evidence.

**Step 2 — Retrieve.** Each subquery is issued against the graph and transcript store using its assigned retrieval modes. Results are accumulated into a working hit set `H`.

**Step 3 — Expand.** The top-5 nodes in `H` by score are used as seeds. For each of the top-3 seeds, 1–2 hop graph expansion is performed along typed edges (`updates`, `contradicts`, `depends_on`, `derived_from`, `part_of`). Expansion along `relates_to` and `similar_to` is excluded to avoid token budget inflation.

**Step 4 — Resolve.** All edges in `H` are inspected. Nodes connected by `updates` edges have their scores penalised (×0.3) and the updating node is boosted (+0.15). Nodes connected by `contradicts` edges are recorded as conflict pairs. Nodes with expired `valid_to` are penalised (×0.2).

**Step 5 — Deduplicate.** For each unique `node_id`, only the highest-scored copy is retained.

**Step 6 — Rank.** Nodes are sorted by: superseded status (non-superseded first), score (descending), label (ascending for ties).

**Step 7 — Compress.** Nodes are packed into the context string `C` in priority order: decisions, constraints, implementation, unfinished, conflicts, superseded, evidence. Packing stops when the token budget `B × 1.15` is reached.

**Step 8 — Format.** A structured header is prepended. Provenance and conflict annotations are attached.

### 4.2 Comparison with Top-k RAG

| Dimension | Top-k RAG | RMCA |
|---|---|---|
| Query strategy | Single embedding query | Decomposed into up to k targeted subqueries |
| Index structure | Flat chunk index | Typed knowledge graph |
| Graph expansion | None | 1–2 hop traversal along typed edges |
| Conflict handling | None | Explicit `contradicts` / `updates` detection and annotation |
| Staleness handling | None | Temporal validity (`valid_to`) with score penalisation |
| Token budget | Fixed top-k | Configurable budget with priority-ordered packing |
| Evidence provenance | Chunk source | Verbatim transcript lane + node provenance |

### 4.3 Comparison with GraphRAG

| Dimension | GraphRAG | RMCA |
|---|---|---|
| Graph construction | Community detection over document chunks | Typed relational graph from conversation turns |
| Query strategy | Single query against pre-computed summaries | Runtime decomposition into targeted subqueries |
| Token budget | Fixed community summary size | Configurable budget with priority ordering |
| Verbatim evidence | Not available | Verbatim transcript retrieval lane |
| Temporal validity | Not modelled | First-class `valid_from` / `valid_to` on every node |

---

## 5. Evaluation

### 5.1 LongMemEval-S

**Dataset.** LongMemEval-S [CITATION] is a 500-question benchmark for multi-session conversational memory retrieval. Each question requires identifying the correct support session(s) from a haystack of prior sessions. The cleaned `s` split (`xiaowu0162/longmemeval-cleaned`) contains 500 questions with gold support sets of cardinality 1–6.

**Metrics.** We report R@5 (recall: does the gold set appear anywhere in the top 5?), Exact@5 (precision: does the top 5 exactly match the gold set?), Exact@10, and Exact@20.

**Setup.** Sessions are prepared by converting each haystack session to a text block, normalising timestamps to UTC ISO format, and embedding unique session texts once with `all-MiniLM-L6-v2`. A prepared-session cache keyed by dataset SHA-256, mode, limit, and embedding model is written on the first run and reused on subsequent runs. All reported numbers use the warm cache.

**Modes.** Two retrieval modes are evaluated:

- `graph_raw`: user turns only; weighted score = 0.72 × semantic + 0.18 × lexical + 0.10 × temporal; top-5 returned directly.
- `graph_hybrid`: user and assistant turns; same raw ranking followed by heuristic reranking of top-20 using RRF fusion, lexical overlap, and temporal recency bias.

**Results.**

| Mode | R@5 | Exact@5 | Exact@10 | Exact@20 |
|---|---|---|---|---|
| `graph_raw` | **97.4%** | **89.0%** | 89.0% | 89.0% |
| `graph_hybrid` | 97.0% | 87.2% | 94.8% | **98.0%** |

`graph_raw` achieves 89.0% Exact@5 with no tunable reranking heuristics, making it the most reproducible baseline. `graph_hybrid` scores lower on Exact@5 but recovers strongly at higher cutoffs (Exact@20 = 98.0%), indicating it finds all correct sessions but does not always pack them into the top 5 slots for high-cardinality queries.

**Cardinality breakdown.**

| Cardinality | n | `graph_raw` R@5 | `graph_raw` Exact@5 |
|---|---|---|---|
| 1 | 176 | 95.5% | 95.5% |
| 2 | 250 | 98.0% | 93.2% |
| 3 | 41 | 100.0% | 73.2% |
| 4 | 19 | 100.0% | 47.4% |
| 5 | 11 | 100.0% | 45.5% |
| 6 | 3 | 100.0% | 0.0% |

The R@5 = 100% at cardinality ≥ 3 confirms the embedding reliably finds the correct base session. The Exact@5 drop at high cardinality is a packing problem: fitting 4–6 chunks into 5 slots while excluding noise is structurally harder than retrieval itself. Exact@10 and Exact@20 recovering to 89–98% confirms the model is finding all the chunks.

**Overfitting check.** To verify the scores are not artefacts of the specific 500-question distribution, we ran a held-out split (50 dev / 450 test, seed 42):

| Mode | Dev Exact@5 (n=50) | Test Exact@5 (n=450) | Gap |
|---|---|---|---|
| `graph_raw` | 88.0% | 89.1% | +1.1pp — stable |
| `graph_hybrid` | 92.0% | 86.7% | −5.3pp — dev-set sensitivity |

`graph_raw` generalises cleanly. The 5.3pp gap for `graph_hybrid` is expected: the heuristic reranking weights (RRF fusion, lexical/coverage scoring) are partially tuned to this distribution. `graph_hybrid` Exact@5 should be treated as an exploratory number rather than a headline result.

### 5.2 RLM-Style Synthetic Benchmark

To evaluate RMCA's behaviour across task types that vary in structural complexity, we constructed a synthetic benchmark suite following the task taxonomy of the RLM paper [Zhang et al., 2026]. Each family maps a canonical long-context task to a Waggle memory graph scenario.

**Task families.**

| Family | RLM equivalent | What it tests |
|---|---|---|
| S-NIAH-style | RULER S-NIAH | Retrieve one fact from N distractors — O(1) |
| BrowseComp-Plus-style | BrowseComp-Plus | Multi-hop QA across 3 linked nodes |
| OOLONG-style | OOLONG | Aggregate N entries — O(n) |
| OOLONG-Pairs-style | OOLONG-Pairs | Pairwise conflict reasoning — O(n²) |
| CodeQA-style | LongBench-v2 CodeQA | Codebase/repo understanding |

**Methods compared.**

- `raw_context`: dump all graph nodes into the context window (no retrieval).
- `query_graph`: single semantic query, top-k results returned.
- `build_context`: full RMCA pipeline.

**Scales.** Each family is evaluated at N = 128, 512, and 2048 nodes.

**Results.**

| Family | Scale | `raw_context` | `query_graph` | `build_context` |
|---|---:|---:|---:|---:|
| S-NIAH-style | 128 | 1.000 | 1.000 | **1.000** |
| S-NIAH-style | 512 | 1.000 | 1.000 | **1.000** |
| S-NIAH-style | 2048 | 1.000 | 1.000 | **1.000** |
| BrowseComp-Plus-style | 128 | 1.000 | 1.000 | **1.000** |
| BrowseComp-Plus-style | 512 | 1.000 | 1.000 | **1.000** |
| BrowseComp-Plus-style | 2048 | 1.000 | 1.000 | **1.000** |
| OOLONG-Pairs-style | 128 | 0.000 | 0.000 | **1.000** |
| OOLONG-Pairs-style | 512 | 0.000 | 0.000 | **1.000** |
| OOLONG-Pairs-style | 2048 | 0.000 | 0.000 | **1.000** |
| CodeQA-style | 128 | 0.000 | 1.000 | **1.000** |
| CodeQA-style | 512 | 0.000 | 1.000 | **1.000** |
| CodeQA-style | 2048 | 0.000 | 1.000 | **1.000** |
| OOLONG-style | 128 | 0.885 | 0.242 | 0.513 |
| OOLONG-style | 512 | 0.403 | 0.035 | 0.224 |
| OOLONG-style | 2048 | 0.000 | 0.010 | 0.069 |

**Token efficiency.**

| Family | Scale | `raw_context` tokens | `build_context` tokens | Ratio |
|---|---:|---:|---:|---:|
| S-NIAH-style | 128 | 1,423 | 181 | **7.9×** |
| S-NIAH-style | 2048 | 1,430 | 202 | **7.1×** |
| OOLONG-Pairs-style | 128 | 1,422 | 515 | **2.8×** |
| OOLONG-Pairs-style | 2048 | 1,407 | 541 | **2.6×** |
| CodeQA-style | 128 | 1,382 | 535 | **2.6×** |
| CodeQA-style | 2048 | 1,400 | 646 | **2.2×** |

**Key findings.**

1. **Pairwise conflict reasoning (OOLONG-Pairs).** Both `raw_context` and `query_graph` score 0.0 at all scales. `build_context` scores 1.0 at all scales. This is the clearest demonstration of RMCA's value: the conflict resolution step (Step 4) surfaces `contradicts` edges that neither a raw dump nor a single-query retrieval can identify.

2. **Codebase understanding (CodeQA).** `raw_context` scores 0.0 at all scales (the relevant code fact is buried in a large context dump). `query_graph` and `build_context` both score 1.0, confirming that targeted retrieval is sufficient for this task type.

3. **Simple factual retrieval (S-NIAH, BrowseComp-Plus).** All three methods score 1.0 at all scales. RMCA uses 7–8× fewer tokens than raw context while achieving the same score.

4. **Linear aggregation (OOLONG).** This is the hardest task family. `raw_context` scores highest at small scale (0.885 at N=128) but degrades to 0.0 at N=2048 as the context window fills. `build_context` scores 0.513 at N=128 and degrades to 0.069 at N=2048. This exposes a fundamental limitation: tasks requiring aggregation over all N entries cannot be fully satisfied by any fixed-budget retrieval system. RMCA degrades more gracefully than raw context at large scale but does not solve the O(n) coverage problem.

### 5.3 Latency

Local latency on SQLite with deterministic embeddings (warm cache):

| Operation | Mean latency |
|---|---|
| `observe_conversation` | 1.54 ms |
| `query_graph` | 1.60 ms |
| `graph_diff` | 0.80 ms |
| `build_context` (N=128) | ~22 ms |
| `build_context` (N=2048) | ~258–415 ms |

`build_context` latency scales with graph size due to the multi-subquery retrieval loop. At N=2048, latency is in the 250–415 ms range, which is acceptable for agent use but not for real-time interactive applications.

---

## 6. Discussion

### 6.1 When RMCA Helps

RMCA provides the largest benefit over raw context and single-query retrieval on tasks that require:

- **Conflict and contradiction detection.** The `contradicts` and `updates` edge resolution in Step 4 is the only mechanism that can surface "we reversed this decision" without the agent having to read the entire history.
- **Multi-aspect information needs.** Query decomposition (Step 1) allows RMCA to retrieve memory relevant to decisions, constraints, implementation details, and conflicts in a single call, where a single-query retrieval would only surface the most semantically similar nodes.
- **Token-constrained contexts.** At large graph sizes, raw context dumps exceed any practical context window. RMCA's token-budget compression (Step 7) ensures the context pack fits regardless of graph size.

### 6.2 When RMCA Does Not Help

RMCA does not improve over simpler methods on:

- **Simple factual retrieval.** When the answer is a single node with high semantic similarity to the query, `query_graph` is sufficient and faster.
- **Linear aggregation.** Tasks requiring enumeration of all N entries are fundamentally O(n) information needs. No fixed-budget retrieval system can guarantee full coverage. RMCA degrades more gracefully than raw context at large scale but does not solve this problem.

### 6.3 Limitations

1. **Synthetic benchmark caveat.** The RLM-style benchmark uses deterministic synthetic Waggle memory tasks. Numerical results must not be compared to the RLM paper [Zhang et al., 2026] or other long-context benchmarks until the exact public datasets are run with a matching model setup.

2. **Token estimation is approximate.** `estimated_tokens(text) = len(text) // 4` is a character-count heuristic. Actual token counts depend on the downstream model's tokenizer and may differ by ±20%.

3. **Decomposition is heuristic, not learned.** Subquery generation uses keyword pattern matching to detect query intent. It does not use an LLM and may produce suboptimal decompositions for queries outside the project/coding and generic-memory categories.

4. **Graph expansion is bounded.** Expansion is limited to 2 hops from the top-3 seed nodes. Deep reasoning chains requiring more than 2 hops are not guaranteed to be surfaced.

5. **LongMemEval scope.** The LongMemEval adapter evaluates session retrieval only — it does not evaluate end-to-end graph extraction quality, contradiction handling across sessions, or context-bundle usefulness for model handoff. These are complementary evaluation dimensions not yet measured.

6. **`graph_hybrid` reranking sensitivity.** The 5.3pp dev/test gap on LongMemEval confirms that the hybrid reranking weights are partially tuned to this distribution. `graph_hybrid` Exact@5 should not be treated as a portable headline number.

---

## 7. Conclusion

We presented Waggle, a local-first persistent memory system for AI agents, and RMCA, an algorithm for assembling compact, high-signal context packs from a typed knowledge graph. On LongMemEval-S, `graph_raw` achieves 89.0% Exact@5 with no overfitting confirmed by a held-out split. On pairwise conflict reasoning tasks, RMCA achieves perfect scores at all scales while raw context dump and single-query retrieval both fail completely. On linear aggregation tasks, RMCA degrades gracefully but exposes a fundamental O(n) coverage limit shared by all fixed-budget retrieval systems.

The key insight is that agent memory is not a retrieval problem alone — it is a retrieval-plus-reasoning problem. Retrieving the right facts is necessary but not sufficient; the memory system must also surface which facts are current, which are superseded, and which contradict each other. RMCA addresses this by treating conflict resolution and temporal validity as first-class operations in the context assembly pipeline, not as post-processing steps.

Future work includes: (1) replacing heuristic query decomposition with a learned decomposer; (2) evaluating on the full RLM public benchmark suite with a matching model setup; (3) measuring end-to-end graph extraction quality on LongMemEval; and (4) hardening the hybrid reranking weights against distribution shift.

---

## References

- Zhang et al. (2026). *Recursive Language Models*. arXiv:2512.24601.
- Edge et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research.
- Packer et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560.
- Park et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv:2304.03442.
- Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020.
- Wu et al. (2024). *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*. arXiv:2410.10813.
- Reimers & Gurevych (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. EMNLP 2019.

---

## Appendix A: Reproduction

### LongMemEval-S

```bash
# Full 500-question run — graph_raw (headline number)
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_raw \
  --output benchmarks/longmemeval/results_graph_raw_$(date +%Y-%m-%d).json

# Full 500-question run — graph_hybrid
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_hybrid \
  --output benchmarks/longmemeval/results_graph_hybrid_$(date +%Y-%m-%d).json

# Held-out split (overfitting check)
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_raw \
  --held-out \
  --output benchmarks/longmemeval/results_graph_raw_heldout_$(date +%Y-%m-%d).json
```

### RLM-Style Synthetic Benchmark

```bash
python benchmarks/rlm_style_waggle_eval.py \
  --db /tmp/waggle_rlm_eval \
  --scales 128 512 2048 \
  --methods raw_context query_graph build_context \
  --families sniah multihop pairwise codeqa linear_agg \
  --token-budget 1200 \
  --seed 42 \
  --output benchmark_results/
```

### Full Suite

```bash
python benchmarks/run_full_benchmark.py --output benchmark_results/
```

---

## Appendix B: RMCA Pseudocode

```
Input:  q, G=(V,E), T, B, d, k
Output: C  where estimated_tokens(C) ≤ B × 1.15

1. DECOMPOSE
   If query intent is project/coding:
     subqueries ← [
       ("recent decisions about {topic}",       priority=1.00, modes=[graph, hybrid]),
       ("current unfinished tasks for {topic}",  priority=0.95, modes=[graph, hybrid]),
       ("constraints and rejected directions",   priority=0.90, modes=[graph, hybrid]),
       ("recent implementation details",         priority=0.85, modes=[graph, hybrid]),
       ("conflicts or updates in direction",     priority=0.80, modes=[graph]),
       (q,                                       priority=0.75, modes=[hybrid, verbatim]),
     ][:k]
   Else:
     subqueries ← [
       (q,                                       priority=1.00, modes=[hybrid, verbatim]),
       ("recent relevant facts about {topic}",   priority=0.90, modes=[graph, hybrid]),
       ("decisions related to {topic}",          priority=0.85, modes=[graph]),
       ("contradictions or conflicts",           priority=0.75, modes=[graph]),
       ("transcript evidence for {topic}",       priority=0.65, modes=[verbatim]),
     ][:k]

2. RETRIEVE
   H ← []
   For each sq_i in subqueries:
     hits_i ← retrieve(sq_i.query, G, T, modes=sq_i.retrieval_modes,
                       max_nodes=12, depth=d)
     H ← H ∪ hits_i

3. EXPAND
   seeds ← top-5 nodes in H by score
   For each seed s in seeds[:3]:
     neighbours ← graph_hop(s, G, depth=min(d, 2))
     H ← H ∪ {n ∈ neighbours : n ∉ seeds}

4. RESOLVE
   For each edge e = (src, tgt, rel) in edges(H):
     If rel = "updates":
       score(tgt) ×= 0.3; score(src) = min(1.0, score(src) + 0.15)
     If rel = "contradicts":
       record conflict_entry(src, tgt)
   For each h ∈ H where h.valid_to < now:
     score(h) ×= 0.2

5. DEDUPLICATE
   H ← {argmax_{score} h : h.node_id}

6. RANK
   H ← sort H by (is_superseded ASC, score DESC, label ASC)

7. COMPRESS
   C ← ""; budget_used ← 0; max_tokens ← B × 1.15
   For section in [decisions, constraints, implementation, unfinished,
                   conflicts, superseded, evidence]:
     For each h in section:
       line ← format(h)
       If budget_used + estimated_tokens(line) > max_tokens: break
       C ← C + line; budget_used += estimated_tokens(line)

8. FORMAT
   C ← prepend "### Waggle Recursive Context Pack\nTask: {q}\n"
   Return C, provenance(H), conflict_entries
```
