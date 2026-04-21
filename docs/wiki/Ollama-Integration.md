# Ollama Integration

With Ollama, agents are used by creating **dedicated models** with baked-in system prompts via Modelfiles.  
You switch agent by switching model — no slash commands, but each model behaves as a specialized agent.

---

## Available Modelfiles

| Modelfile | Agent | Description |
|-----------|-------|-------------|
| `planner.Modelfile` | planner | Implementation planning |
| `architect.Modelfile` | architect | System design |
| `code-reviewer.Modelfile` | code-reviewer | Code review |
| `tdd-guide.Modelfile` | tdd-guide | Test-Driven Development |
| `security-reviewer.Modelfile` | security-reviewer | Security audit |
| `build-error-resolver.Modelfile` | build-error-resolver | Build error fixes |
| `refactor-cleaner.Modelfile` | refactor-cleaner | Dead code cleanup |

---

## Setup

### 1. Choose a base model

Edit the Modelfile for each agent you want. The `FROM` line sets the base model:

```dockerfile
# prompts/ollama/planner.Modelfile
FROM qwen2.5-coder:32b   # ← change this to your model

SYSTEM """
You are an expert planning specialist...
"""
```

Recommended base models by tier:

| Tier | Agent examples | Recommended model |
|------|---------------|-------------------|
| best | planner, architect | `qwen2.5-coder:32b`, `deepseek-coder-v2:33b` |
| mid  | code-reviewer, tdd-guide, security-reviewer | `qwen2.5-coder:14b`, `codellama:13b` |
| fast | build-error-resolver, doc-updater | `qwen2.5-coder:7b`, `codellama:7b` |

### 2. Create the models

```bash
ollama create planner          -f prompts/ollama/planner.Modelfile
ollama create architect        -f prompts/ollama/architect.Modelfile
ollama create code-reviewer    -f prompts/ollama/code-reviewer.Modelfile
ollama create tdd-guide        -f prompts/ollama/tdd-guide.Modelfile
ollama create security-reviewer -f prompts/ollama/security-reviewer.Modelfile
ollama create build-error-resolver -f prompts/ollama/build-error-resolver.Modelfile
ollama create refactor-cleaner -f prompts/ollama/refactor-cleaner.Modelfile
```

### 3. Use them

```bash
# Interactive chat with the planner agent
ollama run planner

# One-shot from CLI
ollama run planner "Plan a REST API for a multi-tenant SaaS app"

# Code review via pipe
cat src/auth.py | ollama run code-reviewer "Review this file"
```

---

## Use in OpenWebUI with Ollama

Once models are created, they appear automatically in OpenWebUI's model list. Select `planner`, `code-reviewer`, etc. from the model dropdown — no slash commands needed, just select the agent model.

**Combine with the [Slash Commands Filter](OpenWebUI-Integration)** for the best experience:
- Use the model dropdown to select your base Qwen 2.5 model
- Use slash commands (`/plan`, `/review`, etc.) for quick agent switching mid-conversation
- No need to create one Ollama model per agent — one base model + the filter covers all 27 agents

**Recommended setup for Qwen 2.5:**
```
OpenWebUI → Ollama → qwen2.5-coder:14b (or :32b)
         ↓
   Function Filter (slash_commands_filter.py)
         ↓
   Injects agent system prompt dynamically
```

See [OpenWebUI Integration](OpenWebUI-Integration) for complete setup.

---

## Create Models for All 27 Agents

For agents without a Modelfile, create one from any existing Modelfile:

```bash
# Template: copy and edit the agent system prompt
cp prompts/ollama/code-reviewer.Modelfile prompts/ollama/python-reviewer.Modelfile
# Edit: replace the SYSTEM content with agents/python-reviewer.md content

# Then create
ollama create python-reviewer -f prompts/ollama/python-reviewer.Modelfile
```

Or use the provided script:
```bash
python scripts/extract.py --create-modelfiles
```

---

## Scripted Usage

Use `query_agent.py` to query any agent programmatically:

```bash
# Single query
python scripts/query_agent.py --agent planner --message "Plan a payment integration"

# With Ollama backend
python scripts/query_agent.py \
  --agent code-reviewer \
  --backend http://localhost:11434/v1 \
  --model qwen2.5-coder:14b \
  --message "Review this code" \
  --file src/auth.py
```

---

## List Created Models

```bash
ollama list | grep -E "planner|architect|code-reviewer|tdd|security|build|refactor"
```

---

## Remove Models

```bash
ollama rm planner
ollama rm code-reviewer
# etc.
```
