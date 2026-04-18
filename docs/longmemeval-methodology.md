# LongMemEval Methodology

This note explains what Waggle's LongMemEval numbers mean, how the adapter is implemented, and how to reproduce the saved artifacts honestly.

## Scope

Waggle currently treats LongMemEval as an external retrieval benchmark, not as a full graph-construction benchmark.

The adapter evaluates session retrieval against the cleaned `s` split:
- dataset: `benchmarks/longmemeval/longmemeval_s_cleaned.json`
- size: `500` questions
- output metrics: `R@5` and `Exact@5`

Those metrics answer a narrow question: can Waggle recover the correct support sessions from a haystack of prior sessions?

## Modes

Two exploratory retrieval modes are implemented in [src/waggle/longmemeval_benchmark.py](../src/waggle/longmemeval_benchmark.py).

`graph_raw`
- includes only user turns when preparing each session
- ranks sessions by a weighted score:
  semantic similarity `0.72`
  lexical overlap `0.18`
  temporal bias `0.10`
- returns the top 5 ranked sessions directly
- this is the fairest current baseline against raw retrieval systems because it does not add a second reranking stage

`graph_hybrid`
- includes user and assistant turns when preparing each session
- first computes the same raw ranking
- then reranks the top 20 sessions with a heuristic that mixes:
  reciprocal base rank
  lexical overlap
  temporal recency bias for `latest` and `oldest` questions
- returns the reranked top 5

The practical tradeoff is visible in the saved results:
- `graph_raw` has higher recall
- `graph_hybrid` has lower recall but higher exact support

## Data Preparation

For each dataset entry, the adapter:
1. normalizes the question and ground-truth session ids
2. converts each haystack session into a single text block
3. normalizes dates into UTC ISO timestamps
4. embeds unique session texts once and reuses them across entries

Important details:
- empty sessions are skipped
- repeated session texts across entries are embedded once, then reused
- timestamps are only used as a lightweight recency feature, not as a hard filter

## Caching

The adapter now writes a prepared-session cache keyed by:
- dataset SHA-256
- mode
- limit
- embedding model name and version

The cache payload stores:
- prepared entries
- question embeddings

That means cold vs warm runs differ in setup cost, not in scoring logic.

Cold run:
- reads the dataset
- prepares all entries
- embeds every unique session text
- embeds every question
- writes a pickle cache under `benchmarks/longmemeval/.cache/` by default

Warm run:
- loads the prepared entries and question embeddings from the cache
- skips the expensive preparation and embedding step
- runs the same ranking logic over the cached representation

Current reports include:
- `cache_status`
- `cache_path`
- `cache_key`
- `prepared_entry_count`
- `prepared_session_count`

## Reproduction

Raw retrieval baseline:

```bash
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_raw \
  --output benchmarks/longmemeval/results_graph_raw.json
```

Hybrid reranked baseline:

```bash
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_hybrid \
  --output benchmarks/longmemeval/results_graph_hybrid.json
```

To place caches elsewhere:

```bash
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_hybrid \
  --cache-dir /tmp/longmemeval-cache \
  --output /tmp/results_graph_hybrid.json
```

If you want to measure warm-cache behavior, rerun the same command without changing:
- dataset
- mode
- limit
- embedding model
- cache directory

## Interpretation

What this benchmark does validate:
- Waggle can retrieve the right support session from long multi-session haystacks
- lexical and temporal signals improve exact-support quality in some cases
- the prepared-session cache makes repeated evaluation practical

What it does not yet validate:
- end-to-end graph extraction quality on LongMemEval
- contradiction handling
- cross-session reasoning over typed nodes and edges
- context-bundle usefulness for model handoff

LongMemEval should therefore be treated as an external retrieval benchmark that complements, not replaces, Waggle's checked-in graph-memory fixture corpus.

## Current Saved Artifacts

- [benchmarks/longmemeval/results_graph_raw.json](../benchmarks/longmemeval/results_graph_raw.json)
- [benchmarks/longmemeval/results_graph_hybrid.json](../benchmarks/longmemeval/results_graph_hybrid.json)
- [benchmarks/longmemeval/README.md](../benchmarks/longmemeval/README.md)
