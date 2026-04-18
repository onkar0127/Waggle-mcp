# README Claim Verification Snapshot — 2026-04-18

This folder captures the exact local runs used to verify the benchmark claims currently summarized in the project README.

Verification target:
- comparative graph eval
- query-stress retrieval numbers
- benchmark harness test coverage for the reporting path

Repository state:
- Commit: `b251e5f6ae71f2fc2b9d36382bad465157b8d5eb`

Commands run:

```bash
.venv/bin/pytest tests/test_benchmark_harness.py -q
.venv/bin/python scripts/benchmark_extraction.py --systems waggle rag_naive rag_tuned --output tests/artifacts/verification/2026-04-18-readme-claims/benchmark_snapshot.json
```

Captured outputs:
- [pytest_test_benchmark_harness.txt](/Users/abhigyanshekhar/Desktop/MCP/tests/artifacts/verification/2026-04-18-readme-claims/pytest_test_benchmark_harness.txt)
- [benchmark_harness_stdout.txt](/Users/abhigyanshekhar/Desktop/MCP/tests/artifacts/verification/2026-04-18-readme-claims/benchmark_harness_stdout.txt)
- [benchmark_snapshot.json](/Users/abhigyanshekhar/Desktop/MCP/tests/artifacts/verification/2026-04-18-readme-claims/benchmark_snapshot.json)
- [benchmark_snapshot.md](/Users/abhigyanshekhar/Desktop/MCP/tests/artifacts/verification/2026-04-18-readme-claims/benchmark_snapshot.md)

Key verified results from `benchmark_snapshot.json`:
- Waggle comparative graph eval: `88% Hit@k`, `79% exact support`, `56.3` mean tokens
- Waggle flat slice: `85% Hit@k`, `85% exact support`
- Waggle graph slice: `93% Hit@k`, `70% exact support`
- Query stress `graph_raw`: `98% Hit@k`, `98% exact support`
- Query stress `graph_hybrid`: `98% Hit@k`, `98% exact support`

Use this folder when you want an auditable snapshot tied to a specific run, not just the rolling `tests/artifacts/benchmark_current.*` files.
