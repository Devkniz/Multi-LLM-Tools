# OpenWebUI Integration

The OpenWebUI integration uses a **Filter Pipeline** — a Python middleware that intercepts user messages, detects `/command` prefixes, and injects the corresponding agent system prompt before the LLM call.

No model switching required. Type `/plan`, `/review`, `/tdd`, etc. in any chat.

---

## How It Works

```
User types:     /plan Build a REST API

Pipeline:
  1. Detects /plan → maps to agents/planner.md
  2. Reads planner.md, strips metadata header
  3. Injects system prompt as the system message
  4. Strips /plan prefix → sends "Build a REST API" to LLM
  5. LLM responds as the Planner agent

Result:         Structured implementation plan
```

Messages without a `/` prefix pass through unchanged — no performance impact on regular conversations.

---

## Installation

### Option A — Docker Compose (recommended)

Add a `pipelines` service to your `docker-compose.yml`:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      - WEBUI_SECRET_KEY=your-secret-key
    depends_on:
      - pipelines

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    ports:
      - "9099:9099"
    volumes:
      # The pipeline file
      - ./prompts/openwebui/slash_commands_pipeline.py:/app/pipelines/slash_commands_pipeline.py
      # The agents directory (system prompts)
      - ./agents:/app/pipelines/agents
    environment:
      - PIPELINES_DIR=/app/pipelines

volumes:
  open-webui:
```

Start everything:
```bash
docker compose up -d
```

---

### Option B — Manual Upload

If you already have OpenWebUI running:

1. Go to **Settings → Admin → Pipelines**
2. Set the Pipelines URL to `http://your-pipelines-server:9099`
3. Click **Upload Pipeline** and select `prompts/openwebui/slash_commands_pipeline.py`
4. Configure the `agents_dir` Valve (see below)

---

## Connect OpenWebUI to the Pipelines Server

1. Open OpenWebUI → **Settings → Admin → Pipelines**
2. Set Pipelines URL to: `http://pipelines:9099` (Docker) or `http://localhost:9099` (local)
3. Click **Save**
4. The **Multi-LLM Tools — Slash Commands** pipeline will appear automatically

---

## Enable the Pipeline for a Model

1. Go to **Settings → Admin → Models**
2. Select the model you want to use with slash commands
3. Under **Filters**, toggle on **Multi-LLM Tools — Slash Commands**
4. Save

Or enable it globally: **Settings → Admin → Pipelines → Set as Default Filter**.

---

## Configuration (Valves)

Go to **Settings → Admin → Pipelines → Multi-LLM Tools** to configure:

| Valve | Default | Description |
|-------|---------|-------------|
| `agents_dir` | `/app/pipelines/agents` | Absolute path to the `agents/` directory |
| `show_activation_banner` | `true` | Appends "Agent activated: Name" to the system prompt |
| `banner_prefix` | `**Agent activated:** ` | Text used in the activation banner |
| `passthrough_unknown` | `true` | If `true`, unknown `/commands` pass through unchanged; if `false`, returns an error |

**Important:** If you mounted the agents to a different path, update `agents_dir` accordingly.

---

## Usage Examples

### Planning a feature
```
/plan Add a real-time notification system to our Django app
```

### Code review
```
/review

def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return db.execute(query)
```

### TDD workflow
```
/tdd Implement a rate limiter middleware for Express.js
```

### Security audit
```
/security
[paste your authentication code here]
```

### Build error
```
/build
Cannot find module './utils/auth' or its corresponding type declarations.
```

### Get all commands
```
/help
```

---

## Available Commands

See [Slash Commands](Slash-Commands) for the complete reference.

---

## Troubleshooting

### "Agent not found" error
- Verify the `agents_dir` valve matches your mount path
- Check the container can read the files: `docker exec pipelines ls /app/pipelines/agents`
- File names must be exact: `planner.md`, `code-reviewer.md`, etc.

### Pipeline doesn't appear in OpenWebUI
- Confirm the Pipelines container is running: `docker ps | grep pipelines`
- Check logs: `docker logs pipelines`
- Verify the URL in Admin → Pipelines is correct

### Commands not intercepted
- Ensure the pipeline is enabled for the model you're chatting with
- Messages must start with `/` — no leading spaces

### System prompt not being applied
- OpenWebUI may have a system prompt configured for the model that conflicts
- The pipeline replaces (not appends to) existing system prompts when a command is used
- Set the model's system prompt to empty if you want agents to have full control
