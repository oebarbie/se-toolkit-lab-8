"""MCP server exposing VictoriaLogs and VictoriaTraces as tools."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field


VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://localhost:9428")
VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://localhost:10428")


class LogsSearchArgs(BaseModel):
    query: str = Field(description="LogsQL query, e.g. 'severity:ERROR' or 'service.name:\"Learning Management Service\" AND severity:ERROR'")
    limit: int = Field(default=20, ge=1, le=200, description="Max log entries to return")
    start: str = Field(default="1h", description="Time range start, e.g. '1h', '30m', '24h'")


class LogsErrorCountArgs(BaseModel):
    service: str = Field(default="", description="Service name, e.g. 'Learning Management Service'. Empty = all services.")
    start: str = Field(default="1h", description="Time window, e.g. '1h', '30m'")


class TracesListArgs(BaseModel):
    service: str = Field(default="Learning Management Service", description="Service name to list traces for")
    limit: int = Field(default=10, ge=1, le=50, description="Max traces to return")


class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


async def logs_search(args: LogsSearchArgs) -> str:
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    params = {"query": args.query, "limit": args.limit, "start": f"now-{args.start}"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        lines = [line for line in resp.text.strip().split("\n") if line]
        entries = [json.loads(line) for line in lines[:args.limit]]
        return json.dumps(entries, ensure_ascii=False, indent=2)


async def logs_error_count(args: LogsErrorCountArgs) -> str:
    if args.service:
        query = f'service.name:"{args.service}" AND severity:ERROR'
    else:
        query = "severity:ERROR"
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    params = {"query": query, "limit": 200, "start": f"now-{args.start}"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        lines = [line for line in resp.text.strip().split("\n") if line]
        count = len([l for l in lines if l])
        return json.dumps({"error_count": count, "service": args.service or "all", "window": args.start})


async def traces_list(args: TracesListArgs) -> str:
    url = f"{VICTORIATRACES_URL}/jaeger/api/traces"
    params = {"service": args.service, "limit": args.limit}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])
        summary = [
            {
                "traceID": t.get("traceID"),
                "spans": len(t.get("spans", [])),
                "duration_ms": round(t.get("spans", [{}])[0].get("duration", 0) / 1000, 2) if t.get("spans") else 0,
            }
            for t in traces
        ]
        return json.dumps(summary, ensure_ascii=False, indent=2)


async def traces_get(args: TracesGetArgs) -> str:
    url = f"{VICTORIATRACES_URL}/jaeger/api/traces/{args.trace_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return json.dumps(resp.json(), ensure_ascii=False, indent=2)


TOOLS = [
    Tool(name="logs_search", description="Search logs in VictoriaLogs using a LogsQL query. Use severity:ERROR for errors.", inputSchema=LogsSearchArgs.model_json_schema()),
    Tool(name="logs_error_count", description="Count ERROR log entries for a service over a time window.", inputSchema=LogsErrorCountArgs.model_json_schema()),
    Tool(name="traces_list", description="List recent traces for a service from VictoriaTraces.", inputSchema=TracesListArgs.model_json_schema()),
    Tool(name="traces_get", description="Fetch a specific trace by ID from VictoriaTraces.", inputSchema=TracesGetArgs.model_json_schema()),
]

HANDLERS: dict[str, Any] = {
    "logs_search": logs_search,
    "logs_error_count": logs_error_count,
    "traces_list": traces_list,
    "traces_get": traces_get,
}


async def main() -> None:
    server = Server("obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        handler = HANDLERS.get(name)
        if handler is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            model_class = {"logs_search": LogsSearchArgs, "logs_error_count": LogsErrorCountArgs, "traces_list": TracesListArgs, "traces_get": TracesGetArgs}[name]
            args = model_class.model_validate(arguments or {})
            result = await handler(args)
            return [TextContent(type="text", text=result)]
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool

    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
