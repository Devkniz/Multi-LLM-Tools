# OpenWebUI — Slash Commands Filter

This **native OpenWebUI Function** intercepts `/command` patterns in the chat and injects the corresponding agent system prompt before the LLM call.

No separate Pipelines server needed. No Docker configuration required. Just upload and use.

Type `/plan`, `/review`, `/tdd`, etc. in any chat and Claude Code agents take over.

---

## Quick Installation

### For OpenWebUI users:

1. Go to **Settings → Admin → Functions**
2. Click **Upload Function**
3. Select `slash_commands_filter.py` from `prompts/openwebui/`
4. Configure the `agents_dir` valve (usually `/app/pipelines/agents` for Docker, or your local `agents/` path)
5. Done! Start typing `/plan`, `/review`, etc.

---

## How It Works

```
User types:     /plan Build a REST API

Filter:
  1. Detects /plan → maps to agents/planner.md
  2. Reads planner.md, strips metadata header
  3. Injects system prompt as the system message
  4. Strips /plan prefix → sends "Build a REST API" to LLM
  5. LLM responds as the Planner agent

Result:         Structured implementation plan
```

Messages without a `/` prefix pass through unchanged — no performance impact on regular conversations.

---

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

## Configuration (Valves)

After uploading, click the filter's gear icon to configure:

| Valve | Default | Description |
|-------|---------|-------------|
| `agents_dir` | `/app/pipelines/agents` | Path to the `agents/` directory |
| `show_activation_banner` | `true` | Show which agent was activated |
| `banner_prefix` | `**Agent activated:** ` | Banner text prefix |
| `passthrough_unknown` | `true` | Pass unknown `/commands` through unchanged |

---

## For Docker Compose Users

Add to your `docker-compose.yml`:

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

volumes:
  open-webui:
```

Then:

1. Start OpenWebUI: `docker compose up -d`
2. Go to **Settings → Admin → Functions**
3. Upload `slash_commands_filter.py`
4. Set `agents_dir` to your local `agents/` path (e.g., `/home/user/Multi-LLM-Tools/agents`)
5. Done!

---

## Troubleshooting

**"Agent not found" error**
- Check the `agents_dir` valve points to the correct path
- Verify agent files exist: `ls agents/planner.md agents/code-reviewer.md` etc.
- File names must be exact: `planner.md`, `code-reviewer.md`, etc.

**Commands not working**
- Ensure the filter is toggled on (should be by default)
- Messages must start with `/` — no leading spaces
- Type `/help` to list all commands

**Filter doesn't appear in Functions list**
- Refresh the page (Ctrl+Shift+R)
- Check browser console for errors
- Try uploading again

---

## Why a Function, Not a Pipeline?

Our integration was originally a **Pipelines server** (port 9099) — but OpenWebUI's official guidance is clear:

> *"If your goal is simply to add support for additional providers or basic filters, you likely don't need Pipelines. OpenWebUI Functions are built-in, much more convenient, and easier to configure."*

Our use case (system prompt injection based on slash commands) fits perfectly in a **Function**. Benefits:

- ✅ **No separate service** — runs inside OpenWebUI
- ✅ **Instant activation** — just upload, no Docker config
- ✅ **Ideal for closed networks** — no inter-service communication
- ✅ **Easier maintenance** — one container, simpler logs
- ✅ **Better for enterprises** — less infrastructure overhead

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

## See Also

- [Slash Commands reference](../../docs/wiki/Slash-Commands.md)
- [OpenWebUI Integration guide](../../docs/wiki/OpenWebUI-Integration.md)
- [Multi-LLM Tools documentation](../../README.md)
