from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from graph_memory.graph import MemoryGraph
from graph_memory.models import NodeType
from graph_memory.config import AppConfig
from graph_memory.server import GraphMemoryServer, _default_graph


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


def make_app(tmp_path: Path) -> GraphMemoryServer:
    graph = MemoryGraph(tmp_path / "server-memory.db", FakeEmbeddingModel())
    config = AppConfig(
        backend="sqlite",
        transport="stdio",
        model_name="fake-model",
        db_path=str(tmp_path / "server-memory.db"),
        default_tenant_id="local-default",
        http_host="127.0.0.1",
        http_port=8080,
        log_level="INFO",
        rate_limit_rpm=120,
        write_rate_limit_rpm=60,
        max_concurrent_requests=8,
        max_payload_bytes=1024 * 1024,
        request_timeout_seconds=30,
        export_dir=None,
        neo4j_uri="",
        neo4j_username="",
        neo4j_password="",
        neo4j_database="",
    )
    return GraphMemoryServer(graph=graph, config=config)


def test_store_node_and_stats_tool(tmp_path: Path) -> None:
    app = make_app(tmp_path)

    result = app.handle_tool_call(
        "store_node",
        {
            "label": "User Preference",
            "content": "User prefers Python for backend development",
            "node_type": NodeType.PREFERENCE.value,
            "tags": ["python"],
        },
    )
    assert "Stored node" in result.content[0].text

    stats_result = app.handle_tool_call("get_stats", {})
    assert "Memory Graph Stats" in stats_result.content[0].text
    assert stats_result.structuredContent["total_nodes"] == 1


