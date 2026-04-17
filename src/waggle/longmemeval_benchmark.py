from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from waggle.benchmark_harness import BenchmarkRuntimeError, _graph, _set_node_timestamp
from waggle.embeddings import EmbeddingModel
from waggle.intelligence import infer_temporal_hints, lexical_overlap
from waggle.models import NodeType


@dataclass
class LongMemEvalCaseResult:
    query_id: str
    question: str
    correct_session_ids: list[str]
    retrieved_session_ids: list[str]
    hit_at_5: bool
    exact_at_5: bool


@dataclass
class LongMemEvalReport:
    dataset_path: str
    mode: str
    case_count: int
    r_at_5: float
    exact_at_5: float
    per_case: list[LongMemEvalCaseResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_path": self.dataset_path,
            "mode": self.mode,
            "case_count": self.case_count,
            "r_at_5": self.r_at_5,
            "exact_at_5": self.exact_at_5,
            "per_case": [asdict(case) for case in self.per_case],
        }


def _load_entries(path: str | Path) -> list[dict[str, Any]]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("entries", "data", "questions"):
            value = raw.get(key)
            if isinstance(value, list):
                return value
    raise BenchmarkRuntimeError("Unsupported LongMemEval file shape. Expected a list or dict with entries/data/questions.")


def _extract_correct_session_ids(entry: dict[str, Any]) -> list[str]:
    for key in (
        "correct_session_ids",
        "answer_session_ids",
        "needle_session_ids",
        "ground_truth_session_ids",
        "support_session_ids",
    ):
        value = entry.get(key)
        if isinstance(value, list) and value:
            return [str(item) for item in value]
    for key in ("correct_session_id", "answer_session_id", "needle_session_id"):
        value = entry.get(key)
        if value:
            return [str(value)]
    raise BenchmarkRuntimeError("Could not find ground-truth session IDs in LongMemEval entry.")


def _normalize_timestamp(raw: str) -> str:
    text = str(raw).strip()
    if not text:
        return datetime.now(timezone.utc).isoformat()
    try:
        if "/" in text and " (" in text:
            parsed = datetime.strptime(text.split(" (", 1)[0], "%Y/%m/%d")
        else:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc).isoformat()
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def _session_text(session: list[dict[str, Any]], *, include_assistant: bool) -> str:
    lines: list[str] = []
    for turn in session:
        role = str(turn.get("role", "unknown")).strip()
        content = str(turn.get("content", "")).strip()
        if not content:
            continue
        if include_assistant or role == "user":
            lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _session_id_from_tags(tags: list[str]) -> str | None:
    for tag in tags:
        if tag.startswith("session_id:"):
            return tag.split(":", 1)[1]
    return None


def _rank_candidates_heuristic(question: str, nodes: list[Any], *, top_k: int) -> list[Any]:
    temporal_hints = infer_temporal_hints(question)
    max_timestamp = max((node.updated_at.timestamp() for node in nodes), default=1.0)
    min_timestamp = min((node.updated_at.timestamp() for node in nodes), default=0.0)
    span = max(max_timestamp - min_timestamp, 1.0)
    scored: list[tuple[float, int, Any]] = []
    for index, node in enumerate(nodes):
        base_score = 1.0 / (index + 1)
        lexical_score = lexical_overlap(question, node.label, node.content)
        temporal_score = 0.0
        if temporal_hints.recency_mode == "latest":
            temporal_score = (node.updated_at.timestamp() - min_timestamp) / span
        elif temporal_hints.recency_mode == "oldest":
            temporal_score = (max_timestamp - node.updated_at.timestamp()) / span
        score = (0.5 * base_score) + (0.35 * lexical_score) + (0.15 * temporal_score)
        scored.append((score, -index, node))
    return [item[2] for item in sorted(scored, key=lambda item: (-item[0], item[1]))[:top_k]]


