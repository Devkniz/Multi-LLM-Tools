# Configuration

All configuration lives in `config.yaml` at the root of the repository.

---

## config.yaml Reference

```yaml
# ─────────────────────────────────────────
# LLM Backend
# ─────────────────────────────────────────
llm_backend:
  # Base URL of your OpenAI-compatible API endpoint
  base_url: "http://localhost:11434/v1"

  # Optional: API key (leave empty for local servers that don't require auth)
  api_key: ""

  # Request timeout in seconds
  timeout: 120

# ─────────────────────────────────────────
# Model Mapping
# ─────────────────────────────────────────
# Each agent specifies a tier (best / mid / fast).
# Map tiers to your actual model names here.
model_mapping:
  best: "qwen2.5-coder:32b"   # planner, architect, chief-of-staff
  mid:  "qwen2.5-coder:14b"   # code-reviewer, tdd-guide, security-reviewer, most agents
  fast: "qwen2.5-coder:7b"    # build-error-resolver, doc-updater (quick tasks)

# ─────────────────────────────────────────
# Agent Settings
# ─────────────────────────────────────────
agents:
  directory: "./agents"       # Path to agent .md files
  cache: true                 # Cache loaded agent prompts in memory

# ─────────────────────────────────────────
# Skills Settings
# ─────────────────────────────────────────
skills:
  directory: "./skills"       # Path to skills directory
```

---

## Backend Examples

### Ollama

```yaml
llm_backend:
  base_url: "http://localhost:11434/v1"
  api_key: ""

model_mapping:
  best: "qwen2.5-coder:32b"
  mid:  "qwen2.5-coder:14b"
  fast: "qwen2.5-coder:7b"
```

### LM Studio

```yaml
llm_backend:
  base_url: "http://localhost:1234/v1"
  api_key: "lm-studio"   # LM Studio requires a non-empty key

model_mapping:
  best: "lmstudio-community/qwen2.5-coder-32b-instruct"
  mid:  "lmstudio-community/qwen2.5-coder-14b-instruct"
  fast: "lmstudio-community/qwen2.5-coder-7b-instruct"
```

### llama.cpp server

```yaml
llm_backend:
  base_url: "http://localhost:8080/v1"
  api_key: ""

model_mapping:
  best: "default"
  mid:  "default"
  fast: "default"
```

### OpenAI API

```yaml
llm_backend:
  base_url: "https://api.openai.com/v1"
  api_key: "sk-..."

model_mapping:
  best: "gpt-4o"
  mid:  "gpt-4o-mini"
  fast: "gpt-4o-mini"
```

### Anthropic API (via proxy)

```yaml
llm_backend:
  base_url: "https://api.anthropic.com/v1"
  api_key: "sk-ant-..."

model_mapping:
  best: "claude-opus-4-6"
  mid:  "claude-sonnet-4-6"
  fast: "claude-haiku-4-5-20251001"
```

---

## Model Recommendations by Use Case

| Agent group | RAM needed | Recommended models |
|-------------|-----------|-------------------|
| Build fixers, doc updates | 8 GB | qwen2.5-coder:7b, codellama:7b |
| Code review, TDD, security | 16 GB | qwen2.5-coder:14b, deepseek-coder:6.7b |
| Planning, architecture, COS | 32 GB | qwen2.5-coder:32b, deepseek-coder-v2:33b |

---

## Environment Variables

You can override `config.yaml` values with environment variables:

```bash
export MULTI_LLM_BASE_URL="http://localhost:11434/v1"
export MULTI_LLM_API_KEY=""
export MULTI_LLM_MODEL_BEST="qwen2.5-coder:32b"
export MULTI_LLM_MODEL_MID="qwen2.5-coder:14b"
export MULTI_LLM_MODEL_FAST="qwen2.5-coder:7b"
```

---

## OpenWebUI Function Configuration

The OpenWebUI Function Filter has its own settings (Valves), separate from `config.yaml`.  
Configure them in OpenWebUI → **Settings → Admin → Functions → Multi-LLM Tools** (click the gear icon).

See [OpenWebUI Integration](OpenWebUI-Integration) for details.