def test_export_graph_html_tool(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.handle_tool_call(
        "store_node",
        {
            "label": "Visual Node",
            "content": "The graph should be exportable as HTML.",
            "node_type": NodeType.CONCEPT.value,
        },
    )

    result = app.handle_tool_call(
        "export_graph_html",
        {
            "output_path": str(tmp_path / "visualization.html"),
            "include_physics": False,
        },
    )

    assert result.isError is False
    assert result.structuredContent["total_nodes"] == 1
    assert Path(result.structuredContent["output_path"]).exists()
    assert "Exported graph visualization" in result.content[0].text


def test_decompose_and_store_tool_persists_subgraph(tmp_path: Path) -> None:
    app = make_app(tmp_path)

    result = app.handle_tool_call(
        "decompose_and_store",
        {
            "content": "- User prefers Python\n- Project uses FastAPI",
            "context": "Backend memory",
        },
    )

    assert result.isError is False
    assert result.structuredContent["total_nodes_in_graph"] >= 3
    assert len(result.structuredContent["edges"]) >= 2
    assert "Memory Graph Results" in result.content[0].text


def test_export_and_import_backup_tools(tmp_path: Path) -> None:
    source = make_app(tmp_path / "source")
    target = make_app(tmp_path / "target")
    source.handle_tool_call(
        "store_node",
        {
            "label": "Backup Tool Node",
            "content": "This node should appear after import.",
            "node_type": NodeType.NOTE.value,
        },
    )

    backup = source.handle_tool_call(
        "export_graph_backup",
        {"output_path": str(tmp_path / "graph-backup.json")},
    )
    imported = target.handle_tool_call(
        "import_graph_backup",
        {"input_path": backup.structuredContent["output_path"]},
    )

    assert backup.isError is False
    assert Path(backup.structuredContent["output_path"]).exists()
    assert imported.isError is False
    assert imported.structuredContent["nodes_created"] == 1
    assert target.graph.get_stats().total_nodes == 1


def test_store_node_reports_deduplication(tmp_path: Path) -> None:
    app = make_app(tmp_path)

    first = app.handle_tool_call(
        "store_node",
        {
            "label": "Session Preference",
            "content": "This session prefers persistent graph memory.",
            "node_type": NodeType.PREFERENCE.value,
        },
    )
    second = app.handle_tool_call(
        "store_node",
        {
            "label": "Session Preference",
            "content": "This session prefers persistent graph memory.",
            "node_type": NodeType.PREFERENCE.value,
            "tags": ["deduped"],
        },
    )

    assert first.structuredContent["created"] is True
    assert second.structuredContent["created"] is False
    assert second.structuredContent["dedup_reason"] == "exact_content"
    assert "Reused existing node" in second.content[0].text


def test_store_node_reports_conflicts(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.handle_tool_call(
        "store_node",
        {
            "label": "REST Preference",
            "content": "User prefers REST APIs for backend work",
            "node_type": NodeType.PREFERENCE.value,
        },
    )

    result = app.handle_tool_call(
        "store_node",
        {
            "label": "GraphQL Preference",
            "content": "User prefers GraphQL APIs for backend work",
            "node_type": NodeType.PREFERENCE.value,
        },
    )

    assert result.isError is False
    assert result.structuredContent["conflicts"]


def test_observe_conversation_tool(tmp_path: Path) -> None:
    app = make_app(tmp_path)

    result = app.handle_tool_call(
        "observe_conversation",
        {
            "user_message": "I prefer Python for backend work.",
            "assistant_response": "Let's use FastAPI and update src/server.py.",
        },
    )

    assert result.isError is False
    assert result.structuredContent["created_count"] >= 2
    assert "Conversation Observation" in result.content[0].text


def test_graph_diff_prime_context_and_topics_tools(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.handle_tool_call(
        "store_node",
        {
            "label": "Alpha Project",
            "content": "Project Alpha uses FastAPI",
            "node_type": NodeType.ENTITY.value,
            "tags": ["alpha"],
        },
    )
    diff = app.handle_tool_call("graph_diff", {"since": "24h"})
    prime = app.handle_tool_call("prime_context", {"project": "alpha"})
    topics = app.handle_tool_call("get_topics", {})

    assert diff.isError is False
    assert diff.structuredContent["added_nodes"]
    assert prime.isError is False
    assert prime.structuredContent["nodes"]
    assert topics.isError is False
    assert topics.structuredContent["total_clusters"] >= 1


def test_recent_resource_serialization(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.graph.add_node(
        label="Architecture",
        content="The project uses SQLite and NetworkX",
        node_type=NodeType.CONCEPT,
    )

    resource_text = app.read_resource_text("graph://recent")
    assert "Recent Memory Nodes" in resource_text
    assert "Architecture" in resource_text


def test_unknown_tool_raises(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    result = app.handle_tool_call("does_not_exist", {})
    assert result.isError is True
    assert result.structuredContent["error_type"] == "ValidationFailure"


def test_invalid_tool_inputs_return_structured_errors(tmp_path: Path) -> None:
    app = make_app(tmp_path)

    empty_query = app.handle_tool_call("query_graph", {"query": ""})
    assert empty_query.isError is True
    assert "Query cannot be empty" in empty_query.content[0].text

    missing_node_edge = app.handle_tool_call(
        "store_edge",
        {
            "source_id": "missing-a",
            "target_id": "missing-b",
            "relationship": "relates_to",
        },
    )
    assert missing_node_edge.isError is True
    assert missing_node_edge.structuredContent["error_type"] == "ValueError"


def test_tool_payload_limit_is_enforced(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.config.max_payload_bytes = 8

    result = app.handle_tool_call(
        "store_node",
        {
            "label": "Too Large",
            "content": "this payload is definitely larger than eight bytes",
            "node_type": NodeType.NOTE.value,
        },
    )

    assert result.isError is True
    assert result.structuredContent["error_code"] == "payload_too_large"


def test_default_graph_uses_sqlite_backend_by_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GRAPH_MEMORY_BACKEND", raising=False)
    monkeypatch.setenv("GRAPH_MEMORY_DB_PATH", str(tmp_path / "sqlite-memory.db"))

    graph = _default_graph()

    assert isinstance(graph, MemoryGraph)
    assert graph.db_path == tmp_path / "sqlite-memory.db"


def test_default_graph_can_build_neo4j_backend(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeNeo4jGraph:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

    import graph_memory.neo4j_graph as neo4j_graph_module

    monkeypatch.setattr(neo4j_graph_module, "Neo4jMemoryGraph", FakeNeo4jGraph)
    monkeypatch.setenv("GRAPH_MEMORY_BACKEND", "neo4j")
    monkeypatch.setenv("GRAPH_MEMORY_MODEL", "fake-model")
    monkeypatch.setenv("GRAPH_MEMORY_EXPORT_DIR", str(tmp_path / "exports"))
    monkeypatch.setenv("GRAPH_MEMORY_NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("GRAPH_MEMORY_NEO4J_USERNAME", "neo4j")
    monkeypatch.setenv("GRAPH_MEMORY_NEO4J_PASSWORD", "secret")
    monkeypatch.setenv("GRAPH_MEMORY_NEO4J_DATABASE", "memory")

    graph = _default_graph()

    assert isinstance(graph, FakeNeo4jGraph)
    assert captured["uri"] == "bolt://localhost:7687"
    assert captured["username"] == "neo4j"
    assert captured["password"] == "secret"
    assert captured["database"] == "memory"
    assert captured["export_dir"] == str(tmp_path / "exports")


def test_default_graph_requires_neo4j_connection_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GRAPH_MEMORY_BACKEND", "neo4j")
    monkeypatch.delenv("GRAPH_MEMORY_NEO4J_URI", raising=False)
    monkeypatch.delenv("GRAPH_MEMORY_NEO4J_USERNAME", raising=False)
    monkeypatch.delenv("GRAPH_MEMORY_NEO4J_PASSWORD", raising=False)

    with pytest.raises(RuntimeError, match="Neo4j backend requires"):
        _default_graph()
