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
