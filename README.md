# ECC Extract — Everything Claude Code, LLM-Agnostic

A portable extraction of [Everything Claude Code (ECC)](https://github.com/steipete/everything-claude-code) 
that works **fully offline** with **any LLM** — Ollama, LM Studio, Aider, continue.dev, GPT4All, and more.

## What's Inside

| Category | Total | Offline-capable |
|----------|-------|-----------------|
| Agents   | 28    | **27** (only `docs-lookup` needs internet) |
| Skills   | 65    | **52** (10 need internet, 3 are meta) |
| Rules    | 74    | **74** (all offline) |

## Directory Structure

```
ECC Extract/
├── config.yaml                  ← Your LLM backend & model config
├── agents/                      ← Agent system prompts (LLM-agnostic)
│   ├── _index.yaml              ← Agent registry with metadata
│   ├── planner.md
│   ├── code-reviewer.md
│   └── ...
├── skills/                      ← Knowledge skills
│   ├── _index.yaml              ← Skill registry with tiers
│   ├── python-patterns/
│   └── ...
├── rules/                       ← Coding guidelines (copy to project)
│   ├── common/
│   └── <language>/
├── prompts/
│   ├── aider/                   ← System prompt .txt files for Aider
│   ├── continue/                ← config.json fragment for continue.dev
│   ├── ollama/                  ← Modelfiles for ollama create
│   └── openai-compatible/       ← JSON payloads for any OpenAI-compatible API
├── docs/
│   └── tool-mapping.md          ← How Claude Code tools map to other platforms
└── scripts/
    ├── extract.py               ← Re-run extraction from ECC source
    ├── validate.py              ← Verify no internet leaks in local tier
    └── query_agent.py           ← CLI to query any agent via local LLM
```

---

## Quick Start

### 1. Configure Your LLM Backend

Edit `config.yaml`:

```yaml
llm_backend:
  base_url: "http://localhost:11434/v1"   # Ollama (default)
  # base_url: "http://localhost:1234/v1"  # LM Studio
  # base_url: "http://localhost:8080/v1"  # llama.cpp server

model_mapping:
  best: "qwen2.5-coder:32b"   # For planner, architect
  mid:  "qwen2.5-coder:14b"   # For code-reviewer, tdd-guide
  fast: "qwen2.5-coder:7b"    # For build-error-resolver, doc-updater
```

### 2. Test It

```bash
# Query the planner agent
python scripts/query_agent.py --agent planner --message "Plan a REST API for a todo app"

# List available agents
python scripts/query_agent.py --list
```

---

## Platform Integration

### Ollama — Specialized Models

Create dedicated agent models with baked-in system prompts:

```bash
# 1. Edit the Modelfile, set your base model
# 2. Create the model
ollama create planner -f prompts/ollama/planner.Modelfile
ollama create code-reviewer -f prompts/ollama/code-reviewer.Modelfile
ollama create tdd-guide -f prompts/ollama/tdd-guide.Modelfile

# 3. Use it
ollama run planner
```

Available Modelfiles: `planner`, `architect`, `build-error-resolver`, 
`refactor-cleaner`, `tdd-guide`, `code-reviewer`, `security-reviewer`

### Aider

```bash
# Load any agent as system prompt
aider --system-prompt-file prompts/aider/planner.txt

# Or for code review
aider --system-prompt-file prompts/aider/code-reviewer.txt
```

See `prompts/aider/usage-examples.sh` for all examples.

### continue.dev (VS Code / JetBrains)

1. Open `~/.continue/config.json`
2. Merge the `slashCommands` array from `prompts/continue/config-fragment.json`
3. Reload your IDE

Then use `/planner`, `/code-reviewer`, `/tdd-guide`, etc. in the Continue chat.

### LM Studio

1. Start LM Studio, enable the local server (`http://localhost:1234`)
2. Update `config.yaml`: `base_url: "http://localhost:1234/v1"`
3. Use `python scripts/query_agent.py` or POST the JSON payloads from `prompts/openai-compatible/`

### Any OpenAI-Compatible API

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @prompts/openai-compatible/planner.json
```

Replace `{{USER_MESSAGE}}` in the JSON with your actual request first.

---

## Available Agents (27 offline)

| Agent | Purpose | Model Tier |
|-------|---------|------------|
| `planner` | Implementation planning | best |
| `architect` | System design | best |
| `code-reviewer` | Code review | mid |
| `tdd-guide` | Test-driven development | mid |
| `security-reviewer` | Security analysis | mid |
| `build-error-resolver` | Fix build errors | mid |
| `refactor-cleaner` | Dead code cleanup | mid |
| `doc-updater` | Documentation | mid |
| `python-reviewer` | Python code review | mid |
| `typescript-reviewer` | TypeScript/JS review | mid |
| `go-reviewer` | Go code review | mid |
| `rust-reviewer` | Rust code review | mid |
| `java-reviewer` | Java/Spring review | mid |
| `kotlin-reviewer` | Kotlin/Android review | mid |
| `cpp-reviewer` | C++ code review | mid |
| `flutter-reviewer` | Flutter/Dart review | mid |
| `database-reviewer` | PostgreSQL review | mid |
| `e2e-runner` | E2E testing | mid |
| `go-build-resolver` | Go build errors | mid |
| `rust-build-resolver` | Rust build errors | mid |
| `cpp-build-resolver` | C++ build errors | mid |
| `java-build-resolver` | Java build errors | mid |
| `kotlin-build-resolver` | Kotlin build errors | mid |
| `pytorch-build-resolver` | PyTorch errors | mid |
| `loop-operator` | Agent loop control | mid |
| `harness-optimizer` | Agent harness config | mid |
| `chief-of-staff` | Email/comm triage | best |

**Internet required**: `docs-lookup` (Context7 MCP)

---

## Skills Requiring Internet (10)

These skills need external API access — included in `skills/` with a clear banner:

- `deep-research` — firecrawl + exa web search
- `exa-search` — Exa API
- `documentation-lookup` — Context7 MCP
- `search-first` — web researcher
- `market-research` — web data
- `fal-ai-media` — fal.ai image/video
- `video-editing` — ElevenLabs, fal.ai
- `x-api` — Twitter/X API
- `crosspost` — social media APIs
- `claude-api` — Anthropic API patterns

---

## Model Recommendations

| Use Case | Min RAM | Recommended Models |
|----------|---------|-------------------|
| Build fixes, doc updates | 8 GB | qwen2.5-coder:7b, codellama:7b |
| Code review, TDD | 16 GB | qwen2.5-coder:14b, deepseek-coder:6.7b |
| Planning, architecture | 32 GB | qwen2.5-coder:32b, deepseek-coder-v2:33b |

See `docs/tool-mapping.md` for detailed platform integration notes.

---

## Re-Extracting from ECC

If you update ECC, re-run extraction:

```bash
pip install pyyaml
python scripts/extract.py
```

## Validation

Verify no internet leaks in local-tier content:

```bash
python scripts/validate.py
```
