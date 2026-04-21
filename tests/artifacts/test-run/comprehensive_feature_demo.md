# Waggle MCP Comprehensive Feature Demo

Generated (UTC): `2026-04-21T04:31:58.434002+00:00`
Workspace: `/Users/abhigyanshekhar/Desktop/MCP`
Database (primary): `/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/demo-memory.db`
Database (restore validation): `/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/restored-memory.db`

## Summary

- Total calls recorded: **46**
- Calls with errors: **0**
- Unique actions covered: **25**
- Covered tools/actions: `decompose_and_store, delete_node, export_context_bundle, export_graph_backup, export_graph_html, export_markdown_vault, get_node_history, get_related, get_stats, get_topics, graph_diff, import_graph_backup, import_markdown_vault, initialize, list_conflicts, list_context_scopes, list_resources, list_tools, observe_conversation, prime_context, query_graph, store_edge, store_node, timeline, update_node`
- Embedding model: **all-MiniLM-L6-v2**

## CLI Feature Guide Output

```text
waggle-mcp feature guide
========================

Core graph workflow
-------------------
1. Ingest memory
   - observe_conversation : extract structured facts/decisions from a finished turn
   - decompose_and_store  : split long content into linked atomic nodes
   - store_node           : save one standalone node directly
   - store_edge           : connect nodes explicitly when relationship is known

2. Retrieve context
   - query_graph          : semantic retrieval over nodes plus graph/replay/fusion context
   - get_related          : walk outward from one node to inspect connected context
   - get_node_history     : inspect one node's evidence, validity, and linked context
   - timeline             : see recent graph events chronologically
   - prime_context        : build a compact briefing for a new model/session

3. Resolve conflicts
   - list_conflicts       : list contradiction/update edges
   - resolve_conflict     : mark a conflict as resolved without deleting history

4. Export / handoff
   - export_context_bundle : create markdown/json context packages for another model
   - export_markdown_vault : export one-file-per-node markdown for manual editing
   - import_markdown_vault : re-import edited markdown vault files
   - export_graph_backup   : portable json backup
   - import_graph_backup   : restore backup into the active backend
   - export_graph_html     : interactive graph visualization

5. Inspect the graph
   - get_stats            : node/edge counts and high-level graph stats
   - list_context_scopes  : available project / agent / session scopes
   - get_topics           : topic clusters via community detection
   - graph_diff           : recently changed nodes and edges

Important behavior
------------------
- store_node alone does not create edges.
- Edges come from:
  - explicit store_edge calls
  - observe_conversation extraction
  - decompose_and_store inferred structure
  - automatic contradiction/update detection in some cases
- The graph-aware tools are what bring connected context back to the model:
  - query_graph
  - get_related
  - get_node_history
  - prime_context
  - export_context_bundle

Common workflows
----------------
- Quick setup:
  waggle-mcp init

- Start the MCP server:
  waggle-mcp serve

- Export a handoff bundle:
  waggle-mcp export-context-bundle --mode query --query "why did we choose PostgreSQL?"

- Edit memory as markdown:
  waggle-mcp export-markdown-vault --root-path ./vault
  waggle-mcp import-markdown-vault --root-path ./vault
```

## Tool Call Transcript

### 1. `initialize` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "server": "waggle",
  "version": "0.2.0"
}
```

Text output:
```text
Connected to waggle 0.2.0
```

### 2. `list_tools` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "tool_names": [
    "store_node",
    "store_edge",
    "query_graph",
    "get_related",
    "get_node_history",
    "list_context_scopes",
    "timeline",
    "list_conflicts",
    "resolve_conflict",
    "update_node",
    "delete_node",
    "decompose_and_store",
    "observe_conversation",
    "graph_diff",
    "prime_context",
    "get_topics",
    "get_stats",
    "export_graph_html",
    "export_graph_backup",
    "export_context_bundle",
    "import_graph_backup",
    "export_markdown_vault",
    "import_markdown_vault"
  ]
}
```

Text output:
```text
23 tools available
```

