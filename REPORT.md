## Task 1A — Bare agent

### What is the agentic loop?

The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks.
It typically consists of these core stages:

1. Perceive — Gather information from the environment (user input, tool outputs, files, APIs, etc.)
2. Think/Reason — Process the information, plan next steps, make decisions about what actions to take
3. Act — Execute actions using available tools (file operations, API calls, code execution, web searches, etc.)
4. Observe — Receive feedback from the actions taken (success, errors, new data)
5. Repeat — Continue the loop until the goal is achieved or a stopping condition is met

### What labs are available in our LMS?

The agent explored workspace files and listed lab task descriptions from local files instead of querying the real LMS backend — it has no tools yet, so it cannot access real data.

## Task 1C — Skill prompt

### Show me the scores (without specifying a lab)

The agent listed all available labs with their scores and asked at the end: "Would you like details on a specific lab?" — demonstrating awareness that a lab parameter may be needed for deeper queries.

## Task 2A — Deployed agent

Nanobot gateway started successfully:


## Task 2B — Web client

Flutter web client accessible at http://10.93.24.128:42002/flutter.
Logged in with NANOBOT_ACCESS_KEY.

### What can you do in this system?

Nanobot listed its capabilities including file/system operations, web search, LMS skill (labs, learners, scores), memory, cron scheduling, and structured UI.

### What labs are available?

The agent returned real lab data from the LMS backend:
- Lab 01 – Products, Architecture & Roles
- Lab 02 — Run, Fix, and Deploy a Backend Service
- Lab 03 — Backend API: Explore, Debug, Implement, Deploy
- Lab 04 — Testing, Front-end, and AI Agents
- Lab 05 — Data Pipeline and Analytics Dashboard
- Lab 06 — Build Your Own Agent
- Lab 07 — Build a Client with an AI Coding Agent
- lab-08

## Task 3A — Structured logging

### Happy-path log excerpt

2026-03-28 21:00:50,420 INFO [lms_backend.main] - request_started [trace_id=52fb3e5194f3fab407e824db7372a2a7]
2026-03-28 21:00:50,421 INFO [lms_backend.auth] - auth_success [trace_id=52fb3e5194f3fab407e824db7372a2a7]
2026-03-28 21:00:50,422 INFO [lms_backend.db.items] - db_query [trace_id=52fb3e5194f3fab407e824db7372a2a7]
2026-03-28 21:00:50,537 INFO [lms_backend.main] - request_completed [trace_id=52fb3e5194f3fab407e824db7372a2a7]
GET /items/ 200 OK



### Error-path log excerpt (postgres stopped)

2026-03-28 21:13:25,824 INFO [lms_backend.main] - request_started [trace_id=739354c750a0275a3a0051601f36bdf6]
2026-03-28 21:13:25,825 INFO [lms_backend.auth] - auth_success [trace_id=739354c750a0275a3a0051601f36bdf6]
2026-03-28 21:13:25,825 INFO [lms_backend.db.items] - db_query [trace_id=739354c750a0275a3a0051601f36bdf6]
2026-03-28 21:13:26,570 ERROR [lms_backend.db.items] - db_query [trace_id=739354c750a0275a3a0051601f36bdf6]
2026-03-28 21:13:26,570 WARNING [lms_backend.routers.items] - items_list_failed_as_not_found
2026-03-28 21:13:26,816 INFO [lms_backend.main] - request_completed [trace_id=739354c750a0275a3a0051601f36bdf6]
GET /items/ 404 Not Found



### VictoriaLogs screenshot
[screenshot added]

## Task 3B — Traces
[screenshots added]

## Task 3C — Observability MCP tools

### Normal conditions: Any errors in the last hour?

"There are 13 ERROR log entries across all services in the last 1 hour."

### Error details after postgres was stopped:

The agent found and analyzed all errors:
- Primary issue: Database connection failures (DNS resolution failure - postgres stopped)
- Secondary issue: Unique constraint violation from earlier ETL sync
- All errors from Learning Management Service
- Agent correctly identified the root cause and recommended actions

Both responses demonstrate the agent can query VictoriaLogs and summarize findings.

## Task 4A — Multi-step investigation

With PostgreSQL stopped, the agent investigated and found:
- Primary issue: Database connectivity failure (DNS resolution - postgres stopped)
- 10+ consecutive db_query errors from Learning Management Service
- Agent chained logs_error_count → logs_search → traces_get automatically
- Correctly identified root cause and recommended actions

## Task 4B — Proactive health check

Agent set up heartbeat-based health monitoring via HEARTBEAT.md.

First check (healthy): 0 errors detected, system looks healthy.

Proactive report after failure (23:18 UTC):
- Status: UNHEALTHY
- Error count (last 2 min): 1 ERROR in LMS
- Root cause: Database connectivity failure [Errno -2] Name or service not known
- Trace ID: 92a4e5ff346807200ea06d4883da66c7
- Agent correctly diagnosed and reported without being asked
