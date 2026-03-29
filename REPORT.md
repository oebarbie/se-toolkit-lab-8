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

## Task 1B — Agent with LMS tools

### What labs are available?

The agent returned real lab names from the backend using MCP tools:
1. Lab 01 - Products, Architecture and Roles
2. Lab 02 - Run, Fix, and Deploy a Backend Service
3. Lab 03 - Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 - Testing, Front-end, and AI Agents
5. Lab 05 - Data Pipeline and Analytics Dashboard
6. Lab 06 - Build Your Own Agent
7. Lab 07 - Build a Client with an AI Coding Agent
8. lab-08

### Describe the architecture of the LMS system

The LMS is a microservices-based platform. Key services: Caddy (reverse proxy), LMS Backend (FastAPI), PostgreSQL, Qwen Code API (LLM proxy), nanobot (AI agent framework), OTel Collector, VictoriaLogs, VictoriaTraces. All services communicate over the lms-network Docker network.

## Task 1C — Skill prompt

### Show me the scores (without specifying a lab)

The agent listed all available labs with their scores and asked at the end: "Would you like details on a specific lab?" demonstrating awareness that a lab parameter may be needed for deeper queries.

## Task 2A — Deployed agent

Nanobot gateway started successfully. Key log lines:

Starting nanobot gateway version 0.1.4.post6 on port 18790
WebChat channel enabled
Channels enabled: webchat
MCP server lms: connected, 9 tools registered
Agent loop started

## Task 2B — Web client

Flutter web client accessible at http://10.93.24.128:42002/flutter.
Logged in with NANOBOT_ACCESS_KEY.

### What can you do in this system?

Nanobot listed its capabilities including file/system operations, web search, LMS skill (labs, learners, scores), memory, cron scheduling, and structured UI.

### What labs are available?

The agent returned real lab data from the LMS backend including all 8 labs from Lab 01 to lab-08.

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

There are 13 ERROR log entries across all services in the last 1 hour.

### Error details after postgres was stopped

The agent found and analyzed all errors. Primary issue: Database connection failures (DNS resolution failure - postgres stopped). Secondary issue: Unique constraint violation from earlier ETL sync. All errors from Learning Management Service. Agent correctly identified the root cause and recommended actions.

## Task 4A — Multi-step investigation

With PostgreSQL stopped, the agent investigated and found the primary issue was database connectivity failure. The agent chained logs_error_count then logs_search then traces_get automatically and correctly identified the root cause and recommended actions.

## Task 4B — Proactive health check

Agent set up heartbeat-based health monitoring via HEARTBEAT.md.

First check (healthy): 0 errors detected, system looks healthy.

Proactive report after failure at 23:18 UTC:
Status: UNHEALTHY
Error count last 2 min: 1 ERROR in LMS
Root cause: Database connectivity failure [Errno -2] Name or service not known
Trace ID: 92a4e5ff346807200ea06d4883da66c7
Agent correctly diagnosed and reported without being asked.

## Task 4C — Bug fix and recovery

### Root cause

The planted bug was in backend/src/lms_backend/routers/items.py. When a database exception occurred, the get_items endpoint raised HTTP 404 Not Found with "Items not found" instead of HTTP 500 Internal Server Error, hiding the real database error.

### Fix

Changed status_code from HTTP_404_NOT_FOUND to HTTP_500_INTERNAL_SERVER_ERROR and detail from "Items not found" to "Internal server error".

### Post-fix failure check

After redeploy with postgres stopped, agent reported HTTP 500 and correctly identified database DNS resolution failure with 4 errors in last 2 min from Learning Management Service.

### Healthy follow-up

After postgres restarted, health check at 23:38 UTC showed 0 errors detected and system HEALTHY.