def _build_entry_graph(entry: dict[str, Any], *, mode: str, embedding_model: Any) -> Any:
    graph = _graph(embedding_model)
    sessions = entry["haystack_sessions"]
    session_ids = entry["haystack_session_ids"]
    dates = entry["haystack_dates"]
    include_assistant = mode == "graph_hybrid"
    for session, session_id, raw_date in zip(sessions, session_ids, dates, strict=True):
        content = _session_text(session, include_assistant=include_assistant)
        if not content.strip():
            continue
        result = graph.add_node(
            label=f"LongMemEval Session {session_id}",
            content=content,
            node_type=NodeType.NOTE,
            tags=["longmemeval", f"session_id:{session_id}"],
        )
        _set_node_timestamp(graph, result.node.id, _normalize_timestamp(str(raw_date)))
    return graph


def evaluate_longmemeval(
    dataset_path: str | Path,
    *,
    embedding_model: Any | None = None,
    mode: Literal["graph_raw", "graph_hybrid"] = "graph_raw",
    limit: int | None = None,
) -> LongMemEvalReport:
    entries = _load_entries(dataset_path)
    if limit is not None:
        entries = entries[:limit]
    model_instance = embedding_model or EmbeddingModel()
    results: list[LongMemEvalCaseResult] = []
    for index, entry in enumerate(entries, start=1):
        graph = _build_entry_graph(entry, mode=mode, embedding_model=model_instance)
        question = str(entry["question"])
        subgraph = graph.query(query=question, max_nodes=20, max_depth=0)
        if mode == "graph_raw":
            ranked_nodes = subgraph.nodes[:5]
        else:
            ranked_nodes = _rank_candidates_heuristic(question, subgraph.nodes, top_k=5)
        retrieved_session_ids = [
            session_id
            for node in ranked_nodes
            for session_id in [_session_id_from_tags(node.tags)]
            if session_id is not None
        ]
        gold_ids = _extract_correct_session_ids(entry)
        retrieved_set = set(retrieved_session_ids[:5])
        gold_set = set(gold_ids)
        results.append(
            LongMemEvalCaseResult(
                query_id=str(entry.get("id", f"entry_{index}")),
                question=question,
                correct_session_ids=gold_ids,
                retrieved_session_ids=retrieved_session_ids[:5],
                hit_at_5=bool(retrieved_set & gold_set),
                exact_at_5=gold_set.issubset(retrieved_set),
            )
        )
    case_count = len(results)
    hit_rate = sum(1 if result.hit_at_5 else 0 for result in results) / case_count if case_count else 0.0
    exact_rate = sum(1 if result.exact_at_5 else 0 for result in results) / case_count if case_count else 0.0
    return LongMemEvalReport(
        dataset_path=str(dataset_path),
        mode=mode,
        case_count=case_count,
        r_at_5=hit_rate,
        exact_at_5=exact_rate,
        per_case=results,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Exploratory LongMemEval adapter for Waggle.")
    parser.add_argument("dataset_path", type=Path, help="Path to longmemeval_s_cleaned.json or equivalent cleaned dataset.")
    parser.add_argument("--mode", choices=["graph_raw", "graph_hybrid"], default="graph_raw")
    parser.add_argument("--limit", type=int, default=None, help="Optional number of entries to evaluate.")
    parser.add_argument("--embedding-model", default="all-MiniLM-L6-v2")
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    report = evaluate_longmemeval(
        args.dataset_path,
        embedding_model=EmbeddingModel(args.embedding_model),
        mode=args.mode,
        limit=args.limit,
    )
    print("=" * 72)
    print("waggle LongMemEval exploratory benchmark")
    print("=" * 72)
    print(f"dataset: {report.dataset_path}")
    print(f"mode: {report.mode}")
    print(f"cases: {report.case_count}")
    print(f"R@5: {report.r_at_5:.1%}")
    print(f"Exact@5: {report.exact_at_5:.1%}")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
        print(f"wrote JSON report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
