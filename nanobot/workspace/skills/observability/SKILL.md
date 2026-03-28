# Observability Skill

You have access to logs and traces from the LMS system via these tools:

## Available tools

- `logs_search` — search logs with LogsQL query
- `logs_error_count` — count errors for a service over a time window
- `traces_list` — list recent traces for a service
- `traces_get` — fetch a specific trace by ID

## Important: field names in VictoriaLogs

- Severity field is `severity` (values: `INFO`, `ERROR`, `WARNING`, `DEBUG`)
- Service name field is `service.name` (e.g. "Learning Management Service", "Qwen Code API")
- Example queries:
  - All errors: `severity:ERROR`
  - Backend errors: `service.name:"Learning Management Service" AND severity:ERROR`

## Strategy

### When asked "What went wrong?" or "Check system health":
1. Call `logs_error_count` with empty service to get total error count
2. Call `logs_search` with query `severity:ERROR` and limit 5 to get recent errors
3. Extract `otelTraceID` from the most recent error log entry
4. Call `traces_get` with that trace ID to get the full trace
5. Summarize concisely: what failed, which service, what error, what the trace shows

### When asked about errors in general:
- Call `logs_error_count` first, then `logs_search` for details
- Summarize findings — do not dump raw JSON
- Group errors by type and service

### For time ranges use: `1h` (last hour), `2m` (last 2 min), `30m` (last 30 min)
