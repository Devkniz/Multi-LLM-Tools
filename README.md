# Multi LLM Tools

> **LLM-agnostic agent toolkit** — use powerful AI agents with any local or cloud LLM.  
> Works with Ollama, OpenWebUI, LM Studio, Aider, continue.dev, and any OpenAI-compatible API.  
> Extracted and extended from [Everything Claude Code](https://github.com/steipete/everything-claude-code).

[**Version française**](README.fr.md) | [**Wiki**](https://github.com/Devkniz/Multi-LLM-Tools/wiki) | [**Changelog**](CHANGELOG.md)

---

## What's Inside

| Category | Total | Offline-capable |
|----------|-------|-----------------|
| Agents   | 28    | **27** (only `docs-lookup` requires internet) |
| Skills   | 65    | **52** (10 require internet, 3 are meta) |
| Rules    | 74    | **74** (all offline) |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Devkniz/Multi-LLM-Tools.git
cd Multi-LLM-Tools
```

### 2. Configure your LLM backend

Edit `config.yaml`:

```yaml
llm_backend:
  base_url: "http://localhost:11434/v1"   # Ollama (default)
  # base_url: "http://localhost:1234/v1"  # LM Studio
  # base_url: "http://localhost:8080/v1"  # llama.cpp server

model_mapping:
  best: "qwen2.5-coder:32b"   # planner, architect, chief-of-staff
  mid:  "qwen2.5-coder:14b"   # code-reviewer, tdd-guide, security-reviewer
  fast: "qwen2.5-coder:7b"    # build-error-resolver, doc-updater
```

### 3. Run your first agent

```bash
python scripts/query_agent.py --agent planner --message "Plan a REST API for a todo app"

# List all available agents
python scripts/query_agent.py --list
```

---

## Platform Integrations

### OpenWebUI — Native Slash Commands

Install the native **Function Filter** (no separate service needed) to use `/plan`, `/review`, `/tdd`, and more directly in chat:

```
/plan Build a REST API with JWT authentication
/review                   ← paste your code in the message
/tdd Write a user auth module
/security                 ← audit the current conversation
/help                     ← list all available commands
```

**Quick setup (3 steps):**

1. Mount the `agents/` directory into your OpenWebUI container:
   ```yaml
   services:
     open-webui:
       image: ghcr.io/open-webui/open-webui:main
       ports: ["3000:8080"]
       volumes:
         - open-webui:/app/backend/data
         - ./agents:/app/pipelines/agents:ro
   ```

2. In OpenWebUI → **Settings → Admin → Functions** → **Upload Function** → select `prompts/openwebui/slash_commands_filter.py`

3. Click the gear icon → set `agents_dir` to `/app/pipelines/agents` → done!

**Works great with Ollama + Qwen 2.5** for closed enterprise networks. See [`prompts/openwebui/README.md`](prompts/openwebui/README.md) for the full guide.

---

### Ollama — Specialized Models

Create dedicated agent models with baked-in system prompts:

```bash
# Create the model (edit the Modelfile to set your base model first)
ollama create planner        -f prompts/ollama/planner.Modelfile
ollama create code-reviewer  -f prompts/ollama/code-reviewer.Modelfile
ollama create tdd-guide      -f prompts/ollama/tdd-guide.Modelfile
ollama create security-reviewer -f prompts/ollama/security-reviewer.Modelfile

# Use it
ollama run planner
```

Available Modelfiles: `planner`, `architect`, `build-error-resolver`, `refactor-cleaner`,
`tdd-guide`, `code-reviewer`, `security-reviewer`.

---

### Aider

```bash
# Load any agent as system prompt
aider --system-prompt-file prompts/aider/planner.txt
aider --system-prompt-file prompts/aider/code-reviewer.txt
aider --system-prompt-file prompts/aider/tdd-guide.txt
```

See [`prompts/aider/usage-examples.sh`](prompts/aider/usage-examples.sh) for all examples.

---

### continue.dev (VS Code / JetBrains)

1. Open `~/.continue/config.json`
2. Merge the `slashCommands` array from [`prompts/continue/config-fragment.json`](prompts/continue/config-fragment.json)
3. Reload your IDE

Then use `/planner`, `/code-reviewer`, `/tdd-guide`, etc. directly in the Continue chat panel.

---

### LM Studio

1. Start LM Studio and enable the local server (`http://localhost:1234`)
2. Update `config.yaml`: `base_url: "http://localhost:1234/v1"`
3. Use `python scripts/query_agent.py` or POST the JSON payloads from `prompts/openai-compatible/`

---

### Any OpenAI-Compatible API

```bash
# Edit the JSON first — replace {{USER_MESSAGE}} with your request
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @prompts/openai-compatible/planner.json
```

---

## Available Agents (27 offline)

### Planning & Architecture

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `planner` | `/plan` | best | Implementation planning for features and refactoring |
| `architect` | `/architect` | best | System design and architectural decisions |

### Code Review — Generic

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `code-reviewer` | `/review` | mid | Quality, security, and maintainability review |

### Code Review — Language-Specific

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `python-reviewer` | `/python` | mid | PEP 8, type hints, Pythonic idioms |
| `typescript-reviewer` | `/typescript` | mid | Type safety, async, Node/web security |
| `go-reviewer` | `/go` | mid | Idiomatic Go, concurrency, error handling |
| `rust-reviewer` | `/rust` | mid | Ownership, lifetimes, unsafe usage |
| `java-reviewer` | `/java` | mid | Spring Boot, JPA, layered architecture |
| `kotlin-reviewer` | `/kotlin` | mid | Coroutines, Compose, KMP |
| `cpp-reviewer` | `/cpp` | mid | Memory safety, modern C++ idioms |
| `flutter-reviewer` | `/flutter` | mid | Widgets, state management, Dart idioms |
| `database-reviewer` | `/db` | mid | PostgreSQL, schema design, query optimization |

### Build Error Fixers

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `build-error-resolver` | `/build` | mid | Build and TypeScript error fixes |
| `go-build-resolver` | `/gobuild` | mid | Go compilation errors |
| `rust-build-resolver` | `/rustbuild` | mid | Cargo / borrow checker errors |
| `cpp-build-resolver` | `/cpbuild` | mid | CMake, linker, template errors |
| `java-build-resolver` | `/javabuild` | mid | Maven/Gradle build failures |
| `kotlin-build-resolver` | `/kotlinbuild` | mid | Kotlin/Gradle errors |
| `pytorch-build-resolver` | `/pytorch` | mid | CUDA, tensor shape, DataLoader errors |

### Testing

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `tdd-guide` | `/tdd` | mid | Test-Driven Development, write tests first |
| `e2e-runner` | `/e2e` | mid | E2E tests with Playwright |

### Security & Quality

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `security-reviewer` | `/security` | mid | OWASP, secrets, injection, XSS |
| `refactor-cleaner` | `/refactor` | mid | Dead code removal, consolidation |
| `doc-updater` | `/doc` | fast | Documentation and codemap updates |

### Operations

| Agent | OpenWebUI Command | Model Tier | Description |
|-------|-------------------|------------|-------------|
| `loop-operator` | `/loop` | mid | Autonomous agent loop control |
| `harness-optimizer` | `/harness` | mid | Agent harness configuration |
| `chief-of-staff` | `/cos` | best | Email/Slack/comm triage |

**Requires internet:** `docs-lookup` (Context7 MCP)

---

## Skills (65 total)

Skills are knowledge packs that guide the LLM on specific topics.
See the [Skills wiki page](https://github.com/Devkniz/Multi-LLM-Tools/wiki/Skills) for descriptions of all 65 skills.

**Offline skills (52):** python-patterns, typescript, golang, rust, java, kotlin, cpp, flutter,
django, laravel, springboot, api-design, backend-patterns, frontend-patterns, tdd-workflow,
e2e-testing, security-review, and more.

**Internet-required skills (10):** deep-research, exa-search, documentation-lookup,
search-first, market-research, fal-ai-media, video-editing, x-api, crosspost, claude-api.

---

## Rules System

74 coding guidelines organized by language and concern:

```
rules/
├── common/          # Universal principles (all languages)
│   ├── coding-style.md
│   ├── testing.md
│   ├── security.md
│   ├── git-workflow.md
│   └── ...
├── python/
├── typescript/
├── golang/
├── rust/
├── java/
├── kotlin/
├── cpp/
├── swift/
├── php/
├── perl/
└── csharp/
```

Copy the relevant directories to your project's `.claude/rules/` folder.

---

## Model Recommendations

| Use Case | Min RAM | Recommended Models |
|----------|---------|-------------------|
| Build fixes, doc updates | 8 GB | qwen2.5-coder:7b, codellama:7b |
| Code review, TDD | 16 GB | qwen2.5-coder:14b, deepseek-coder:6.7b |
| Planning, architecture | 32 GB | qwen2.5-coder:32b, deepseek-coder-v2:33b |

---

## Directory Structure

```
Multi-LLM-Tools/
├── config.yaml                        ← LLM backend & model config
├── agents/                            ← Agent system prompts
│   ├── _index.yaml                    ← Agent registry
│   ├── planner.md
│   └── ...
├── skills/                            ← Knowledge skills
│   ├── _index.yaml
│   └── python-patterns/SKILL.md
├── rules/                             ← Coding guidelines
│   ├── common/
│   └── <language>/
├── prompts/
│   ├── openwebui/                     ← Function Filter + README
│   ├── aider/                         ← System prompt .txt files
│   ├── continue/                      ← config.json fragment
│   ├── ollama/                        ← Modelfiles
│   └── openai-compatible/             ← JSON payloads
├── docs/
│   └── tool-mapping.md                ← Claude Code → other platforms
└── scripts/
    ├── query_agent.py                 ← CLI agent runner
    ├── extract.py                     ← Re-extract from ECC source
    └── validate.py                    ← Verify offline-tier content
```

---

## Re-Extracting from ECC

If you update Everything Claude Code, re-run the extraction:

```bash
pip install pyyaml
python scripts/extract.py
```

Validate no internet leaks in local-tier content:

```bash
python scripts/validate.py
```

---

## Contributing

Issues and PRs welcome. See the [wiki](https://github.com/Devkniz/Multi-LLM-Tools/wiki) for architecture notes.

## License

MIT — see [LICENSE](LICENSE).

---

[**Version française →**](README.fr.md)
