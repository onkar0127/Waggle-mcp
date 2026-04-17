from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from waggle.longmemeval_benchmark import evaluate_longmemeval


class FakeEmbeddingModel:
    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(8, dtype=np.float32)
        for token in text.lower().split():
            index = sum(ord(character) for character in token) % len(vector)
            vector[index] += 1.0
        norm = np.linalg.norm(vector)
        if norm == 0.0:
            return vector
        return vector / norm

    def to_bytes(self, embedding: np.ndarray) -> bytes:
        return embedding.astype(np.float32).tobytes()

    def from_bytes(self, data: bytes) -> np.ndarray:
        return np.frombuffer(data, dtype=np.float32)

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        if a_norm == 0.0 or b_norm == 0.0:
            return 0.0
        return float(np.dot(a, b) / (a_norm * b_norm))


def test_evaluate_longmemeval_graph_modes(tmp_path: Path) -> None:
    dataset = [
        {
            "id": "entry_1",
            "question": "what database are we using in production",
            "haystack_sessions": [
                [
                    {"role": "user", "content": "We are using SQLite locally."},
                    {"role": "assistant", "content": "SQLite sounds fine for local work."},
                ],
                [
                    {"role": "user", "content": "Production uses PostgreSQL for safer migrations."},
                    {"role": "assistant", "content": "PostgreSQL is the production choice."},
                ],
            ],
            "haystack_session_ids": ["sess_local", "sess_prod"],
            "haystack_dates": ["2024/01/05 (Fri) 09:00", "2024/02/10 (Sat) 09:00"],
            "correct_session_ids": ["sess_prod"],
        }
    ]
    dataset_path = tmp_path / "longmemeval.json"
    dataset_path.write_text(json.dumps(dataset), encoding="utf-8")

    raw_report = evaluate_longmemeval(dataset_path, embedding_model=FakeEmbeddingModel(), mode="graph_raw")
    hybrid_report = evaluate_longmemeval(dataset_path, embedding_model=FakeEmbeddingModel(), mode="graph_hybrid")

    assert raw_report.case_count == 1
    assert hybrid_report.case_count == 1
    assert raw_report.r_at_5 == 1.0
    assert hybrid_report.r_at_5 == 1.0
    assert raw_report.per_case[0].retrieved_session_ids
