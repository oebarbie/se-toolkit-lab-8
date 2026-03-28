import json
import os

config_path = "/app/nanobot/config.json"
workspace_path = "/app/nanobot/workspace"

with open(config_path) as f:
    config = json.load(f)

config["providers"]["custom"]["apiKey"] = os.environ.get("LLM_API_KEY", "")
config["providers"]["custom"]["apiBase"] = os.environ.get("LLM_API_BASE_URL", "")
config["agents"]["defaults"]["model"] = os.environ.get("LLM_API_MODEL", "coder-model")
config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))

config["channels"]["webchat"] = {
    "enabled": True,
    "host": os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"),
    "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
    "accessKey": os.environ.get("NANOBOT_ACCESS_KEY", ""),
    "allow_from": ["*"]
}

config["tools"]["mcpServers"]["lms"] = {
    "command": "/app/.venv/bin/python",
    "args": ["-m", "mcp_lms"],
    "env": {
        "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", ""),
        "NANOBOT_LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", "")
    }
}

config["tools"]["mcpServers"]["obs"] = {
    "command": "/app/.venv/bin/python",
    "args": ["-m", "mcp_obs"],
    "env": {
        "NANOBOT_VICTORIALOGS_URL": os.environ.get("NANOBOT_VICTORIALOGS_URL", ""),
        "NANOBOT_VICTORIATRACES_URL": os.environ.get("NANOBOT_VICTORIATRACES_URL", "")
    }
}

resolved_path = "/tmp/config.resolved.json"
with open(resolved_path, "w") as f:
    json.dump(config, f, indent=2)

os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace_path])
