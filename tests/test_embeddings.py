from __future__ import annotations

import numpy as np

from graph_memory.embeddings import EmbeddingModel


def test_embedding_bytes_round_trip() -> None:
    vector = np.array([0.1, 0.2, 0.3], dtype=np.float32)
    encoded = EmbeddingModel.to_bytes(vector)
    decoded = EmbeddingModel.from_bytes(encoded)
    assert np.allclose(decoded, vector)


def test_cosine_similarity_handles_orthogonal_vectors() -> None:
    a = np.array([1.0, 0.0], dtype=np.float32)
    b = np.array([0.0, 1.0], dtype=np.float32)
    assert EmbeddingModel.cosine_similarity(a, b) == 0.0
