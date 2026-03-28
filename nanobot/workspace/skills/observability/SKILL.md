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

- When asked about errors, call `logs_error_count` first with empty service to get total, then `logs_search` with `severity:ERROR` for details
- Summarize findings concisely, do not dump raw JSON
- If you find a trace_id in logs, call `traces_get` to fetch the full trace