### 3. `list_resources` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "resources": [
    "graph://stats",
    "graph://recent"
  ]
}
```

Text output:
```text
2 resources available
```

### 4. `observe_conversation` [OK]

Arguments:
```json
{
  "user_message": "Should we use PostgreSQL or MySQL for production?",
  "assistant_response": "Decision: use PostgreSQL for production due to reliability and team readiness.",
  "agent_id": "demo-agent",
  "project": "waggle-demo",
  "session_id": "s1"
}
```

Structured content:
```json
{
  "stored_nodes": [
    {
      "id": "8ad9e2f5-972a-4a2f-a14f-d009f95ef101",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s1",
      "label": "Should we use PostgreSQL or MySQL for production?",
      "content": "Should we use PostgreSQL or MySQL for production?",
      "node_type": "question",
      "tags": [
        "observed",
        "speaker:user"
      ],
      "source_prompt": "user: Should we use PostgreSQL or MySQL for production?\nassistant: Decision: use PostgreSQL for production due to reliability and team readiness.",
      "evidence_records": [
        {
          "evidence_id": "1ccdabe0-6dda-4be6-9e4f-040984d0dac4",
          "session_id": "s1",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Should we use PostgreSQL or MySQL for production?",
          "source_span_start": 6,
          "source_span_end": 55,
          "observed_at": "2026-04-21T04:31:30.755706+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:30.755706+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.683917+00:00",
      "updated_at": "2026-04-21T04:31:53.683919+00:00",
      "access_count": 0
    },
    {
      "id": "1eb1a89b-43b8-4a95-8e5a-e2b3fafa69e9",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s1",
      "label": "Decision",
      "content": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "node_type": "entity",
      "tags": [
        "observed",
        "speaker:assistant"
      ],
      "source_prompt": "user: Should we use PostgreSQL or MySQL for production?\nassistant: Decision: use PostgreSQL for production 
... [truncated]
```

Text output:
```text
=== Conversation Observation ===
Stored nodes: 2
Created: 2
Reused: 0

[STORED]
• [question] "Should we use PostgreSQL or MySQL for production?"
• [entity] "Decision"
=== End Observation ===
```

### 5. `observe_conversation` [OK]

Arguments:
```json
{
  "user_message": "Actually we might switch to MySQL because team familiarity is higher.",
  "assistant_response": "Noted: potential switch to MySQL due to team familiarity.",
  "agent_id": "demo-agent",
  "project": "waggle-demo",
  "session_id": "s2"
}
```

Structured content:
```json
{
  "stored_nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.703960+00:00",
      "access_count": 0
    },
    {
      "id": "b5c3883e-5981-46b9-92ee-b9ea04ce1098",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "team familiarity is higher",
      "content": "Team familiarity is higher.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:user",
        "decision-rationale",
        "database"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because
... [truncated]
```

Text output:
```text
=== Conversation Observation ===
Stored nodes: 3
Created: 2
Reused: 1

[STORED]
• [decision] "Database decision"
• [fact] "team familiarity is higher"
• [decision] "Database decision"
=== End Observation ===
```

### 6. `observe_conversation` [OK]

Arguments:
```json
{
  "user_message": "Frontend default should be dark mode and auth token expiry is 15 minutes.",
  "assistant_response": "Stored preference for dark mode and JWT expiry = 15 minutes.",
  "agent_id": "demo-agent",
  "project": "waggle-demo",
  "session_id": "s3"
}
```

Structured content:
```json
{
  "stored_nodes": [
    {
      "id": "e186755a-5dba-4652-bb6b-5ba6a2076156",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s3",
      "label": "JWT expiry",
      "content": "JWT tokens expire in 15 minutes.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:assistant",
        "auth"
      ],
      "source_prompt": "user: Frontend default should be dark mode and auth token expiry is 15 minutes.\nassistant: Stored preference for dark mode and JWT expiry = 15 minutes.",
      "evidence_records": [
        {
          "evidence_id": "b446ab25-65e5-45dc-845b-8cda726e21c5",
          "session_id": "s3",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "JWT tokens expire in 15 minutes.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:53.717861+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.717861+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.727399+00:00",
      "updated_at": "2026-04-21T04:31:53.727401+00:00",
      "access_count": 0
    }
  ],
  "created_count": 1,
  "reused_count": 0,
  "conflicts": []
}
```

Text output:
```text
=== Conversation Observation ===
Stored nodes: 1
Created: 1
Reused: 0

[STORED]
• [fact] "JWT expiry"
=== End Observation ===
```

### 7. `store_node` [OK]

Arguments:
```json
{
  "label": "API rate limiting",
  "content": "Apply 100 req/min baseline and burst controls.",
  "node_type": "concept",
  "tags": [
    "api",
    "ops"
  ]
}
```

Structured content:
```json
{
  "id": "ec17c243-91e7-44af-8820-68d97dddfc33",
  "tenant_id": "local-default",
  "agent_id": "",
  "project": "",
  "session_id": "",
  "label": "API rate limiting",
  "content": "Apply 100 req/min baseline and burst controls.",
  "node_type": "concept",
  "tags": [
    "api",
    "ops"
  ],
  "source_prompt": "",
  "evidence_records": [],
  "valid_from": null,
  "valid_to": null,
  "created_at": "2026-04-21T04:31:53.733889+00:00",
  "updated_at": "2026-04-21T04:31:53.733889+00:00",
  "access_count": 0,
  "created": true,
  "dedup_reason": null,
  "similarity": null,
  "conflicts": []
}
```

Text output:
```text
Stored node 'API rate limiting' with id ec17c243-91e7-44af-8820-68d97dddfc33.
```

### 8. `store_node` [OK]

Arguments:
```json
{
  "label": "Bench preference",
  "content": "Use Python for benchmark harness scripts.",
  "node_type": "preference",
  "tags": [
    "benchmark",
    "python"
  ]
}
```

Structured content:
```json
{
  "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
  "tenant_id": "local-default",
  "agent_id": "",
  "project": "",
  "session_id": "",
  "label": "Bench preference",
  "content": "Use Python for benchmark harness scripts.",
  "node_type": "preference",
  "tags": [
    "benchmark",
    "python"
  ],
  "source_prompt": "",
  "evidence_records": [],
  "valid_from": null,
  "valid_to": null,
  "created_at": "2026-04-21T04:31:53.740795+00:00",
  "updated_at": "2026-04-21T04:31:53.740795+00:00",
  "access_count": 0,
  "created": true,
  "dedup_reason": null,
  "similarity": null,
  "conflicts": []
}
```

Text output:
```text
Stored node 'Bench preference' with id 1c9a42b5-62b6-444a-a8b9-9aa49bcefa03.
```

### 9. `store_edge` [OK]

Arguments:
```json
{
  "source_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
  "target_id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
  "relationship": "relates_to",
  "weight": 0.72
}
```

Structured content:
```json
{
  "id": "fee765f4-8a72-434a-9a19-b98bb223a0f4",
  "tenant_id": "local-default",
  "source_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
  "target_id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
  "relationship": "relates_to",
  "weight": 0.72,
  "metadata": {},
  "created_at": "2026-04-21T04:31:53.748027+00:00"
}
```

Text output:
```text
Created edge fee765f4-8a72-434a-9a19-b98bb223a0f4 linking ec17c243-91e7-44af-8820-68d97dddfc33 to 1c9a42b5-62b6-444a-a8b9-9aa49bcefa03 as relates_to.
```

### 10. `decompose_and_store` [OK]

Arguments:
```json
{
  "content": "- Add integration tests\n- Keep dark mode default\n- Keep PostgreSQL migration scripts reviewed weekly",
  "context": "Milestone backlog"
}
```

Structured content:
```json
{
  "query": "decomposition:Milestone backlog",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "f08ece06-224b-4fc4-be43-df99423f374c",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Milestone backlog",
      "content": "Milestone backlog",
      "node_type": "concept",
      "tags": [
        "decomposition-context"
      ],
      "source_prompt": "- Add integration tests\n- Keep dark mode default\n- Keep PostgreSQL migration scripts reviewed weekly",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.749907+00:00",
      "updated_at": "2026-04-21T04:31:53.749908+00:00",
      "access_count": 0
    },
    {
      "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Add integration tests",
      "content": "Add integration tests",
      "node_type": "fact",
      "tags": [
        "decomposed"
      ],
      "source_prompt": "Milestone backlog",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.753712+00:00",
      "updated_at": "2026-04-21T04:31:53.753712+00:00",
      "access_count": 0
    },
    {
      "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Keep dark mode default",
      "content": "Keep dark mode default",
      "node_type": "fact",
      "tags": [
        "decomposed"
      ],
      "source_prompt": "Milestone backlog",
      "evidence_records": [],
      "valid_from": null,
     
... [truncated]
```

Text output:
```text
=== Memory Graph Results (4 nodes, 5 edges, mode=graph) ===

[NODES]
• (id: f08ece06) [concept] "Milestone backlog" — Milestone backlog (created: 2026-04-21, accessed: 0 times) tags:['decomposition-context']
• (id: 00bc20c5) [fact] "Add integration tests" — Add integration tests (created: 2026-04-21, accessed: 0 times) tags:['decomposed']
• (id: bf706135) [fact] "Keep dark mode default" — Keep dark mode default (created: 2026-04-21, accessed: 0 times) tags:['decomposed']
• (id: 4940810b) [fact] "Keep PostgreSQL migration scripts reviewed weekly" — Keep PostgreSQL migration scripts reviewed weekly (created: 2026-04-21, accessed: 0 times) tags:['decomposed']

[RELATIONSHIPS]
• "Add integration tests" --[part_of]--> "Milestone backlog"
• "Keep dark mode default" --[part_of]--> "Milestone backlog"
• "Keep PostgreSQL migration scripts reviewed weekly" --[part_of]--> "Milestone backlog"
• "Add integration tests" --[derived_from]--> "Keep dark mode default"
• "Keep dark mode default" --[relates_to]--> "Keep PostgreSQL migration scripts reviewed weekly"

=== End Results ===
```

### 11. `query_graph` [OK]

Arguments:
```json
{
  "query": "database decision",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "graph",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "database decision",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ff838771-fcaa-48a8-b7d2-79cca78ef927",
          "session_id": "s2",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": 87,
          "source_span_end": 144,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        },
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.714789+00:00",
      "access_c
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=graph) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 1 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 1 times) tags:['observed', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 1 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 1 times) tags:['observed', 'speaker:user']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 1 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

=== End Results ===
```

### 12. `query_graph` [OK]

Arguments:
```json
{
  "query": "latest database direction",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "graph",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "latest database direction",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "e186755a-5dba-4652-bb6b-5ba6a2076156",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s3",
      "label": "JWT expiry",
      "content": "JWT tokens expire in 15 minutes.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:assistant",
        "auth"
      ],
      "source_prompt": "user: Frontend default should be dark mode and auth token expiry is 15 minutes.\nassistant: Stored preference for dark mode and JWT expiry = 15 minutes.",
      "evidence_records": [
        {
          "evidence_id": "b446ab25-65e5-45dc-845b-8cda726e21c5",
          "session_id": "s3",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "JWT tokens expire in 15 minutes.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:53.717861+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.717861+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.727399+00:00",
      "updated_at": "2026-04-21T04:31:53.727401+00:00",
      "access_count": 2
    },
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "sou
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=graph) ===

[NODES]
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 2 times) tags:['observed', 'speaker:assistant', 'auth']
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 2 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 2 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 2 times) tags:['observed', 'speaker:assistant']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 2 times) tags:['observed', 'speaker:user']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

=== End Results ===
```

### 13. `query_graph` [OK]

Arguments:
```json
{
  "query": "original database choice",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "graph",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "original database choice",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ff838771-fcaa-48a8-b7d2-79cca78ef927",
          "session_id": "s2",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": 87,
          "source_span_end": 144,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        },
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.714789+00:00",
      "a
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=graph) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 3 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 3 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 3 times) tags:['observed', 'speaker:user']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 3 times) tags:['observed', 'speaker:assistant']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 3 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

