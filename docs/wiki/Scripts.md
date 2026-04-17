# Scripts

Three Python utility scripts in the `scripts/` directory.

---

## `query_agent.py` — CLI Agent Runner

Query any agent interactively or in a pipeline.

### Prerequisites

```bash
pip install pyyaml requests
```

### Usage

```bash
# Basic query
python scripts/query_agent.py --agent planner --message "Plan a REST API for a todo app"

# List all available agents
python scripts/query_agent.py --list

# With a specific file as context
python scripts/query_agent.py \
  --agent code-reviewer \
  --message "Review this file" \
  --file src/auth.py

# Override backend (ignores config.yaml)
python scripts/query_agent.py \
  --agent security-reviewer \
  --backend http://localhost:11434/v1 \
  --model qwen2.5-coder:14b \
  --message "Audit this code for vulnerabilities" \
  --file src/api.py

# Pipe from stdin
cat src/utils.py | python scripts/query_agent.py --agent python-reviewer --message "Review"

# Save output to file
python scripts/query_agent.py \
  --agent planner \
  --message "Plan a microservices migration" \
  --output plan.md
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--agent` | required | Agent name (e.g., `planner`, `code-reviewer`) |
| `--message` | required | Your message / question |
| `--file` | — | File to include as context |
| `--backend` | from config.yaml | API base URL override |
| `--model` | from config.yaml | Model name override |
| `--output` | stdout | Save response to file |
| `--list` | — | List all available agents and exit |
| `--config` | `./config.yaml` | Path to config file |

---

## `extract.py` — Re-Extract from ECC

Re-runs the extraction from an Everything Claude Code source directory.  
Use this when you update ECC and want to pull in new agents or skills.

### Prerequisites

```bash
pip install pyyaml
```

### Usage

```bash
# Re-extract from default ECC location
python scripts/extract.py

# From a specific ECC directory
python scripts/extract.py --source ~/everything-claude-code

# Extract only agents
python scripts/extract.py --only agents

# Extract only skills
python scripts/extract.py --only skills

# Generate Modelfiles for new agents
python scripts/extract.py --create-modelfiles

# Install rules to user-level Claude config
python scripts/extract.py --install typescript python
```

### What it does

1. Reads agent `.md` files from the ECC source
2. Strips Claude Code-specific tool references (replaces with generic equivalents)
3. Generates Aider `.txt` files, Ollama Modelfiles, OpenAI-compatible JSON payloads
4. Updates `agents/_index.yaml` and `skills/_index.yaml`

---

## `validate.py` — Offline Validation

Verifies that `local`-tier agents and skills don't contain internet dependencies.

### Usage

```bash
# Validate all local-tier content
python scripts/validate.py

# Verbose output (shows each check)
python scripts/validate.py --verbose

# Check only agents
python scripts/validate.py --only agents

# Check only skills
python scripts/validate.py --only skills
```

### What it checks

- No references to `mcp__context7`, `mcp__firecrawl`, `mcp__exa` in local-tier files
- No hardcoded API URLs (OpenAI, Anthropic, etc.) in local-tier system prompts
- All files referenced in `_index.yaml` exist on disk
- YAML frontmatter is valid in all skill files

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | All checks passed |
| `1` | Validation errors found (details printed to stdout) |

---

## Workflow Example

```bash
# 1. Update ECC source
cd ~/everything-claude-code && git pull

# 2. Re-extract
cd ~/Multi-LLM-Tools
python scripts/extract.py --source ~/everything-claude-code

# 3. Validate
python scripts/validate.py

# 4. Test a new agent
python scripts/query_agent.py --agent planner --message "Test message"

# 5. Commit
git add agents/ skills/ && git commit -m "chore: update agents and skills from ECC"
```
