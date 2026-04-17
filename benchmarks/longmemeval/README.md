# LongMemEval Baseline

This directory contains the downloaded `longmemeval_s_cleaned.json` split and Waggle's exploratory benchmark outputs.

## Dataset

- Source: `xiaowu0162/longmemeval-cleaned`
- File: `longmemeval_s_cleaned.json`
- Cases: `500`

## Reproduction

Run the raw retrieval-only baseline:

```bash
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_raw \
  --output benchmarks/longmemeval/results_graph_raw.json
```

Run the heuristic hybrid baseline:

```bash
.venv/bin/python scripts/benchmark_longmemeval.py \
  benchmarks/longmemeval/longmemeval_s_cleaned.json \
  --mode graph_hybrid \
  --output benchmarks/longmemeval/results_graph_hybrid.json
```

## Current measured result

Measured locally on the full `500`-question `s` split:

| Mode | R@5 | Exact@5 |
|------|-----|---------|
| `graph_raw` | `97.0%` | `76.4%` |

Raw output artifact:

- [`results_graph_raw.json`](./results_graph_raw.json)

## Notes

- This adapter preloads each LongMemEval entry into a temporary Waggle graph and evaluates retrieval against the known session IDs.
- `graph_raw` is the fairest current comparison to raw retrieval systems because it does not add reranking.
- The current `graph_hybrid` runner is significantly slower on the full 500-case split and should be treated as an exploratory mode rather than a fast CI benchmark.