=== End Results ===
```

### 14. `query_graph` [OK]

Arguments:
```json
{
  "query": "dark mode preference",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "graph",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "dark mode preference",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ff838771-fcaa-48a8-b7d2-79cca78ef927",
          "session_id": "s2",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": 87,
          "source_span_end": 144,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        },
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.714789+00:00",
      "acces
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=graph) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 4 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 4 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 4 times) tags:['observed', 'speaker:user']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 4 times) tags:['observed', 'speaker:assistant']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 4 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

=== End Results ===
```

### 15. `query_graph` [OK]

Arguments:
```json
{
  "query": "benchmark language preference",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "graph",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "benchmark language preference",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "b5c3883e-5981-46b9-92ee-b9ea04ce1098",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "team familiarity is higher",
      "content": "Team familiarity is higher.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:user",
        "decision-rationale",
        "database"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ee9ac288-163e-416b-9259-f16b29ce2350",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Team familiarity is higher.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.707637+00:00",
      "updated_at": "2026-04-21T04:31:53.707639+00:00",
      "access_count": 5
    },
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:ass
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=graph) ===

[NODES]
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 5 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 5 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 5 times) tags:['observed', 'speaker:assistant']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 5 times) tags:['observed', 'speaker:user']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 5 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

=== End Results ===
```

### 16. `query_graph` [OK]

Arguments:
```json
{
  "query": "database decision",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "replay",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "database decision",
  "retrieval_mode": "replay",
  "total_nodes_in_graph": 0,
  "nodes": [],
  "edges": [],
  "replay_hits": [
    {
      "score": 0.4073134768009186,
      "session_id": "s1",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "transcript_snippet": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.3280093312263489,
      "session_id": "s1",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Should we use PostgreSQL or MySQL for production?",
      "transcript_snippet": "Should we use PostgreSQL or MySQL for production?",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.32560433745384215,
      "session_id": "s2",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Actually we might switch to MySQL because team familiarity is higher.",
      "transcript_snippet": "Actually we might switch to MySQL because team familiarity is higher.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.2998324203491211,
      "session_id": "s2",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Noted: potential switch to MySQL due to team familiarity.",
      "transcript_snippet": "Noted: potential switch to MySQL due to team familiarity.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.12914017021656038,
      "session_id": "s3",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Stored preference for dark mode and JWT expiry = 15 m
... [truncated]
```

Text output:
```text
=== Memory Replay Results (6 hits) ===

[TRANSCRIPT HITS]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.407]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.328]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.326]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.300]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.129]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.100]

=== End Results ===
```

### 17. `query_graph` [OK]

Arguments:
```json
{
  "query": "latest database direction",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "replay",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "latest database direction",
  "retrieval_mode": "replay",
  "total_nodes_in_graph": 0,
  "nodes": [],
  "edges": [],
  "replay_hits": [
    {
      "score": 0.43461491062277136,
      "session_id": "s2",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Actually we might switch to MySQL because team familiarity is higher.",
      "transcript_snippet": "Actually we might switch to MySQL because team familiarity is higher.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.4284719176494437,
      "session_id": "s2",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Noted: potential switch to MySQL due to team familiarity.",
      "transcript_snippet": "Noted: potential switch to MySQL due to team familiarity.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.2783159911632538,
      "session_id": "s1",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Should we use PostgreSQL or MySQL for production?",
      "transcript_snippet": "Should we use PostgreSQL or MySQL for production?",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.27746685624122625,
      "session_id": "s1",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "transcript_snippet": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.21075695119798185,
      "session_id": "s3",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Frontend default should be dark mode and auth tok
... [truncated]
```

Text output:
```text
=== Memory Replay Results (6 hits) ===

[TRANSCRIPT HITS]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.435]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.428]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.278]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.277]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.211]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.205]

=== End Results ===
```

### 18. `query_graph` [OK]

Arguments:
```json
{
  "query": "original database choice",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "replay",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "original database choice",
  "retrieval_mode": "replay",
  "total_nodes_in_graph": 0,
  "nodes": [],
  "edges": [],
  "replay_hits": [
    {
      "score": 0.379680460691452,
      "session_id": "s2",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Actually we might switch to MySQL because team familiarity is higher.",
      "transcript_snippet": "Actually we might switch to MySQL because team familiarity is higher.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.35549002766609195,
      "session_id": "s2",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Noted: potential switch to MySQL due to team familiarity.",
      "transcript_snippet": "Noted: potential switch to MySQL due to team familiarity.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.3502491176128387,
      "session_id": "s1",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Should we use PostgreSQL or MySQL for production?",
      "transcript_snippet": "Should we use PostgreSQL or MySQL for production?",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.27690221548080446,
      "session_id": "s1",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "transcript_snippet": "Decision: use PostgreSQL for production due to reliability and team readiness.",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.10520392015576364,
      "session_id": "s3",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Stored preference for dark mode and JWT expiry
... [truncated]
```

Text output:
```text
=== Memory Replay Results (6 hits) ===

[TRANSCRIPT HITS]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.380]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.355]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.350]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.277]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.105]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.100]

=== End Results ===
```

### 19. `query_graph` [OK]

Arguments:
```json
{
  "query": "dark mode preference",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "replay",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "dark mode preference",
  "retrieval_mode": "replay",
  "total_nodes_in_graph": 0,
  "nodes": [],
  "edges": [],
  "replay_hits": [
    {
      "score": 0.5968082594871522,
      "session_id": "s3",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Stored preference for dark mode and JWT expiry = 15 minutes.",
      "transcript_snippet": "Stored preference for dark mode and JWT expiry = 15 minutes.",
      "observed_at": "2026-04-21T04:31:53.717861+00:00"
    },
    {
      "score": 0.4883306761582692,
      "session_id": "s3",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Frontend default should be dark mode and auth token expiry is 15 minutes.",
      "transcript_snippet": "Frontend default should be dark mode and auth token expiry is 15 minutes.",
      "observed_at": "2026-04-21T04:31:53.717861+00:00"
    },
    {
      "score": 0.18246011734008788,
      "session_id": "s2",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Actually we might switch to MySQL because team familiarity is higher.",
      "transcript_snippet": "Actually we might switch to MySQL because team familiarity is higher.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.1704494893550873,
      "session_id": "s1",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Should we use PostgreSQL or MySQL for production?",
      "transcript_snippet": "Should we use PostgreSQL or MySQL for production?",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.15204307913780213,
      "session_id": "s2",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Noted: potential switch to MySQL due to team familiarity.",
... [truncated]
```

Text output:
```text
=== Memory Replay Results (6 hits) ===

[TRANSCRIPT HITS]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.597]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.488]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.182]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.170]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.152]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.126]

=== End Results ===
```

### 20. `query_graph` [OK]

Arguments:
```json
{
  "query": "benchmark language preference",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "replay",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "benchmark language preference",
  "retrieval_mode": "replay",
  "total_nodes_in_graph": 0,
  "nodes": [],
  "edges": [],
  "replay_hits": [
    {
      "score": 0.24767316579818727,
      "session_id": "s2",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Actually we might switch to MySQL because team familiarity is higher.",
      "transcript_snippet": "Actually we might switch to MySQL because team familiarity is higher.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.214675931930542,
      "session_id": "s2",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Noted: potential switch to MySQL due to team familiarity.",
      "transcript_snippet": "Noted: potential switch to MySQL due to team familiarity.",
      "observed_at": "2026-04-21T04:31:53.695310+00:00"
    },
    {
      "score": 0.20507692674795788,
      "session_id": "s3",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Stored preference for dark mode and JWT expiry = 15 minutes.",
      "transcript_snippet": "Stored preference for dark mode and JWT expiry = 15 minutes.",
      "observed_at": "2026-04-21T04:31:53.717861+00:00"
    },
    {
      "score": 0.19360575079917908,
      "session_id": "s1",
      "turn_index": 0,
      "role": "user",
      "transcript_text": "Should we use PostgreSQL or MySQL for production?",
      "transcript_snippet": "Should we use PostgreSQL or MySQL for production?",
      "observed_at": "2026-04-21T04:31:30.755706+00:00"
    },
    {
      "score": 0.1749587732553482,
      "session_id": "s1",
      "turn_index": 1,
      "role": "assistant",
      "transcript_text": "Decision: use PostgreSQL for production due to reliability and team readiness
... [truncated]
```

Text output:
```text
=== Memory Replay Results (6 hits) ===

[TRANSCRIPT HITS]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.248]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.215]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.205]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.194]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.175]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.107]

