from __future__ import annotations

from typing import Any

import numpy as np


class EmbeddingModel:
    """Lazy-loaded sentence-transformer wrapper."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model: Any | None = None

    @property
    def model(self) -> Any:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, text: str) -> np.ndarray:
        normalized = text.strip()
        if not normalized:
            raise ValueError("Cannot embed empty text.")
        return np.asarray(
            self.model.encode(
                normalized,
                normalize_embeddings=True,
                convert_to_numpy=True,
            ),
            dtype=np.float32,
        )

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 0), dtype=np.float32)
        normalized = [text.strip() for text in texts]
        if any(not text for text in normalized):
            raise ValueError("Cannot embed empty text values.")
        return np.asarray(
            self.model.encode(
                normalized,
                normalize_embeddings=True,
                convert_to_numpy=True,
            ),
            dtype=np.float32,
        )

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        a_vec = np.asarray(a, dtype=np.float32)
        b_vec = np.asarray(b, dtype=np.float32)
        if a_vec.size == 0 or b_vec.size == 0:
            return 0.0
        a_norm = float(np.linalg.norm(a_vec))
        b_norm = float(np.linalg.norm(b_vec))
        if a_norm == 0.0 or b_norm == 0.0:
            return 0.0
        return float(np.dot(a_vec, b_vec) / (a_norm * b_norm))

    @staticmethod
    def to_bytes(embedding: np.ndarray) -> bytes:
        return np.asarray(embedding, dtype=np.float32).tobytes()

    @staticmethod
    def from_bytes(data: bytes) -> np.ndarray:
        return np.frombuffer(data, dtype=np.float32)
