# Docker Setup — OpenWebUI + Ollama + Qwen 2.5

This is the **quickest way to get everything running** for a closed enterprise network.

## Prerequisites

- Docker & Docker Compose installed
- 16 GB RAM (for qwen2.5-coder:14b) or 24+ GB for the 32b version
- Optional: NVIDIA GPU with CUDA support (uncomment GPU sections in `docker-compose.yml`)

## Quick Start

### 1. Configure Environment

```bash
# Copy the example env file and customize if needed
cp .env.example .env

# Edit .env if you want to change ports or add a strong secret key
# nano .env
```

### 2. Start the Stack

```bash
docker compose up -d
```

This starts:
- **Ollama** on `http://localhost:11434`
- **OpenWebUI** on `http://localhost:3000`

Wait for containers to be healthy:
```bash
docker compose logs -f
```

Look for: `OpenWebUI is running on http://0.0.0.0:8080`

### 3. First Time Setup in OpenWebUI

1. Open http://localhost:3000
2. Create admin account (first user becomes admin)
3. Confirm Ollama is detected:
   - **Settings → Admin → Models**
   - Should show Ollama models available (none initially, until you pull one)

### 4. Pull Qwen 2.5 Model

Choose your size based on available VRAM:

```bash
# 7B — 8 GB VRAM, fast
docker exec ollama ollama pull qwen2.5-coder:7b

# 14B — 16 GB VRAM, balanced (recommended)
docker exec ollama ollama pull qwen2.5-coder:14b

# 32B — 24 GB VRAM, best quality
docker exec ollama ollama pull qwen2.5-coder:32b
```

Verify:
```bash
docker exec ollama ollama list
```

### 5. Upload the Function Filter

1. Go to **Settings → Admin → Functions**
2. Click **Upload Function**
3. Select `prompts/openwebui/slash_commands_filter.py`
4. Wait for upload to complete
5. Click the **gear icon** on the filter
6. Set `agents_dir` to `/app/pipelines/agents` (this is the mount path)
7. Toggle the filter **ON**

### 6. Enable Filter for Your Model

1. Go to **Settings → Admin → Models**
2. Select `qwen2.5-coder:14b` (or your chosen size)
3. Click **Filters** tab
4. Toggle **Multi-LLM Tools — Slash Commands** → **ON**
5. Save

### 7. Test It!

Start a new chat:
- Model: `qwen2.5-coder:14b`
- Type: `/help`
- Should see all 27+ agent commands

Try a command:
```
/plan Build a REST API with JWT authentication
```

---

## Troubleshooting

### "Model not found" error

The model hasn't been pulled yet. Run:
```bash
docker exec ollama ollama pull qwen2.5-coder:14b
```

### "Agent not found" error

The Function can't read the agents directory. Verify:
```bash
docker exec open-webui ls /app/pipelines/agents
```

Should show files like: `planner.md`, `code-reviewer.md`, etc.

If empty or error, the mount failed. Check `docker-compose.yml` line with:
```yaml
- ./agents:/app/pipelines/agents:ro
```

### Function not showing up in Admin → Functions

The upload may have failed. Check logs:
```bash
docker compose logs open-webui | tail -50
```

### Qwen 2.5 seems to ignore the system prompt

Context window might be too small. Increase it:
1. **Settings → Admin → Models → qwen2.5-coder:14b**
2. Click **Advanced**
3. Set **Context Length** to `8192` or `16384`
4. Save

---

## Useful Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f open-webui

# Stop everything
docker compose down

# Stop but keep data
docker compose stop

# Restart
docker compose restart

# Access Ollama CLI inside container
docker exec -it ollama ollama list
docker exec -it ollama ollama run qwen2.5-coder:14b "Your prompt here"

# Pull additional models
docker exec ollama ollama pull deepseek-coder-v2:16b
```

---

## File Structure

```
.
├── docker-compose.yml          ← Main configuration
├── .env.example                ← Environment variables template
├── .env                        ← Your local config (created by you, not pushed)
├── agents/                     ← Agent system prompts (mounted into OpenWebUI)
├── prompts/openwebui/
│   └── slash_commands_filter.py ← The Function to upload
└── docs/wiki/
    └── OpenWebUI-Integration.md ← Full setup guide
```

---

## Production Deployment

For a real production setup:

1. **Change `WEBUI_SECRET_KEY`** to a strong random string
2. **Use environment files** (`.env`) for secrets, not in `docker-compose.yml`
3. **Mount volumes on persistent storage** (not local directories)
4. **Add a reverse proxy** (nginx) in front with HTTPS
5. **Set resource limits** in the `deploy` section
6. **Use a network policy** to restrict inter-container communication

Example advanced setup:
```yaml
services:
  open-webui:
    ...
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

---

## Offline Operation Verification

This stack is **fully offline** once running:

- ✅ Ollama: runs locally, no API calls
- ✅ OpenWebUI: runs locally, no telemetry
- ✅ Function Filter: reads local files only
- ✅ All 27 agents: no internet needed

Perfect for:
- Enterprise closed networks
- Air-gapped environments
- Regulated industries (GDPR, HIPAA, SOC2)

---

See [`docs/wiki/OpenWebUI-Integration.md`](docs/wiki/OpenWebUI-Integration.md) for more details.