=== End Results ===
```

### 21. `query_graph` [OK]

Arguments:
```json
{
  "query": "database decision",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "fusion",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "database decision",
  "retrieval_mode": "fusion",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ff838771-fcaa-48a8-b7d2-79cca78ef927",
          "session_id": "s2",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": 87,
          "source_span_end": 144,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        },
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.714789+00:00",
      "access_
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=fusion) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 6 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 6 times) tags:['observed', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 6 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 6 times) tags:['observed', 'speaker:user']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 6 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

[REPLAY HITS]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.407]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.328]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.326]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.300]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.129]
• (session: s3, turn: 0, role: user) Fro
... [truncated]
```

### 22. `query_graph` [OK]

Arguments:
```json
{
  "query": "latest database direction",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "fusion",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "latest database direction",
  "retrieval_mode": "fusion",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "e186755a-5dba-4652-bb6b-5ba6a2076156",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s3",
      "label": "JWT expiry",
      "content": "JWT tokens expire in 15 minutes.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:assistant",
        "auth"
      ],
      "source_prompt": "user: Frontend default should be dark mode and auth token expiry is 15 minutes.\nassistant: Stored preference for dark mode and JWT expiry = 15 minutes.",
      "evidence_records": [
        {
          "evidence_id": "b446ab25-65e5-45dc-845b-8cda726e21c5",
          "session_id": "s3",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "JWT tokens expire in 15 minutes.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:53.717861+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.717861+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.727399+00:00",
      "updated_at": "2026-04-21T04:31:53.727401+00:00",
      "access_count": 7
    },
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "so
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=fusion) ===

[NODES]
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 7 times) tags:['observed', 'speaker:assistant', 'auth']
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 7 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 7 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 7 times) tags:['observed', 'speaker:assistant']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 7 times) tags:['observed', 'speaker:user']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

[REPLAY HITS]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.435]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.428]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.278]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.277]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.211]
• (session: s3, turn: 1, role: a
... [truncated]
```

### 23. `query_graph` [OK]

Arguments:
```json
{
  "query": "original database choice",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "fusion",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "original database choice",
  "retrieval_mode": "fusion",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ff838771-fcaa-48a8-b7d2-79cca78ef927",
          "session_id": "s2",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": 87,
          "source_span_end": 144,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        },
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.714789+00:00",
      "
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=fusion) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 8 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 8 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 8 times) tags:['observed', 'speaker:user']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 8 times) tags:['observed', 'speaker:assistant']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 8 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

[REPLAY HITS]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.380]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.355]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.350]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.277]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.105]
• (session: s3, turn: 0, role: user) Fro
... [truncated]
```

### 24. `query_graph` [OK]

Arguments:
```json
{
  "query": "dark mode preference",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "fusion",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "dark mode preference",
  "retrieval_mode": "fusion",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ff838771-fcaa-48a8-b7d2-79cca78ef927",
          "session_id": "s2",
          "turn_index": 1,
          "source_role": "assistant",
          "source_text": "Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": 87,
          "source_span_end": 144,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        },
        {
          "evidence_id": "57b3ad25-33e6-4a8f-a5bd-fbcab60446f9",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": 6,
          "source_span_end": 75,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31:53.714789+00:00",
      "acce
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=fusion) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 9 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 9 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 9 times) tags:['observed', 'speaker:user']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 9 times) tags:['observed', 'speaker:assistant']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 9 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

[REPLAY HITS]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.597]
• (session: s3, turn: 0, role: user) Frontend default should be dark mode and auth token expiry is 15 minutes. [score=0.488]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.182]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.170]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.152]
• (session: s1, turn: 1, role: assistant) Decision
... [truncated]
```

### 25. `query_graph` [OK]

Arguments:
```json
{
  "query": "benchmark language preference",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "fusion",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "query": "benchmark language preference",
  "retrieval_mode": "fusion",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "b5c3883e-5981-46b9-92ee-b9ea04ce1098",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "team familiarity is higher",
      "content": "Team familiarity is higher.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:user",
        "decision-rationale",
        "database"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ee9ac288-163e-416b-9259-f16b29ce2350",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Team familiarity is higher.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.707637+00:00",
      "updated_at": "2026-04-21T04:31:53.707639+00:00",
      "access_count": 10
    },
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:a
... [truncated]
```

Text output:
```text
=== Memory Graph Results (5 nodes, 1 edges, mode=fusion) ===

[NODES]
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 10 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 10 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 10 times) tags:['observed', 'speaker:assistant']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 10 times) tags:['observed', 'speaker:user']
• (id: e186755a) [fact] "JWT expiry" — JWT tokens expire in 15 minutes. (created: 2026-04-21, accessed: 10 times) tags:['observed', 'speaker:assistant', 'auth']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"

[REPLAY HITS]
• (session: s2, turn: 0, role: user) Actually we might switch to MySQL because team familiarity is higher. [score=0.248]
• (session: s2, turn: 1, role: assistant) Noted: potential switch to MySQL due to team familiarity. [score=0.215]
• (session: s3, turn: 1, role: assistant) Stored preference for dark mode and JWT expiry = 15 minutes. [score=0.205]
• (session: s1, turn: 0, role: user) Should we use PostgreSQL or MySQL for production? [score=0.194]
• (session: s1, turn: 1, role: assistant) Decision: use PostgreSQL for production due to reliability and team readiness. [score=0.175]
• (session: s3, turn: 0, role: user
... [truncated]
```

### 26. `get_related` [OK]

Arguments:
```json
{
  "node_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
  "max_depth": 2
}
```

Structured content:
```json
{
  "query": "related:ec17c243-91e7-44af-8820-68d97dddfc33",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "ec17c243-91e7-44af-8820-68d97dddfc33",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "API rate limiting",
      "content": "Apply 100 req/min baseline and burst controls.",
      "node_type": "concept",
      "tags": [
        "api",
        "ops"
      ],
      "source_prompt": "",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.733889+00:00",
      "updated_at": "2026-04-21T04:31:53.733889+00:00",
      "access_count": 1
    },
    {
      "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Bench preference",
      "content": "Use Python for benchmark harness scripts.",
      "node_type": "preference",
      "tags": [
        "benchmark",
        "python"
      ],
      "source_prompt": "",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.740795+00:00",
      "updated_at": "2026-04-21T04:31:53.740795+00:00",
      "access_count": 1
    }
  ],
  "edges": [
    {
      "id": "fee765f4-8a72-434a-9a19-b98bb223a0f4",
      "tenant_id": "local-default",
      "source_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
      "target_id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "relationship": "relates_to",
      "weight": 0.72,
      "metadata": {},
      "created_at": "2026-04-21T04:31:53.748027+00:00"
    }
  ],
  "replay_hits": [],
  "fusion_hits": []
}
```

Text output:
```text
=== Memory Graph Results (2 nodes, 1 edges, mode=graph) ===

[NODES]
• (id: ec17c243) [concept] "API rate limiting" — Apply 100 req/min baseline and burst controls. (created: 2026-04-21, accessed: 1 times) tags:['api', 'ops']
• (id: 1c9a42b5) [preference] "Bench preference" — Use Python for benchmark harness scripts. (created: 2026-04-21, accessed: 1 times) tags:['benchmark', 'python']

[RELATIONSHIPS]
• "API rate limiting" --[relates_to]--> "Bench preference"

