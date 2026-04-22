# Docker Setup — OpenWebUI + Ollama + Qwen 2.5

## Choose Your Setup

You have **two options** — pick the one that matches your situation:

### 📦 **Option 1: Everything in Docker** (Recommended for teams)
Use `docker-compose.yml`

**Best for:**
- Team deployments (collaborators just need Docker)
- Closed enterprise networks
- Reproducible, containerized environments
- CI/CD pipelines

**Requirements:** Docker & Docker Compose only

---

### 💻 **Option 2: Local Ollama + Docker OpenWebUI** (For individual dev)
Use `docker-compose.local.yml`

**Best for:**
- Individual development on macOS/Linux
- You already have Ollama running locally (e.g., via Brew)
- Faster iteration (no container networking overhead)
- Lower resource usage (no separate Ollama container)

**Requirements:** Docker + local Ollama running

---

## Option 1: Everything in Docker

### Prerequisites

- Docker & Docker Compose installed
- 16 GB RAM (for qwen2.5-coder:14b) or 24+ GB for the 32b version
- Optional: NVIDIA GPU with CUDA support

### Quick Start

```bash
# 1. Configure environment (optional)
cp .env.example .env

# 2. Start the stack
docker compose up -d

# 3. Wait for services to be healthy
docker compose logs -f
# Should show: "OpenWebUI is running on http://0.0.0.0:8080"

# 4. Pull Qwen 2.5 model (inside the container)
docker exec ollama ollama pull qwen2.5-coder:14b
# Or other sizes: 7b (8GB RAM), 32b (24GB+ RAM)

# 5. Verify model was pulled
docker exec ollama ollama list
```

### Setup in OpenWebUI

1. Open http://localhost:3000
2. Create admin account (first user becomes admin)
3. Check Ollama is detected:
   - **Settings → Admin → Models**
   - Should show qwen2.5-coder:14b

### Upload the Function Filter

1. Go to **Settings → Admin → Functions**
2. Click **Upload Function**
3. Select `prompts/openwebui/slash_commands_filter.py`
4. Click the **gear icon** on the filter
5. Set `agents_dir` to `/app/pipelines/agents`
6. Toggle the filter **ON**

### Enable Filter for Your Model

1. Go to **Settings → Admin → Models**
2. Select `qwen2.5-coder:14b`
3. Click **Filters** tab
4. Toggle **Multi-LLM Tools — Slash Commands** → **ON**
5. Save

### Test It!

```
/help
```

Should see all 27+ agent commands.

```
/plan Build a REST API with JWT authentication
```

---

## Option 2: Local Ollama + Docker OpenWebUI

### Prerequisites

**On your Mac:**
```bash
# Install Ollama (if not already done)
brew install ollama

# Start Ollama in the background
ollama serve &

# Pull your model
ollama pull qwen2.5-coder:14b

# Verify it's running
curl http://localhost:11434/api/tags
```

**Then use Docker:**
```bash
# (Docker still needed for OpenWebUI only)
docker compose -f docker-compose.local.yml up -d
```

### How It Works

- **Ollama** runs on your Mac locally (`http://localhost:11434`)
- **OpenWebUI** runs in Docker but connects to your local Ollama via `host.docker.internal`
- No separate Ollama container needed

### Setup in OpenWebUI

Same as Option 1, but Ollama models already exist (no need to pull again).

1. Open http://localhost:3000
2. Create admin account
3. Verify Ollama is detected:
   - **Settings → Admin → Models**
   - Should show qwen2.5-coder:14b from your local Ollama
4. Upload Function Filter (same steps as Option 1)
5. Enable for your model (same steps as Option 1)
6. Test: `/help`, `/plan`, etc.

### Stop

```bash
# Stop OpenWebUI container
docker compose -f docker-compose.local.yml down

# Stop local Ollama (if running in background)
pkill ollama

# Restart Ollama
ollama serve &
```

---

## Comparison Table

| Aspect | Option 1 (Docker) | Option 2 (Local) |
|--------|---|---|
| **Setup complexity** | 1 command | 2 services |
| **For collaborators** | ✅ Perfect | ❌ Each needs Ollama |
| **Disk usage** | ~20 GB (Ollama container) | ~15 GB (just models) |
| **Performance** | Good | Slightly faster (no network layer) |
| **Portability** | ✅ Works everywhere | ⚠️ Mac/Linux only |
| **Reproducibility** | ✅ Identical across machines | ❌ Depends on local setup |

---

## Troubleshooting

### "Model not found" error

**Option 1:** Pull inside container:
```bash
docker exec ollama ollama pull qwen2.5-coder:14b
```

**Option 2:** Pull locally:
```bash
ollama pull qwen2.5-coder:14b
```

### "Agent not found" error

Verify agents directory is mounted:

**Option 1:**
```bash
docker exec open-webui ls /app/pipelines/agents
```

**Option 2:**
```bash
docker exec open-webui-local ls /app/pipelines/agents
```

Should show: `planner.md`, `code-reviewer.md`, etc.

### OpenWebUI can't reach Ollama (Option 2)

Make sure:
1. Ollama is running locally: `ollama serve &`
2. You're using `docker-compose.local.yml`
3. Host is macOS (other OS would need different hostname)

### Qwen 2.5 ignores system prompt

Increase context window in OpenWebUI:
1. **Settings → Admin → Models → qwen2.5-coder:14b**
2. Click **Advanced**
3. Set **Context Length** to `8192` or `16384`
4. Save

---

## Useful Commands

### Option 1 (Full Docker)

```bash
docker compose up -d              # Start
docker compose down               # Stop
docker compose logs -f            # View logs
docker compose restart            # Restart
docker exec ollama ollama list    # List models
docker exec ollama ollama pull MODELNAME  # Pull new model
```

### Option 2 (Local Ollama)

```bash
docker compose -f docker-compose.local.yml up -d
docker compose -f docker-compose.local.yml down
ollama serve &                    # Start local Ollama
ollama list                       # List local models
ollama pull MODELNAME             # Pull to local Ollama
```

---

## For Teams / Production

**Use Option 1** with these additions:

1. **Change `WEBUI_SECRET_KEY`** to a random string
2. **Add a reverse proxy** (nginx) with HTTPS
3. **Set resource limits** in `deploy` section
4. **Use persistent storage** on a network volume (NFS, etc.)
5. **Document the setup** in your team's deployment guide

Example with resource limits:
```yaml
services:
  open-webui:
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

See [`docs/wiki/OpenWebUI-Integration.md`](docs/wiki/OpenWebUI-Integration.md) for more details.
