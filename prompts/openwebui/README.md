# OpenWebUI — Slash Commands Pipeline

This Filter Pipeline intercepts `/command` patterns in the chat and injects
the corresponding agent system prompt before the LLM call.

## Available Commands

| Command | Agent | Description |
|---------|-------|-------------|
| `/plan [task]` | planner | Implementation planning |
| `/architect [task]` | architect | System design |
| `/review [code]` | code-reviewer | Generic code review |
| `/tdd [feature]` | tdd-guide | Test-Driven Development |
| `/security [code]` | security-reviewer | Security audit |
| `/refactor [code]` | refactor-cleaner | Dead code cleanup |
| `/doc [task]` | doc-updater | Documentation updates |
| `/build [error]` | build-error-resolver | Fix build errors |
| `/e2e [flow]` | e2e-runner | E2E test generation |
| `/python [code]` | python-reviewer | Python review |
| `/typescript [code]` | typescript-reviewer | TS/JS review |
| `/go [code]` | go-reviewer | Go review |
| `/rust [code]` | rust-reviewer | Rust review |
| `/java [code]` | java-reviewer | Java/Spring review |
| `/kotlin [code]` | kotlin-reviewer | Kotlin/Android review |
| `/cpp [code]` | cpp-reviewer | C++ review |
| `/flutter [code]` | flutter-reviewer | Flutter/Dart review |
| `/db [query]` | database-reviewer | PostgreSQL review |
| `/loop` | loop-operator | Agent loop control |
| `/help` | — | List all commands |

Commands are **case-insensitive**. Your message follows the command:

```
/plan Build a REST API with JWT authentication
/review [paste code here]
/tdd
```

---

## Installation

### Option A — Docker Compose (recommended)

Add to your `docker-compose.yml`:

```yaml
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    # ...

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    volumes:
      # Mount the pipeline file
      - ./prompts/openwebui/slash_commands_pipeline.py:/app/pipelines/slash_commands_pipeline.py
      # Mount the agents directory so the pipeline can read system prompts
      - ./agents:/app/pipelines/agents
    environment:
      - PIPELINES_DIR=/app/pipelines
    ports:
      - "9099:9099"
```

Then in OpenWebUI → **Settings → Admin → Pipelines**:
- Set Pipelines URL to `http://pipelines:9099`
- Click **Save**

The pipeline will appear automatically.

---

### Option B — Manual upload (no Docker)

1. Open OpenWebUI → **Settings → Admin → Pipelines**
2. Click **Upload Pipeline**
3. Select `slash_commands_pipeline.py`
4. Configure the `agents_dir` valve to point to your local agents directory

---

## Configuration (Valves)

After installation, go to **Settings → Admin → Pipelines → Multi-LLM Tools**:

| Valve | Default | Description |
|-------|---------|-------------|
| `agents_dir` | `/app/pipelines/agents` | Path to the `agents/` directory |
| `show_activation_banner` | `true` | Show which agent was activated |
| `banner_prefix` | `**Agent activated:** ` | Banner text prefix |
| `passthrough_unknown` | `true` | Pass unknown `/commands` through unchanged |

---

## How It Works

```
User types:  /plan Build a REST API

Pipeline:
  1. Detects /plan → maps to agents/planner.md
  2. Reads planner.md, extracts system prompt (after ---)
  3. Injects it as the system message
  4. Strips /plan from user message → "Build a REST API"
  5. LLM responds as the Planner agent
```

The pipeline is a **Filter** (not a Pipe) — it runs transparently before every
LLM call. Messages without a `/command` prefix pass through unchanged.

---

## Activating the Pipeline for a Model

1. Go to **Settings → Admin → Models**
2. Select a model
3. Under **Filters**, enable **Multi-LLM Tools — Slash Commands**
4. Save

Or enable it globally for all models.

---

## Troubleshooting

**"Agent not found" error**
- Check that `agents_dir` valve points to the correct path
- Verify the `agents/` directory is mounted in the Docker container
- File names must match: `planner.md`, `code-reviewer.md`, etc.

**Commands not intercepted**
- Make sure the pipeline is enabled for the model you're using
- The pipeline only intercepts messages that start with `/`

**Pipeline doesn't appear in OpenWebUI**
- Confirm the Pipelines container is running: `docker ps`
- Check Pipelines URL in Admin settings (`http://pipelines:9099`)