=== End Results ===
```

### 27. `get_node_history` [OK]

Arguments:
```json
{
  "node_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
  "max_depth": 2
}
```

Structured content:
```json
{
  "node": {
    "id": "ec17c243-91e7-44af-8820-68d97dddfc33",
    "tenant_id": "local-default",
    "agent_id": "",
    "project": "",
    "session_id": "",
    "label": "API rate limiting",
    "content": "Apply 100 req/min baseline and burst controls.",
    "node_type": "concept",
    "tags": [
      "api",
      "ops"
    ],
    "source_prompt": "",
    "evidence_records": [],
    "valid_from": null,
    "valid_to": null,
    "created_at": "2026-04-21T04:31:53.733889+00:00",
    "updated_at": "2026-04-21T04:31:53.733889+00:00",
    "access_count": 1
  },
  "related_nodes": [
    {
      "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Bench preference",
      "content": "Use Python for benchmark harness scripts.",
      "node_type": "preference",
      "tags": [
        "benchmark",
        "python"
      ],
      "source_prompt": "",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.740795+00:00",
      "updated_at": "2026-04-21T04:31:53.740795+00:00",
      "access_count": 2
    }
  ],
  "edges": [
    {
      "id": "fee765f4-8a72-434a-9a19-b98bb223a0f4",
      "tenant_id": "local-default",
      "source_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
      "target_id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "relationship": "relates_to",
      "weight": 0.72,
      "metadata": {},
      "created_at": "2026-04-21T04:31:53.748027+00:00"
    }
  ]
}
```

Text output:
```text
=== Node History ===
Node: "API rate limiting" [concept]
Evidence records: 0

[RELATED NODES]
• [preference] "Bench preference"
=== End Node History ===
```

### 28. `timeline` [OK]

Arguments:
```json
{
  "node_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
  "limit": 20,
  "max_depth": 2,
  "include_evidence": true
}
```

Structured content:
```json
{
  "scope": "node:ec17c243-91e7-44af-8820-68d97dddfc33",
  "items": [
    {
      "kind": "edge_relates_to",
      "timestamp": "2026-04-21T04:31:53.748027+00:00",
      "label": "API rate limiting -> Bench preference",
      "summary": "relates_to",
      "node_id": null,
      "edge_id": "fee765f4-8a72-434a-9a19-b98bb223a0f4"
    },
    {
      "kind": "node_created",
      "timestamp": "2026-04-21T04:31:53.740795+00:00",
      "label": "Bench preference",
      "summary": "Use Python for benchmark harness scripts.",
      "node_id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "edge_id": null
    },
    {
      "kind": "node_created",
      "timestamp": "2026-04-21T04:31:53.733889+00:00",
      "label": "API rate limiting",
      "summary": "Apply 100 req/min baseline and burst controls.",
      "node_id": "ec17c243-91e7-44af-8820-68d97dddfc33",
      "edge_id": null
    }
  ]
}
```

Text output:
```text
=== Timeline ===
Scope: node:ec17c243-91e7-44af-8820-68d97dddfc33
Items: 3

