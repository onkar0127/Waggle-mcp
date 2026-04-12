from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class NodeType(str, Enum):
    FACT = "fact"
    ENTITY = "entity"
    CONCEPT = "concept"
    PREFERENCE = "preference"
    DECISION = "decision"
    QUESTION = "question"
    NOTE = "note"


class RelationType(str, Enum):
    RELATES_TO = "relates_to"
    CONTRADICTS = "contradicts"
    DEPENDS_ON = "depends_on"
    PART_OF = "part_of"
    UPDATES = "updates"
    DERIVED_FROM = "derived_from"
    SIMILAR_TO = "similar_to"


class Node(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = ""
    label: str
    content: str
    node_type: NodeType
    tags: list[str] = Field(default_factory=list)
    source_prompt: str = ""
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    access_count: int = 0

    @field_validator("label", "content", mode="before")
    @classmethod
    def _validate_required_text(cls, value: Any) -> str:
        if value is None:
            raise ValueError("Value is required.")
        text = str(value).strip()
        if not text:
            raise ValueError("Value cannot be empty.")
        return text

    @field_validator("source_prompt", mode="before")
    @classmethod
    def _normalize_source_prompt(cls, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip()

    @field_validator("tags", mode="before")
    @classmethod
    def _normalize_tags(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value.strip()] if value.strip() else []

        normalized: list[str] = []
        seen: set[str] = set()
        for item in value:
            text = str(item).strip()
            if not text or text in seen:
                continue
            normalized.append(text)
            seen.add(text)
        return normalized


class Edge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = ""
    source_id: str
    target_id: str
    relationship: RelationType
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("source_id", "target_id", mode="before")
    @classmethod
    def _validate_node_ids(cls, value: Any) -> str:
        text = str(value).strip()
        if not text:
            raise ValueError("Node IDs cannot be empty.")
        return text


class ConnectedNodeStat(BaseModel):
    id: str
    label: str
    node_type: NodeType
    connection_count: int = 0


class RecentNodeStat(BaseModel):
    id: str
    label: str
    node_type: NodeType
    updated_at: datetime


class GraphStats(BaseModel):
    total_nodes: int = 0
    total_edges: int = 0
    node_type_breakdown: dict[str, int] = Field(default_factory=dict)
    most_connected_nodes: list[ConnectedNodeStat] = Field(default_factory=list)
    most_recent_nodes: list[RecentNodeStat] = Field(default_factory=list)


class SubgraphResult(BaseModel):
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    query: str = ""
    total_nodes_in_graph: int = 0


class ConflictRecord(BaseModel):
    other_node_id: str
    other_node_label: str
    relationship: RelationType = RelationType.CONTRADICTS
    reason: str


class NodeStoreResult(BaseModel):
    node: Node
    created: bool = True
    dedup_reason: str | None = None
    similarity: float | None = None
    conflicts: list[ConflictRecord] = Field(default_factory=list)


class BackupResult(BaseModel):
    output_path: str
    tenant_id: str = ""
    schema_version: int = 1
    node_count: int = 0
    edge_count: int = 0


class ImportResult(BaseModel):
    input_path: str
    tenant_id: str = ""
    schema_version: int = 1
    nodes_created: int = 0
    nodes_updated: int = 0
    edges_created: int = 0
    edges_updated: int = 0


class ObservationResult(BaseModel):
    stored_nodes: list[Node] = Field(default_factory=list)
    created_count: int = 0
    reused_count: int = 0
    conflicts: list[ConflictRecord] = Field(default_factory=list)


class GraphDiffResult(BaseModel):
    since: str
    generated_at: datetime = Field(default_factory=utc_now)
    added_nodes: list[Node] = Field(default_factory=list)
    updated_nodes: list[Node] = Field(default_factory=list)
    created_edges: list[Edge] = Field(default_factory=list)
    contradiction_edges: list[Edge] = Field(default_factory=list)


class PrimeContextResult(BaseModel):
    project: str = ""
    summary: str = ""
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    total_nodes_in_graph: int = 0


class TopicCluster(BaseModel):
    cluster_id: int
    label: str
    node_count: int
    top_tags: list[str] = Field(default_factory=list)
    nodes: list[Node] = Field(default_factory=list)


class TopicResult(BaseModel):
    clusters: list[TopicCluster] = Field(default_factory=list)
    total_clusters: int = 0


class TenantRecord(BaseModel):
    tenant_id: str
    name: str = ""
    status: str = "active"
    created_at: datetime = Field(default_factory=utc_now)


class ApiKeyRecord(BaseModel):
    api_key_id: str
    tenant_id: str
    key_hash: str
    name: str = ""
    status: str = "active"
    created_at: datetime = Field(default_factory=utc_now)
    last_used_at: datetime | None = None


class ApiKeyCreateResult(BaseModel):
    record: ApiKeyRecord
    raw_api_key: str
