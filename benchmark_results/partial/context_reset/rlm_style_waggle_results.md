# Waggle RLM-style Benchmark Results

> **Warning:** This benchmark follows the benchmark families used in the RLM paper,
> but uses deterministic synthetic memory tasks mapped to Waggle's graph/transcript
> environment. It should **not** be compared numerically to the RLM paper until the
> exact public datasets and matching model setup are run.

| Benchmark family | Scale | Method | Score | F1 | Ev. Coverage | Tokens returned | Latency (ms) |
|---|---:|---|---:|---:|---:|---:|---:|
| ContextReset | 128 | raw_context | 0.875 | 1.000 | 1.000 | 1994 | 2 |
| ContextReset | 128 | query_graph | 0.000 | 0.000 | 0.000 | 76 | 5 |
| ContextReset | 128 | build_context | 0.000 | 0.000 | 0.000 | 121 | 28 |
| ContextReset | 128 | bm25_topk | 0.875 | 1.000 | 1.000 | 1994 | 2 |
| ContextReset | 128 | hybrid_rrf | 0.875 | 1.000 | 1.000 | 1994 | 3 |

## Token efficiency: build_context vs baselines

| Benchmark family | Scale | Method | Tokens returned | Score |
|---|---:|---|---:|---:|
| ContextReset | 128 | query_graph | 76 | 0.000 |
| ContextReset | 128 | build_context | 121 | 0.000 |
| ContextReset | 128 | raw_context | 1994 | 0.875 |
| ContextReset | 128 | bm25_topk | 1994 | 0.875 |
| ContextReset | 128 | hybrid_rrf | 1994 | 0.875 |