[ITEMS]
• 2026-04-21T04:31:53.748027+00:00 [edge_relates_to] API rate limiting -> Bench preference — relates_to edge=fee765f4
• 2026-04-21T04:31:53.740795+00:00 [node_created] Bench preference — Use Python for benchmark harness scripts. node=1c9a42b5
• 2026-04-21T04:31:53.733889+00:00 [node_created] API rate limiting — Apply 100 req/min baseline and burst controls. node=ec17c243
=== End Timeline ===
```

### 29. `timeline` [OK]

Arguments:
```json
{
  "query": "database decision",
  "limit": 20,
  "max_depth": 2,
  "include_evidence": true
}
```

Structured content:
```json
{
  "scope": "query:database decision",
  "items": [
    {
      "kind": "edge_relates_to",
      "timestamp": "2026-04-21T04:31:53.767098+00:00",
      "label": "Keep dark mode default -> Keep PostgreSQL migration scripts reviewed weekly",
      "summary": "relates_to",
      "node_id": null,
      "edge_id": "f503b774-780a-4625-aff3-1884d5c4d491"
    },
    {
      "kind": "edge_derived_from",
      "timestamp": "2026-04-21T04:31:53.766696+00:00",
      "label": "Add integration tests -> Keep dark mode default",
      "summary": "derived_from",
      "node_id": null,
      "edge_id": "111a1efc-34ff-48fe-8214-e8a0301230ba"
    },
    {
      "kind": "edge_part_of",
      "timestamp": "2026-04-21T04:31:53.766272+00:00",
      "label": "Keep PostgreSQL migration scripts reviewed weekly -> Milestone backlog",
      "summary": "part_of",
      "node_id": null,
      "edge_id": "0f36315d-0a56-4e93-a150-8ad8785be19e"
    },
    {
      "kind": "node_updated",
      "timestamp": "2026-04-21T04:31:53.762238+00:00",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "summary": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "edge_id": null
    },
    {
      "kind": "node_created",
      "timestamp": "2026-04-21T04:31:53.762237+00:00",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "summary": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "edge_id": null
    },
    {
      "kind": "edge_part_of",
      "timestamp": "2026-04-21T04:31:53.761809+00:00",
      "label": "Keep dark mode default -> Milestone backlog",
      "summary": "part_of",
      "node_id": null,
      "edge_id": "a8f884e1-3057-4
... [truncated]
```

Text output:
```text
=== Timeline ===
Scope: query:database decision
Items: 20

[ITEMS]
• 2026-04-21T04:31:53.767098+00:00 [edge_relates_to] Keep dark mode default -> Keep PostgreSQL migration scripts reviewed weekly — relates_to edge=f503b774
• 2026-04-21T04:31:53.766696+00:00 [edge_derived_from] Add integration tests -> Keep dark mode default — derived_from edge=111a1efc
• 2026-04-21T04:31:53.766272+00:00 [edge_part_of] Keep PostgreSQL migration scripts reviewed weekly -> Milestone backlog — part_of edge=0f36315d
• 2026-04-21T04:31:53.762238+00:00 [node_updated] Keep PostgreSQL migration scripts reviewed weekly — Keep PostgreSQL migration scripts reviewed weekly node=4940810b
• 2026-04-21T04:31:53.762237+00:00 [node_created] Keep PostgreSQL migration scripts reviewed weekly — Keep PostgreSQL migration scripts reviewed weekly node=4940810b
• 2026-04-21T04:31:53.761809+00:00 [edge_part_of] Keep dark mode default -> Milestone backlog — part_of edge=a8f884e1
• 2026-04-21T04:31:53.758162+00:00 [node_updated] Keep dark mode default — Keep dark mode default node=bf706135
• 2026-04-21T04:31:53.758161+00:00 [node_created] Keep dark mode default — Keep dark mode default node=bf706135
• 2026-04-21T04:31:53.757745+00:00 [edge_part_of] Add integration tests -> Milestone backlog — part_of edge=3970884b
• 2026-04-21T04:31:53.753712+00:00 [node_created] Add integration tests — Add integration tests node=00bc20c5
• 2026-04-21T04:31:53.749908+00:00 [node_updated] Milestone backlog — Milestone backlog node=f08ece06
• 2026-04-21T04:31:53.749907+00:00 [node_created] Milestone backlog — Milestone backlog node=f08ece06
• 2026-04-21T04:31:53.748027+00:00 [edge_relates_to] API rate limiting -> Bench preference — relates_to edge=fee765f4
• 2026-04-21T04:31:53.740795+00:00 [node_created] Bench preference — Use Pyth
... [truncated]
```

### 30. `list_context_scopes` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "agent_ids": [
    "demo-agent"
  ],
  "projects": [
    "waggle-demo"
  ],
  "session_ids": [
    "s1",
    "s2",
    "s3"
  ]
}
```

Text output:
```text
Known scopes: 1 agents, 1 projects, 3 sessions.
```

### 31. `list_conflicts` [OK]

Arguments:
```json
{
  "include_resolved": false,
  "limit": 20
}
```

Structured content:
```json
{
  "include_resolved": false,
  "conflicts": []
}
```

Text output:
```text
=== Conflicts ===
Include resolved: no
Conflicts: 0
No matching conflicts.
=== End Conflicts ===
```

### 32. `update_node` [OK]

Arguments:
```json
{
  "node_id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
  "content": "Use Python 3.11+ for benchmark harness scripts.",
  "tags": [
    "benchmark",
    "python",
    "updated"
  ]
}
```

Structured content:
```json
{
  "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
  "tenant_id": "local-default",
  "agent_id": "",
  "project": "",
  "session_id": "",
  "label": "Bench preference",
  "content": "Use Python 3.11+ for benchmark harness scripts.",
  "node_type": "preference",
  "tags": [
    "benchmark",
    "python",
    "updated"
  ],
  "source_prompt": "",
  "evidence_records": [],
  "valid_from": null,
  "valid_to": null,
  "created_at": "2026-04-21T04:31:53.740795+00:00",
  "updated_at": "2026-04-21T04:31:53.918166+00:00",
  "access_count": 4
}
```

Text output:
```text
Updated node 'Bench preference' (1c9a42b5-62b6-444a-a8b9-9aa49bcefa03).
```

### 33. `store_node` [OK]

Arguments:
```json
{
  "label": "Disposable note",
  "content": "Temporary node for delete verification",
  "node_type": "note",
  "tags": [
    "tmp"
  ]
}
```

Structured content:
```json
{
  "id": "3da487fb-f5f1-4b4c-b9af-cb26b138537d",
  "tenant_id": "local-default",
  "agent_id": "",
  "project": "",
  "session_id": "",
  "label": "Disposable note",
  "content": "Temporary node for delete verification",
  "node_type": "note",
  "tags": [
    "tmp"
  ],
  "source_prompt": "",
  "evidence_records": [],
  "valid_from": null,
  "valid_to": null,
  "created_at": "2026-04-21T04:31:53.926780+00:00",
  "updated_at": "2026-04-21T04:31:53.926780+00:00",
  "access_count": 0,
  "created": true,
  "dedup_reason": null,
  "similarity": null,
  "conflicts": []
}
```

Text output:
```text
Stored node 'Disposable note' with id 3da487fb-f5f1-4b4c-b9af-cb26b138537d.
```

### 34. `delete_node` [OK]

Arguments:
```json
{
  "node_id": "3da487fb-f5f1-4b4c-b9af-cb26b138537d"
}
```

Structured content:
```json
{
  "id": "3da487fb-f5f1-4b4c-b9af-cb26b138537d",
  "label": "Disposable note",
  "tenant_id": "local-default"
}
```

Text output:
```text
Deleted node 'Disposable note' (3da487fb-f5f1-4b4c-b9af-cb26b138537d) and its connected edges.
```

### 35. `prime_context` [OK]

Arguments:
```json
{
  "project": "waggle-demo",
  "agent_id": "demo-agent"
}
```

Structured content:
```json
{
  "project": "waggle-demo",
  "summary": "Prime context for project 'waggle-demo': 5 nodes (1 decision, 1 entity, 2 fact, 1 question) with 1 edges (1 depends_on) from 11 total nodes [?]",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "b5c3883e-5981-46b9-92ee-b9ea04ce1098",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "team familiarity is higher",
      "content": "Team familiarity is higher.",
      "node_type": "fact",
      "tags": [
        "observed",
        "speaker:user",
        "decision-rationale",
        "database"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "ee9ac288-163e-416b-9259-f16b29ce2350",
          "session_id": "s2",
          "turn_index": 0,
          "source_role": "user",
          "source_text": "Team familiarity is higher.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:53.695310+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.707637+00:00",
      "updated_at": "2026-04-21T04:31:53.707639+00:00",
      "access_count": 11
    },
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "t
... [truncated]
```

Text output:
```text
=== Prime Context ===
Prime context for project 'waggle-demo': 5 nodes (1 decision, 1 entity, 2 fact, 1 question) with 1 edges (1 depends_on) from 11 total nodes [?]

[NODES]
• [fact] "team familiarity is higher" — Team familiarity is higher.
• [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher.
• [fact] "JWT expiry" — JWT tokens expire in 15 minutes.
• [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness.
• [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production?

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"
=== End Prime Context ===
```

### 36. `get_topics` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "total_clusters": 6,
  "clusters": [
    {
      "cluster_id": 5,
      "label": "decomposed, decomposition-context",
      "node_count": 4,
      "top_tags": [
        "decomposed",
        "decomposition-context"
      ],
      "nodes": [
        {
          "id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
          "tenant_id": "local-default",
          "agent_id": "",
          "project": "",
          "session_id": "",
          "label": "Keep PostgreSQL migration scripts reviewed weekly",
          "content": "Keep PostgreSQL migration scripts reviewed weekly",
          "node_type": "fact",
          "tags": [
            "decomposed"
          ],
          "source_prompt": "Milestone backlog",
          "evidence_records": [],
          "valid_from": null,
          "valid_to": null,
          "created_at": "2026-04-21T04:31:53.762237+00:00",
          "updated_at": "2026-04-21T04:31:53.762238+00:00",
          "access_count": 1
        },
        {
          "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
          "tenant_id": "local-default",
          "agent_id": "",
          "project": "",
          "session_id": "",
          "label": "Keep dark mode default",
          "content": "Keep dark mode default",
          "node_type": "fact",
          "tags": [
            "decomposed"
          ],
          "source_prompt": "Milestone backlog",
          "evidence_records": [],
          "valid_from": null,
          "valid_to": null,
          "created_at": "2026-04-21T04:31:53.758161+00:00",
          "updated_at": "2026-04-21T04:31:53.758162+00:00",
          "access_count": 1
        },
        {
          "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
          "tenant_id": "local-default",
          "agent_id": "",
          "project": "",
          "ses
... [truncated]
```

Text output:
```text
=== Topics (6 clusters) ===
• Cluster 5: "decomposed, decomposition-context" — 4 nodes tags:['decomposed', 'decomposition-context']
  - [fact] "Keep PostgreSQL migration scripts reviewed weekly"
  - [fact] "Keep dark mode default"
  - [fact] "Add integration tests"
  - [concept] "Milestone backlog"
• Cluster 2: "observed, speaker:user, database" — 2 nodes tags:['observed', 'speaker:user', 'database']
  - [decision] "Database decision"
  - [fact] "team familiarity is higher"
• Cluster 3: "api, ops, benchmark" — 2 nodes tags:['api', 'ops', 'benchmark']
  - [preference] "Bench preference"
  - [concept] "API rate limiting"
• Cluster 0: "observed, speaker:user" — 1 nodes tags:['observed', 'speaker:user']
  - [question] "Should we use PostgreSQL or MySQL for production?"
• Cluster 1: "observed, speaker:assistant" — 1 nodes tags:['observed', 'speaker:assistant']
  - [entity] "Decision"
• Cluster 4: "observed, speaker:assistant, auth" — 1 nodes tags:['observed', 'speaker:assistant', 'auth']
  - [fact] "JWT expiry"
=== End Topics ===
```

### 37. `graph_diff` [OK]

Arguments:
```json
{
  "since": "24h"
}
```

Structured content:
```json
{
  "since": "24h",
  "generated_at": "2026-04-21T04:31:53.944353+00:00",
  "added_nodes": [
    {
      "id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "content": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_type": "fact",
      "tags": [
        "decomposed"
      ],
      "source_prompt": "Milestone backlog",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.762237+00:00",
      "updated_at": "2026-04-21T04:31:53.762238+00:00",
      "access_count": 1
    },
    {
      "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Keep dark mode default",
      "content": "Keep dark mode default",
      "node_type": "fact",
      "tags": [
        "decomposed"
      ],
      "source_prompt": "Milestone backlog",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.758161+00:00",
      "updated_at": "2026-04-21T04:31:53.758162+00:00",
      "access_count": 1
    },
    {
      "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
      "tenant_id": "local-default",
      "agent_id": "",
      "project": "",
      "session_id": "",
      "label": "Add integration tests",
      "content": "Add integration tests",
      "node_type": "fact",
      "tags": [
        "decomposed"
      ],
      "source_prompt": "Milestone backlog",
      "evidence_records": [],
      "valid_from": null,
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.75
... [truncated]
```

Text output:
```text
=== Graph Diff Since 24h ===
Nodes added: 11
Nodes updated: 0
Edges created: 7
Contradictions detected: 0

[ADDED NODES]
• [fact] "Keep PostgreSQL migration scripts reviewed weekly"
• [fact] "Keep dark mode default"
• [fact] "Add integration tests"
• [concept] "Milestone backlog"
• [preference] "Bench preference"
• [concept] "API rate limiting"
• [fact] "JWT expiry"
• [fact] "team familiarity is higher"
• [decision] "Database decision"
• [entity] "Decision"
• [question] "Should we use PostgreSQL or MySQL for production?"

[CREATED EDGES]
• bf706135 --[relates_to]--> 4940810b
• 00bc20c5 --[derived_from]--> bf706135
• 4940810b --[part_of]--> f08ece06
• bf706135 --[part_of]--> f08ece06
• 00bc20c5 --[part_of]--> f08ece06
• ec17c243 --[relates_to]--> 1c9a42b5
• 6da85e37 --[depends_on]--> b5c3883e
=== End Diff ===
```

### 38. `get_stats` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "total_nodes": 11,
  "total_edges": 7,
  "node_type_breakdown": {
    "fact": 5,
    "entity": 1,
    "concept": 2,
    "preference": 1,
    "decision": 1,
    "question": 1,
    "note": 0
  },
  "most_connected_nodes": [
    {
      "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
      "label": "Keep dark mode default",
      "node_type": "fact",
      "connection_count": 3
    },
    {
      "id": "f08ece06-224b-4fc4-be43-df99423f374c",
      "label": "Milestone backlog",
      "node_type": "concept",
      "connection_count": 3
    },
    {
      "id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_type": "fact",
      "connection_count": 2
    },
    {
      "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
      "label": "Add integration tests",
      "node_type": "fact",
      "connection_count": 2
    },
    {
      "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "label": "Bench preference",
      "node_type": "preference",
      "connection_count": 1
    }
  ],
  "most_recent_nodes": [
    {
      "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "label": "Bench preference",
      "node_type": "preference",
      "updated_at": "2026-04-21T04:31:53.918166+00:00"
    },
    {
      "id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_type": "fact",
      "updated_at": "2026-04-21T04:31:53.762238+00:00"
    },
    {
      "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
      "label": "Keep dark mode default",
      "node_type": "fact",
      "updated_at": "2026-04-21T04:31:53.758162+00:00"
    },
    {
      "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
      "label": "Add integration tests",
      "node_type": "fact",

... [truncated]
```

Text output:
```text
=== Memory Graph Stats ===
Total nodes: 11
Total edges: 7

[NODE TYPES]
• fact: 5
• entity: 1
• concept: 2
• preference: 1
• decision: 1
• question: 1
• note: 0

[MOST CONNECTED]
• "Keep dark mode default" (fact) — 3 connections
• "Milestone backlog" (concept) — 3 connections
• "Keep PostgreSQL migration scripts reviewed weekly" (fact) — 2 connections
• "Add integration tests" (fact) — 2 connections
• "Bench preference" (preference) — 1 connections

[MOST RECENT]
• "Bench preference" (preference) — updated 2026-04-21 04:31:53 UTC
• "Keep PostgreSQL migration scripts reviewed weekly" (fact) — updated 2026-04-21 04:31:53 UTC
• "Keep dark mode default" (fact) — updated 2026-04-21 04:31:53 UTC
• "Add integration tests" (fact) — updated 2026-04-21 04:31:53 UTC
• "Milestone backlog" (concept) — updated 2026-04-21 04:31:53 UTC
=== End Stats ===
```

### 39. `export_graph_html` [OK]

Arguments:
```json
{
  "output_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph.html",
  "include_physics": false
}
```

Structured content:
```json
{
  "output_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph.html",
  "tenant_id": "local-default",
  "total_nodes": 11,
  "total_edges": 7
}
```

Text output:
```text
Exported graph visualization to /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph.html.
```

### 40. `export_graph_backup` [OK]

Arguments:
```json
{
  "output_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json"
}
```

Structured content:
```json
{
  "output_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json",
  "tenant_id": "local-default",
  "schema_version": 3,
  "node_count": 11,
  "edge_count": 7
}
```

Text output:
```text
Exported graph backup to /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json.
```

### 41. `export_context_bundle` [OK]

Arguments:
```json
{
  "mode": "query",
  "query": "database decision and preferences",
  "project": "waggle-demo",
  "retrieval_mode": "fusion",
  "format": "both",
  "output_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/context-bundle",
  "max_nodes": 20,
  "max_depth": 2,
  "include_edges": true,
  "include_timestamps": true,
  "audience": "human"
}
```

Structured content:
```json
{
  "tenant_id": "local-default",
  "project": "waggle-demo",
  "mode": "query",
  "retrieval_mode": "fusion",
  "query": "database decision and preferences",
  "summary": "Key context: Team familiarity is higher.; Decision: use PostgreSQL for production due to reliability and team readiness.. Decisions: Actually we might switch to MySQL because team familiarity is higher. Supported by team familiarity is higher. 6 replay hits included for provenance.",
  "markdown_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/context-bundle.md",
  "json_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/context-bundle.json",
  "node_count": 5,
  "edge_count": 1,
  "render_hints": {
    "token_estimate": 1499,
    "recommended_paste_order": [
      "Paste the summary and key facts first.",
      "Paste decisions, contradictions, and timeline next.",
      "Paste appendix chunks only if the receiving AI needs more detail."
    ],
    "truncation_flags": [],
    "chunk_count": 1
  }
}
```

Text output:
```text
=== Context Bundle Export ===
Mode: query
Retrieval mode: fusion
Tenant: local-default
Project: waggle-demo
Query: database decision and preferences
Nodes: 5
Edges: 1
Markdown: /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/context-bundle.md
JSON: /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/context-bundle.json

Key context: Team familiarity is higher.; Decision: use PostgreSQL for production due to reliability and team readiness.. Decisions: Actually we might switch to MySQL because team familiarity is higher. Supported by team familiarity is higher. 6 replay hits included for provenance.
=== End Context Bundle Export ===
```

### 42. `export_markdown_vault` [OK]

Arguments:
```json
{
  "root_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault",
  "project": "waggle-demo"
}
```

Structured content:
```json
{
  "root_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault",
  "tenant_id": "local-default",
  "project": "waggle-demo",
  "node_count": 5,
  "edge_count": 1,
  "files_written": [
    "waggle-demo/fact/jwt-expiry--e186755a-5dba-4652-bb6b-5ba6a2076156.md",
    "waggle-demo/decision/database-decision--6da85e37-51a8-4c8e-9f7a-804f0f3c7738.md",
    "waggle-demo/fact/team-familiarity-is-higher--b5c3883e-5981-46b9-92ee-b9ea04ce1098.md",
    "waggle-demo/entity/decision--1eb1a89b-43b8-4a95-8e5a-e2b3fafa69e9.md",
    "waggle-demo/question/should-we-use-postgresql-or-mysql-for-production--8ad9e2f5-972a-4a2f-a14f-d009f95ef101.md"
  ]
}
```

Text output:
```text
Exported Markdown vault to /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault.
```

### 43. `import_graph_backup` [OK]

Arguments:
```json
{
  "input_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json"
}
```

Structured content:
```json
{
  "input_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json",
  "tenant_id": "local-default",
  "schema_version": 3,
  "nodes_created": 11,
  "nodes_updated": 0,
  "edges_created": 7,
  "edges_updated": 0
}
```

Text output:
```text
Imported graph backup from /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json.
```

### 44. `get_stats` [OK]

Arguments:
```json
{}
```

Structured content:
```json
{
  "total_nodes": 11,
  "total_edges": 7,
  "node_type_breakdown": {
    "fact": 5,
    "entity": 1,
    "concept": 2,
    "preference": 1,
    "decision": 1,
    "question": 1,
    "note": 0
  },
  "most_connected_nodes": [
    {
      "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
      "label": "Keep dark mode default",
      "node_type": "fact",
      "connection_count": 3
    },
    {
      "id": "f08ece06-224b-4fc4-be43-df99423f374c",
      "label": "Milestone backlog",
      "node_type": "concept",
      "connection_count": 3
    },
    {
      "id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_type": "fact",
      "connection_count": 2
    },
    {
      "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
      "label": "Add integration tests",
      "node_type": "fact",
      "connection_count": 2
    },
    {
      "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "label": "Bench preference",
      "node_type": "preference",
      "connection_count": 1
    }
  ],
  "most_recent_nodes": [
    {
      "id": "1c9a42b5-62b6-444a-a8b9-9aa49bcefa03",
      "label": "Bench preference",
      "node_type": "preference",
      "updated_at": "2026-04-21T04:31:53.918166+00:00"
    },
    {
      "id": "4940810b-2ad3-48c7-8e1e-a650e2dd3ae5",
      "label": "Keep PostgreSQL migration scripts reviewed weekly",
      "node_type": "fact",
      "updated_at": "2026-04-21T04:31:53.762238+00:00"
    },
    {
      "id": "bf706135-07c0-41ff-b740-77c28c0066d7",
      "label": "Keep dark mode default",
      "node_type": "fact",
      "updated_at": "2026-04-21T04:31:53.758162+00:00"
    },
    {
      "id": "00bc20c5-2a4b-4f38-b383-4cf2e736a9c4",
      "label": "Add integration tests",
      "node_type": "fact",

... [truncated]
```

Text output:
```text
=== Memory Graph Stats ===
Total nodes: 11
Total edges: 7

[NODE TYPES]
• fact: 5
• entity: 1
• concept: 2
• preference: 1
• decision: 1
• question: 1
• note: 0

[MOST CONNECTED]
• "Keep dark mode default" (fact) — 3 connections
• "Milestone backlog" (concept) — 3 connections
• "Keep PostgreSQL migration scripts reviewed weekly" (fact) — 2 connections
• "Add integration tests" (fact) — 2 connections
• "Bench preference" (preference) — 1 connections

[MOST RECENT]
• "Bench preference" (preference) — updated 2026-04-21 04:31:53 UTC
• "Keep PostgreSQL migration scripts reviewed weekly" (fact) — updated 2026-04-21 04:31:53 UTC
• "Keep dark mode default" (fact) — updated 2026-04-21 04:31:53 UTC
• "Add integration tests" (fact) — updated 2026-04-21 04:31:53 UTC
• "Milestone backlog" (concept) — updated 2026-04-21 04:31:53 UTC
=== End Stats ===
```

### 45. `import_markdown_vault` [OK]

Arguments:
```json
{
  "root_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault"
}
```

Structured content:
```json
{
  "root_path": "/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault",
  "tenant_id": "local-default",
  "nodes_created": 0,
  "nodes_updated": 5,
  "edges_created": 0,
  "edges_deleted": 0,
  "stub_nodes_created": 0,
  "conflicts": []
}
```

Text output:
```text
Imported Markdown vault from /Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault.
```

### 46. `query_graph` [OK]

Arguments:
```json
{
  "query": "database decision",
  "max_nodes": 10,
  "max_depth": 2,
  "retrieval_mode": "graph"
}
```

Structured content:
```json
{
  "query": "database decision",
  "retrieval_mode": "graph",
  "total_nodes_in_graph": 11,
  "nodes": [
    {
      "id": "6da85e37-51a8-4c8e-9f7a-804f0f3c7738",
      "tenant_id": "local-default",
      "agent_id": "demo-agent",
      "project": "waggle-demo",
      "session_id": "s2",
      "label": "Database decision",
      "content": "Actually we might switch to MySQL because team familiarity is higher.",
      "node_type": "decision",
      "tags": [
        "observed",
        "speaker:user",
        "database",
        "choice:mysql",
        "speaker:assistant"
      ],
      "source_prompt": "user: Actually we might switch to MySQL because team familiarity is higher.\nassistant: Noted: potential switch to MySQL due to team familiarity.",
      "evidence_records": [
        {
          "evidence_id": "421abadd-c0c4-4879-be27-6786aaa5bd6c",
          "session_id": "",
          "turn_index": 0,
          "source_role": "vault",
          "source_text": "[assistant turn 1] Noted: potential switch to MySQL due to team familiarity.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:57.820575+00:00"
        },
        {
          "evidence_id": "87222183-7f84-466b-b79c-17b81510b884",
          "session_id": "",
          "turn_index": 1,
          "source_role": "vault",
          "source_text": "[user turn 0] Actually we might switch to MySQL because team familiarity is higher.",
          "source_span_start": null,
          "source_span_end": null,
          "observed_at": "2026-04-21T04:31:57.820581+00:00"
        }
      ],
      "valid_from": "2026-04-21T04:31:53.695310+00:00",
      "valid_to": null,
      "created_at": "2026-04-21T04:31:53.703958+00:00",
      "updated_at": "2026-04-21T04:31
... [truncated]
```

Text output:
```text
=== Memory Graph Results (8 nodes, 6 edges, mode=graph) ===

[NODES]
• (id: 6da85e37) [decision] "Database decision" — Actually we might switch to MySQL because team familiarity is higher. (created: 2026-04-21, accessed: 12 times) tags:['observed', 'speaker:user', 'database', 'choice:mysql', 'speaker:assistant']
• (id: 1eb1a89b) [entity] "Decision" — Decision: use PostgreSQL for production due to reliability and team readiness. (created: 2026-04-21, accessed: 12 times) tags:['observed', 'speaker:assistant']
• (id: 8ad9e2f5) [question] "Should we use PostgreSQL or MySQL for production?" — Should we use PostgreSQL or MySQL for production? (created: 2026-04-21, accessed: 12 times) tags:['observed', 'speaker:user']
• (id: b5c3883e) [fact] "team familiarity is higher" — Team familiarity is higher. (created: 2026-04-21, accessed: 12 times) tags:['observed', 'speaker:user', 'decision-rationale', 'database']
• (id: f08ece06) [concept] "Milestone backlog" — Milestone backlog (created: 2026-04-21, accessed: 2 times) tags:['decomposition-context']
• (id: bf706135) [fact] "Keep dark mode default" — Keep dark mode default (created: 2026-04-21, accessed: 2 times) tags:['decomposed']
• (id: 4940810b) [fact] "Keep PostgreSQL migration scripts reviewed weekly" — Keep PostgreSQL migration scripts reviewed weekly (created: 2026-04-21, accessed: 2 times) tags:['decomposed']
• (id: 00bc20c5) [fact] "Add integration tests" — Add integration tests (created: 2026-04-21, accessed: 2 times) tags:['decomposed']

[RELATIONSHIPS]
• "Database decision" --[depends_on]--> "team familiarity is higher"
• "Add integration tests" --[part_of]--> "Milestone backlog"
• "Keep dark mode default" --[part_of]--> "Milestone backlog"
• "Keep PostgreSQL migration scripts reviewed weekly" --[part_of]--> "Milestone b
... [truncated]
```

## Exported Artifacts

- Graph HTML: `/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph.html`
- Graph backup JSON: `/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/graph-backup.json`
- Context bundle directory: `/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/context-bundle`
- Markdown vault directory: `/Users/abhigyanshekhar/Desktop/MCP/.tmp/comprehensive-feature-demo/exports/vault`
- Raw call log JSON: `/Users/abhigyanshekhar/Desktop/MCP/tests/artifacts/verification/2026-04-21-comprehensive-feature-demo/tool_calls.json`

## Notes

- Retrieval was tested with multiple natural-language inputs and across `graph`, `replay`, and `fusion` retrieval modes.
- Backup export/import and markdown vault export/import were validated in a fresh database instance.
- Demo used `WAGGLE_MODEL=all-MiniLM-L6-v2`.
