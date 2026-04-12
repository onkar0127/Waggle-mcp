# graph-memory-mcp

`graph-memory-mcp` is a persistent memory service for MCP-aware LLMs. It stores atomic facts, preferences, entities, decisions, questions, and notes as graph nodes, connects them with typed edges, and returns tenant-scoped subgraphs instead of flat text snippets.

The project now supports:
- local stdio MCP for Codex/Desktop
- hosted HTTP MCP for Kubernetes
- SQLite for local/dev
- Neo4j for production
- API-key auth and tenant isolation in hosted mode
- graph export/import, HTML visualization, decomposition, temporal retrieval, context priming, graph diff, conversation observation, and topic clustering

## Production posture

The codebase now includes the core production-hardening layer:
- tenant-aware storage on both backends
- API key creation, listing, revocation, and validation
- HTTP MCP transport with `X-API-Key`
- `/health/live`, `/health/ready`, and `/metrics`
- request size limits, timeouts, and rate limiting
- structured JSON logging
- migration path from legacy SQLite into tenant-aware Neo4j
- Docker and Kubernetes deployment assets

This is suitable for internal or team-hosted deployment. It is not positioned as an internet-scale public SaaS.

## Done vs next

### Done

- tenant-aware graph storage on SQLite and Neo4j
- API-key creation, listing, revocation, and validation
- stdio MCP and hosted HTTP MCP
- health, readiness, and metrics endpoints
- request payload limits, request timeout enforcement, and rate limiting
- graph backup/import, HTML export, temporal retrieval, conflict detection, decomposition, observation, graph diff, priming, and topic clustering
- Docker image and Kubernetes manifests
- automated tests covering graph logic, tenant isolation, HTTP auth, payload rejection, and rate limiting

### To do

- verify the Kubernetes manifests against a live cluster and real ingress setup
- run sustained load and concurrency testing against a real Neo4j deployment
- wire metrics and logs into a real observability stack
- add API-key rotation workflow documentation and operational runbooks
- validate end-to-end backup/restore drills in a staging environment
- harden deployment defaults for TLS, ingress, and secret-management tooling

## Architecture

### Layers

- Core domain: graph storage, deduplication, retrieval, decomposition, conflict detection, export/import
- Transport: stdio MCP and streamable HTTP MCP
- Platform: config, auth, tenant resolution, rate limiting, logging, metrics, health endpoints

### Backend policy

- Production: Neo4j only
- Local/dev: SQLite only

`GRAPH_MEMORY_TRANSPORT=http` requires `GRAPH_MEMORY_BACKEND=neo4j`.

## Implemented functionality

### Memory model

- Node types: `fact`, `entity`, `concept`, `preference`, `decision`, `question`, `note`
- Edge types: `relates_to`, `contradicts`, `depends_on`, `part_of`, `updates`, `derived_from`, `similar_to`
- Every node and edge now carries `tenant_id`

### Retrieval and memory quality

- sentence-transformers embeddings with `all-MiniLM-L6-v2`
- exact, label, acronym/entity, and semantic deduplication
- automatic conflict detection with `contradicts` edges
- temporal query interpretation for phrases like `recently`, `latest`, `originally`, and `last week`
- automatic decomposition into atomic nodes with inferred edges
- conversation-aware observation via `observe_conversation`
- graph diff and multi-session context priming
- community-detection topic clustering

### Operations

- JSON backup export/import with `schema_version` and `tenant_id`
- HTML graph visualization export
- startup validation for backend connectivity and embedding availability
- in-memory Prometheus-style metrics
- API-key admin commands

## MCP tools

- `store_node`
- `store_edge`
- `query_graph`
- `get_related`
- `update_node`
- `delete_node`
- `decompose_and_store`
- `observe_conversation`
- `graph_diff`
- `prime_context`
- `get_topics`
- `get_stats`
- `export_graph_html`
- `export_graph_backup`
- `import_graph_backup`

## MCP resources

- `graph://stats`
- `graph://recent`

## Installation

