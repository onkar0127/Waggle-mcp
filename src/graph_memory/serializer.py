from __future__ import annotations

from graph_memory.models import (
    GraphDiffResult,
    GraphStats,
    Node,
    ObservationResult,
    PrimeContextResult,
    SubgraphResult,
    TopicResult,
)


def serialize_subgraph(result: SubgraphResult) -> str:
    """Convert a subgraph result into readable text for an LLM."""
    if not result.nodes:
        return "=== Memory Graph: No results found ==="

    lines = [
        f"=== Memory Graph Results ({len(result.nodes)} nodes, {len(result.edges)} edges) ===",
        "",
        "[NODES]",
    ]

    for node in result.nodes:
        tags_suffix = f" tags:{node.tags}" if node.tags else ""
        lines.append(
            f'• (id: {node.id[:8]}) [{node.node_type.value}] "{node.label}" — {node.content} '
            f"(created: {node.created_at.strftime('%Y-%m-%d')}, accessed: {node.access_count} times){tags_suffix}"
        )

    lines.append("")
    lines.append("[RELATIONSHIPS]")
    if result.edges:
        label_map = {node.id: node.label for node in result.nodes}
        for edge in result.edges:
            source_label = label_map.get(edge.source_id, edge.source_id[:8])
            target_label = label_map.get(edge.target_id, edge.target_id[:8])
            lines.append(
                f'• "{source_label}" --[{edge.relationship.value}]--> "{target_label}"'
            )
    else:
        lines.append("• No connecting relationships in this subgraph.")

    lines.extend(["", "=== End Results ==="])
    return "\n".join(lines)


def serialize_stats(stats: GraphStats) -> str:
    lines = [
        "=== Memory Graph Stats ===",
        f"Total nodes: {stats.total_nodes}",
        f"Total edges: {stats.total_edges}",
        "",
        "[NODE TYPES]",
    ]

    for node_type, count in stats.node_type_breakdown.items():
        lines.append(f"• {node_type}: {count}")

    lines.extend(["", "[MOST CONNECTED]"])
    if stats.most_connected_nodes:
        for node in stats.most_connected_nodes:
            lines.append(
                f'• "{node.label}" ({node.node_type.value}) — {node.connection_count} connections'
            )
    else:
        lines.append("• No nodes stored yet.")

    lines.extend(["", "[MOST RECENT]"])
    if stats.most_recent_nodes:
        for node in stats.most_recent_nodes:
            lines.append(
                f'• "{node.label}" ({node.node_type.value}) — updated {node.updated_at.strftime("%Y-%m-%d %H:%M:%S UTC")}'
            )
    else:
        lines.append("• No nodes stored yet.")

    lines.append("=== End Stats ===")
    return "\n".join(lines)


def serialize_recent_nodes(nodes: list[Node]) -> str:
    if not nodes:
        return "=== Recent Memory Nodes: No nodes stored ==="

    lines = ["=== Recent Memory Nodes ==="]
    for node in nodes:
        lines.append(
            f'• (id: {node.id[:8]}) [{node.node_type.value}] "{node.label}" — '
            f"updated {node.updated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
    lines.append("=== End Recent Nodes ===")
    return "\n".join(lines)


def serialize_observation_result(result: ObservationResult) -> str:
    lines = [
        "=== Conversation Observation ===",
        f"Stored nodes: {len(result.stored_nodes)}",
        f"Created: {result.created_count}",
        f"Reused: {result.reused_count}",
    ]
    if result.stored_nodes:
        lines.extend(["", "[STORED]"])
        for node in result.stored_nodes:
            lines.append(f'• [{node.node_type.value}] "{node.label}"')
    if result.conflicts:
        lines.extend(["", "[CONFLICTS]"])
        for conflict in result.conflicts:
            lines.append(f'• "{conflict.other_node_label}" — {conflict.reason}')
    lines.append("=== End Observation ===")
    return "\n".join(lines)


def serialize_graph_diff(result: GraphDiffResult) -> str:
    lines = [
        f"=== Graph Diff Since {result.since} ===",
        f"Nodes added: {len(result.added_nodes)}",
        f"Nodes updated: {len(result.updated_nodes)}",
        f"Edges created: {len(result.created_edges)}",
        f"Contradictions detected: {len(result.contradiction_edges)}",
    ]
    if result.added_nodes:
        lines.extend(["", "[ADDED NODES]"])
        for node in result.added_nodes:
            lines.append(f'• [{node.node_type.value}] "{node.label}"')
    if result.updated_nodes:
        lines.extend(["", "[UPDATED NODES]"])
        for node in result.updated_nodes:
            lines.append(f'• [{node.node_type.value}] "{node.label}"')
    if result.created_edges:
        lines.extend(["", "[CREATED EDGES]"])
        for edge in result.created_edges:
            lines.append(f"• {edge.source_id[:8]} --[{edge.relationship.value}]--> {edge.target_id[:8]}")
    if result.contradiction_edges:
        lines.extend(["", "[CONTRADICTIONS]"])
        for edge in result.contradiction_edges:
            lines.append(f"• {edge.source_id[:8]} contradicts {edge.target_id[:8]}")
    lines.append("=== End Diff ===")
    return "\n".join(lines)


def serialize_prime_context(result: PrimeContextResult) -> str:
    if not result.nodes:
        return "=== Prime Context: No memory available ==="

    lines = [
        "=== Prime Context ===",
        result.summary,
        "",
        "[NODES]",
    ]
    for node in result.nodes:
        lines.append(f'• [{node.node_type.value}] "{node.label}" — {node.content}')
    lines.extend(["", "[RELATIONSHIPS]"])
    if result.edges:
        label_map = {node.id: node.label for node in result.nodes}
        for edge in result.edges:
            source_label = label_map.get(edge.source_id, edge.source_id[:8])
            target_label = label_map.get(edge.target_id, edge.target_id[:8])
            lines.append(f'• "{source_label}" --[{edge.relationship.value}]--> "{target_label}"')
    else:
        lines.append("• No connecting relationships in this brief.")
    lines.append("=== End Prime Context ===")
    return "\n".join(lines)


def serialize_topics(result: TopicResult) -> str:
    if not result.clusters:
        return "=== Topics: No topics detected ==="

    lines = [
        f"=== Topics ({result.total_clusters} clusters) ===",
    ]
    for cluster in result.clusters:
        tag_suffix = f" tags:{cluster.top_tags}" if cluster.top_tags else ""
        lines.append(f'• Cluster {cluster.cluster_id}: "{cluster.label}" — {cluster.node_count} nodes{tag_suffix}')
        for node in cluster.nodes[:5]:
            lines.append(f'  - [{node.node_type.value}] "{node.label}"')
    lines.append("=== End Topics ===")
    return "\n".join(lines)
