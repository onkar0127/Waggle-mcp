# RMCA Answer-Level Evaluation Results

> **DISCLAIMER:** Deterministic answer-level metrics are reproducible lower bounds. They are not equivalent to human preference ratings or LLM-judge quality assessments. Scores should be interpreted as retrieval-quality proxies, not end-to-end answer quality.

| Family | Scale | Method | Answerer | EM | F1 | Ev.Used | Contra.Corr | Hall.Rate | Tokens |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| pairwise | 128 | rmca_full | deterministic | 0.000 | 0.308 | 0.333 | 1.000 | 0.000 | 515 |
| pairwise | 128 | query_graph | deterministic | 0.000 | 0.125 | 0.000 | 0.000 | 0.000 | 98 |
| pairwise | 128 | bm25_topk | deterministic | 0.000 | 0.125 | 0.000 | 0.000 | 0.000 | 1422 |
| pairwise | 128 | raw_context | deterministic | 0.000 | 0.125 | 0.000 | 0.000 | 0.000 | 1422 |
| codeqa | 128 | rmca_full | deterministic | 1.000 | 0.600 | 1.000 | 1.000 | 0.000 | 535 |
| codeqa | 128 | query_graph | deterministic | 1.000 | 0.545 | 1.000 | 1.000 | 0.000 | 178 |
| codeqa | 128 | bm25_topk | deterministic | 1.000 | 0.545 | 1.000 | 1.000 | 0.000 | 1398 |
| codeqa | 128 | raw_context | deterministic | 0.000 | 0.000 | 0.500 | 1.000 | 0.000 | 1382 |
| context_reset | 128 | rmca_full | deterministic | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 121 |
| context_reset | 128 | query_graph | deterministic | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 76 |
| context_reset | 128 | bm25_topk | deterministic | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1413 |
| context_reset | 128 | raw_context | deterministic | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1413 |