### Local development with SQLite

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Production or Neo4j-backed development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,neo4j]"
```

## Running the server

### Stdio MCP

```bash
GRAPH_MEMORY_TRANSPORT=stdio \
GRAPH_MEMORY_BACKEND=sqlite \
GRAPH_MEMORY_DB_PATH=./memory.db \
GRAPH_MEMORY_DEFAULT_TENANT_ID=local-default \
graph-memory-mcp
```

### HTTP MCP

```bash
GRAPH_MEMORY_TRANSPORT=http \
GRAPH_MEMORY_BACKEND=neo4j \
GRAPH_MEMORY_DEFAULT_TENANT_ID=workspace-default \
GRAPH_MEMORY_NEO4J_URI=bolt://localhost:7687 \
GRAPH_MEMORY_NEO4J_USERNAME=neo4j \
GRAPH_MEMORY_NEO4J_PASSWORD=change-me \
GRAPH_MEMORY_NEO4J_DATABASE=neo4j \
graph-memory-mcp
```

Health endpoints:
- `GET /health/live`
- `GET /health/ready`
- `GET /metrics`

HTTP MCP endpoint:
- `POST /mcp`

Use `X-API-Key` for hosted mode.

## Environment variables

### Core

- `GRAPH_MEMORY_BACKEND`: `sqlite` or `neo4j`
- `GRAPH_MEMORY_TRANSPORT`: `stdio` or `http`
- `GRAPH_MEMORY_MODEL`: embedding model name
- `GRAPH_MEMORY_DEFAULT_TENANT_ID`: default tenant for local or process-bound mode
- `GRAPH_MEMORY_EXPORT_DIR`: optional export directory

### SQLite

- `GRAPH_MEMORY_DB_PATH`: path to the SQLite file

### HTTP service

- `GRAPH_MEMORY_HTTP_HOST`
- `GRAPH_MEMORY_HTTP_PORT`
- `GRAPH_MEMORY_LOG_LEVEL`
- `GRAPH_MEMORY_RATE_LIMIT_RPM`
- `GRAPH_MEMORY_WRITE_RATE_LIMIT_RPM`
- `GRAPH_MEMORY_MAX_CONCURRENT_REQUESTS`
- `GRAPH_MEMORY_MAX_PAYLOAD_BYTES`
- `GRAPH_MEMORY_REQUEST_TIMEOUT_SECONDS`

### Neo4j

- `GRAPH_MEMORY_NEO4J_URI`
- `GRAPH_MEMORY_NEO4J_USERNAME`
- `GRAPH_MEMORY_NEO4J_PASSWORD`
- `GRAPH_MEMORY_NEO4J_DATABASE`

## Admin commands

### Create a tenant

```bash
graph-memory-mcp create-tenant --tenant-id workspace-a --name "Workspace A"
```

### Create an API key

```bash
graph-memory-mcp create-api-key --tenant-id workspace-a --name "ci-agent"
```

This returns the raw API key once. Store it outside the database; only the hash is persisted.

### List API keys

```bash
graph-memory-mcp list-api-keys --tenant-id workspace-a
```

### Revoke an API key

```bash
graph-memory-mcp revoke-api-key --api-key-id <api-key-id>
```

### Migrate legacy SQLite data into Neo4j

```bash
GRAPH_MEMORY_BACKEND=neo4j \
GRAPH_MEMORY_TRANSPORT=stdio \
GRAPH_MEMORY_DEFAULT_TENANT_ID=workspace-a \
GRAPH_MEMORY_NEO4J_URI=bolt://localhost:7687 \
GRAPH_MEMORY_NEO4J_USERNAME=neo4j \
GRAPH_MEMORY_NEO4J_PASSWORD=change-me \
graph-memory-mcp migrate-sqlite --db-path ./memory.db --tenant-id workspace-a
```

The migration path exports the SQLite graph as a portable backup and imports it into the target tenant in Neo4j.

## Codex setup

Example stdio config for local Codex use:

```toml
[mcp_servers.graph-memory]
command = "/absolute/path/to/project/.venv/bin/python"
args = ["-m", "graph_memory.server"]
cwd = "/absolute/path/to/project"
env = { PYTHONPATH = "/absolute/path/to/project/src", GRAPH_MEMORY_TRANSPORT = "stdio", GRAPH_MEMORY_BACKEND = "sqlite", GRAPH_MEMORY_DB_PATH = "/absolute/path/to/memory.db", GRAPH_MEMORY_DEFAULT_TENANT_ID = "local-default", GRAPH_MEMORY_MODEL = "all-MiniLM-L6-v2" }
```

The repo also includes [`codex_config.example.toml`](./codex_config.example.toml).

## Docker

Build:

```bash
docker build -t graph-memory-mcp:latest .
```

Run:

```bash
docker run --rm -p 8080:8080 \
  -e GRAPH_MEMORY_TRANSPORT=http \
  -e GRAPH_MEMORY_BACKEND=neo4j \
  -e GRAPH_MEMORY_DEFAULT_TENANT_ID=workspace-default \
  -e GRAPH_MEMORY_NEO4J_URI=bolt://host.docker.internal:7687 \
  -e GRAPH_MEMORY_NEO4J_USERNAME=neo4j \
  -e GRAPH_MEMORY_NEO4J_PASSWORD=change-me \
  graph-memory-mcp:latest
```

## Kubernetes

Manifests are in `deploy/kubernetes/`:
- `configmap.yaml`
- `secret.example.yaml`
- `deployment.yaml`
- `service.yaml`

Apply them after replacing the example secret values and image reference.

## Testing

```bash
.venv/bin/pytest -q
```

Current test coverage includes:
- graph CRUD and retrieval
- deduplication and conflict detection
- tenant isolation on SQLite
- backup/import metadata handling
- stdio MCP integration
- HTTP health/auth/metrics behavior
- payload limits and structured errors

## Project layout

```text
graph-memory-mcp/
├── deploy/kubernetes/
├── src/graph_memory/
├── tests/
├── Dockerfile
├── README.md
├── codex_config.example.toml
└── pyproject.toml
```
