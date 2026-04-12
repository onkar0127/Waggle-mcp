from __future__ import annotations

import asyncio
from pathlib import Path

import numpy as np
import pytest
from starlette.testclient import TestClient

from graph_memory.auth import hash_api_key, verify_api_key
from graph_memory.config import AppConfig
from graph_memory.errors import RateLimitExceededError
from graph_memory.graph import MemoryGraph
from graph_memory.models import NodeType
from graph_memory.rate_limit import RateLimiter
from graph_memory.server import GraphMemoryServer, create_http_application


class FakeEmbeddingModel:
    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(8, dtype=np.float32)
        for token in text.lower().split():
            vector[sum(ord(character) for character in token) % len(vector)] += 1.0
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


def make_graph(tmp_path: Path, tenant_id: str = "local-default") -> MemoryGraph:
    return MemoryGraph(tmp_path / "memory.db", FakeEmbeddingModel(), tenant_id=tenant_id)


def make_http_config(tmp_path: Path, **overrides: object) -> AppConfig:
    config = AppConfig(
        backend="neo4j",
        transport="http",
        model_name="fake-model",
        db_path=str(tmp_path / "memory.db"),
        default_tenant_id="local-default",
        http_host="127.0.0.1",
        http_port=8080,
        log_level="INFO",
        rate_limit_rpm=10,
        write_rate_limit_rpm=5,
        max_concurrent_requests=2,
        max_payload_bytes=1024 * 1024,
        request_timeout_seconds=30,
        export_dir=None,
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="secret",
        neo4j_database="neo4j",
    )
    for key, value in overrides.items():
        setattr(config, key, value)
    return config


def test_api_key_hashing_round_trip() -> None:
    hashed = hash_api_key("secret-token")
    assert hashed != "secret-token"
    assert verify_api_key("secret-token", hashed) is True
    assert verify_api_key("wrong-token", hashed) is False


def test_rate_limiter_enforces_request_and_concurrency_limits() -> None:
    limiter = RateLimiter(requests_per_minute=1, write_requests_per_minute=1, max_concurrent_requests=1)

    async def exercise() -> None:
        await limiter.check_rate("tenant-a", is_write=False)
        with pytest.raises(RateLimitExceededError):
            await limiter.check_rate("tenant-a", is_write=False)

        async with limiter.concurrency_slot("tenant-a"):
            with pytest.raises(RateLimitExceededError):
                async with limiter.concurrency_slot("tenant-a"):
                    pass

    asyncio.run(exercise())


def test_tenant_scoping_isolated_within_same_sqlite_database(tmp_path: Path) -> None:
    root = make_graph(tmp_path)
    tenant_a = root.for_tenant("tenant-a")
    tenant_b = root.for_tenant("tenant-b")

    tenant_a.add_node(
        label="Tenant A Project",
        content="Tenant A stores isolated memory",
        node_type=NodeType.ENTITY,
    )

    assert tenant_a.get_stats().total_nodes == 1
    assert tenant_b.get_stats().total_nodes == 0
    assert tenant_b.query(query="isolated memory", max_nodes=5, max_depth=1).nodes == []


def test_backup_round_trip_preserves_schema_and_tenant_metadata(tmp_path: Path) -> None:
    source = make_graph(tmp_path / "source", tenant_id="tenant-source")
    source.add_node(
        label="Tenant Source Node",
        content="Backup metadata should include tenant identity.",
        node_type=NodeType.NOTE,
    )

    backup = source.export_graph_backup(output_path=tmp_path / "source" / "backup.json")
    target = make_graph(tmp_path / "target", tenant_id="tenant-target")
    imported = target.import_graph_backup(input_path=backup.output_path)

    assert backup.tenant_id == "tenant-source"
    assert backup.schema_version >= 2
    assert imported.tenant_id == "tenant-target"
    assert imported.schema_version >= 2
    assert target.get_stats().total_nodes == 1


def test_http_app_health_auth_and_metrics(tmp_path: Path) -> None:
    graph = make_graph(tmp_path)
    app_server = GraphMemoryServer(graph=graph, config=make_http_config(tmp_path))
    created = graph.create_api_key("tenant-http", "http-test")
    app = create_http_application(app_server, app_server.config)

    with TestClient(app) as client:
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200

        missing = client.post("/mcp", json={})
        assert missing.status_code == 401
        invalid = client.post("/mcp", json={}, headers={"X-API-Key": "bad-key"})
        assert invalid.status_code == 401

        valid = client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}},
            headers={"X-API-Key": created.raw_api_key, "accept": "application/json, text/event-stream"},
        )
        assert valid.status_code == 200

        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "graph_memory_http_requests_total" in metrics.text
        assert "graph_memory_ready" in metrics.text


def test_http_app_rate_limit_and_payload_limit(tmp_path: Path) -> None:
    graph = make_graph(tmp_path)
    config = make_http_config(tmp_path, rate_limit_rpm=1, max_payload_bytes=256)
    app_server = GraphMemoryServer(graph=graph, config=config)
    created = graph.create_api_key("tenant-http", "http-test")
    app = create_http_application(app_server, config)

    with TestClient(app) as client:
        too_large = client.post(
            "/mcp",
            content=b"x" * 512,
            headers={"X-API-Key": created.raw_api_key},
        )
        assert too_large.status_code == 413

        first = client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}},
            headers={"X-API-Key": created.raw_api_key, "accept": "application/json, text/event-stream"},
        )
        second = client.post(
            "/mcp",
            json={"jsonrpc": "2.0", "id": "2", "method": "tools/list", "params": {}},
            headers={"X-API-Key": created.raw_api_key, "accept": "application/json, text/event-stream"},
        )

        assert first.status_code == 200
        assert second.status_code == 429
