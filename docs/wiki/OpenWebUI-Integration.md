# OpenWebUI Integration

The OpenWebUI integration uses a **native Function Filter** — a Python component that intercepts user messages, detects `/command` prefixes, and injects the corresponding agent system prompt before the LLM call.

**No separate service required.** No Pipelines server, no Docker networking, no complexity. Just upload and use. Perfect for closed enterprise networks.

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

## Installation

### Step 1: Locate the Filter File

The filter is located at:
```
prompts/openwebui/slash_commands_filter.py
```

### Step 2: Upload to OpenWebUI

1. Open OpenWebUI → **Settings → Admin → Functions**
2. Click **Upload Function**
3. Select `prompts/openwebui/slash_commands_filter.py`
4. Click **Upload**

### Step 3: Configure the Filter

After upload, you'll see **"Multi-LLM Tools — Slash Commands"** in your Functions list.

Click the **gear icon** next to it to configure:

| Valve | Default | What to set |
|-------|---------|-------------|
| `agents_dir` | `/app/pipelines/agents` | Path to your `agents/` directory |
| `show_activation_banner` | `true` | (optional) show agent name |
| `banner_prefix` | `**Agent activated:** ` | (optional) customize banner |
| `passthrough_unknown` | `true` | (optional) pass unknown commands |

**Most important:** Set `agents_dir` to your local agents directory. Examples:
- Docker: `/app/pipelines/agents` (if mounted)
- Local: `/home/user/Multi-LLM-Tools/agents`
- WSL: `/mnt/c/Users/YourName/Multi-LLM-Tools/agents`

### Step 4: Use It

Type any command in the chat:

```
/plan Build a REST API with JWT authentication
/review [paste code]
/tdd
/security
/help
```

That's it!

---

## For Docker Compose Users

If you're running OpenWebUI in Docker, mount the `agents/` directory:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
      # Mount agents for the filter to read
      - ./agents:/app/pipelines/agents
    environment:
      - WEBUI_SECRET_KEY=your-secret-key

volumes:
  open-webui:
```

Then:
1. Start: `docker compose up -d`
2. Upload the filter via **Settings → Admin → Functions**
3. Set `agents_dir` to `/app/pipelines/agents` (the mounted path)
4. Done!

---

## Available Commands

See [Slash Commands](Slash-Commands) for the complete reference.

Quick overview:

```
/plan [task]       → Implementation planning
/architect [task]  → System design
/review [code]     → Code review
/tdd [feature]     → Test-Driven Development
/security [code]   → Security audit
/refactor [code]   → Code cleanup
/doc [task]        → Documentation
/build [error]     → Fix build errors
/e2e [flow]        → E2E tests
/help              → List all commands

Language-specific:
/python /typescript /go /rust /java /kotlin /cpp /flutter /db
```

---

## Troubleshooting

### "Agent not found" error

**Cause:** The filter can't find the agent files.

**Fix:**
1. Verify `agents_dir` valve points to your agents directory
2. Check files exist: `ls agents/planner.md agents/code-reviewer.md` etc.
3. File names must match exactly (case-sensitive): `planner.md`, `code-reviewer.md`, etc.

### Commands not intercepted

**Cause:** The filter isn't enabled or message format is wrong.

**Fix:**
1. Verify the filter is toggled on (it should be by default)
2. Ensure messages start with `/` with no leading spaces
3. Type `/help` to confirm it's working

### Filter doesn't appear in Functions list

**Cause:** Upload failed or filter crashed on load.

**Fix:**
1. Refresh the page (Ctrl+Shift+R)
2. Check browser console for errors (F12)
3. Try uploading again
4. Verify Python syntax is valid (no typos in filter file)

### System prompt not being applied

**Cause:** OpenWebUI has a model-level system prompt that overrides ours.

**Fix:**
1. Go to **Settings → Admin → Models**
2. Select the model you're using
3. Clear the "System Prompt" field (or set it to empty)
4. The filter will now have full control

---

## Why This Approach?

This is a **native OpenWebUI Function**, not a separate Pipelines server. Benefits:

### ✅ Simpler Architecture
- Single container (OpenWebUI)
- No separate Pipelines service (port 9099)
- No inter-service communication overhead

### ✅ Perfect for Enterprise Networks
- No Docker networking complexity
- No firewall rules between services
- Works in completely closed networks
- Easier to deploy and maintain

### ✅ Instant Activation
- Upload, configure, use
- No Docker Compose or infrastructure changes
- Works with managed OpenWebUI instances
- Ideal for SaaS deployments

### ✅ Better Reliability
- Single point of failure (unavoidable)
- Fewer logs to parse and debug
- OpenWebUI handles all lifecycle management

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

- [Slash Commands reference](Slash-Commands)
- [OpenWebUI README](../../../prompts/openwebui/README.md)
- [Multi-LLM Tools documentation](../../README.md)
