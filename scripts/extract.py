#!/usr/bin/env python3
"""
ECC Extract - Extraction script for Everything Claude Code
Extracts agents, skills, and rules from ECC and converts them
to be compatible with any LLM (Ollama, LM Studio, Aider, continue.dev, etc.)
"""

import os
import re
import json
import shutil
import yaml
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
HOME = Path.home()
ECC_BASE = HOME / ".claude"
SRC_AGENTS = ECC_BASE / "agents"
SRC_SKILLS = ECC_BASE / "skills"
SRC_RULES  = ECC_BASE / "rules"

OUT_BASE   = Path(__file__).parent.parent
OUT_AGENTS = OUT_BASE / "agents"
OUT_SKILLS = OUT_BASE / "skills"
OUT_RULES  = OUT_BASE / "rules"
OUT_PROMPTS = OUT_BASE / "prompts"

# ── Internet-dependency detection ─────────────────────────────────────────────
# Only flag actual runtime calls to external services, NOT textual mentions.
# We look for: MCP tool invocations, real API client imports, tool-use blocks.
INTERNET_TOOL_PATTERNS = [
    r"mcp__context7__",       # Context7 MCP tool calls
    r"mcp__firecrawl__",      # Firecrawl MCP
    r"mcp__exa__",            # Exa MCP
    r"\bWebSearch\b",         # Claude Code web search tool
    r"\bWebFetch\b",          # Claude Code web fetch tool
]

# Skills hardcoded as internet-required (their purpose is external API usage)
ALWAYS_INTERNET = {
    "docs-lookup",        # Context7 MCP
    "docs-lookup.md",
}

INTERNET_SKILLS = {
    "deep-research",        # firecrawl + exa MCP web search
    "exa-search",           # Exa API key required
    "documentation-lookup", # Context7 MCP live docs
    "search-first",         # invokes web researcher agent
    "market-research",      # web search for data
    "fal-ai-media",         # fal.ai API for image/video
    "video-editing",        # ElevenLabs, fal.ai
    "x-api",                # Twitter/X API
    "crosspost",            # social media APIs
}

META_SKILLS = {
    "configure-ecc", "everything-claude-code", "frontend-slides",
}

# ── Claude-specific replacements ───────────────────────────────────────────────
CLAUDE_REPLACEMENTS = [
    # Tool names → generic descriptions
    (r'\bTodoWrite\b', 'task tracker'),
    (r'\bAskUserQuestion\b', 'ask user'),
    (r'\bExitPlanMode\b', 'exit planning mode'),
    (r'\bEnterPlanMode\b', 'enter planning mode'),
    (r'\bmcp__context7__[a-z_-]+\b', 'documentation lookup tool'),
    # Model references
    (r'claude-opus-4[-\w]*', '{{BEST_MODEL}}'),
    (r'claude-sonnet-4[-\w]*', '{{MID_MODEL}}'),
    (r'claude-haiku-4[-\w]*', '{{FAST_MODEL}}'),
    (r'\bclaude-opus\b', '{{BEST_MODEL}}'),
    (r'\bclaude-sonnet\b', '{{MID_MODEL}}'),
    (r'\bclaude-haiku\b', '{{FAST_MODEL}}'),
    # Claude Code specific concepts
    (r'CLAUDE\.md', 'project instructions file (CLAUDE.md or equivalent)'),
    (r'\bClaude Code\b', 'AI coding assistant'),
    (r'\bClaude\b(?! Code)', 'the AI assistant'),
    (r'extended thinking', 'deep reasoning mode'),
    (r'/compact\b', '/compact (context compression command)'),
]

# ── Model tier mapping ─────────────────────────────────────────────────────────
MODEL_TIER = {
    "opus":   "best",
    "sonnet": "mid",
    "haiku":  "fast",
}

TOOL_MAPPING = {
    "Read":             "file_read",
    "Write":            "file_write",
    "Edit":             "file_edit",
    "Bash":             "shell_exec",
    "Grep":             "search",
    "Glob":             "file_search",
    "TodoWrite":        "task_tracker",
    "AskUserQuestion":  "ask_user",
    "Task":             "spawn_subagent",
    "Agent":            "spawn_subagent",
    "WebSearch":        "web_search",
    "WebFetch":         "web_fetch",
    "NotebookEdit":     "notebook_edit",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns (meta, body)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw_yaml = text[3:end].strip()
            body = text[end + 4:].lstrip("\n")
            try:
                meta = yaml.safe_load(raw_yaml) or {}
            except Exception:
                meta = {}
            return meta, body
    return {}, text


def clean_body(text: str) -> str:
    """Apply Claude-specific replacements to make text LLM-agnostic."""
    for pattern, replacement in CLAUDE_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def has_internet_dependency(name: str, text: str) -> bool:
    """Detect if content requires internet.

    Only flag actual runtime calls to external services — NOT textual mentions
    of URLs, API keys in example code, or conceptual references to 'the internet'.
    """
    if name in ALWAYS_INTERNET:
        return True
    name_clean = name.replace(".md", "").replace("/SKILL", "")
    if name_clean in INTERNET_SKILLS:
        return True
    # Check for actual MCP tool invocations or web tool calls in the prompt text
    for pattern in INTERNET_TOOL_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def classify_skill(skill_name: str, content: str) -> str:
    """Return tier: local | internet | meta"""
    if skill_name in META_SKILLS:
        return "meta"
    if has_internet_dependency(skill_name, content):
        return "internet"
    return "local"


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  [+] {path.relative_to(OUT_BASE)}")


# ── Agent extraction ───────────────────────────────────────────────────────────

def extract_agents() -> list[dict]:
    registry = []
    print("\n=== Extracting Agents ===")

    for src_file in sorted(SRC_AGENTS.glob("*.md")):
        text = src_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        name = meta.get("name", src_file.stem)
        description = meta.get("description", "")
        tools_raw = meta.get("tools", [])
        model_raw = meta.get("model", "sonnet")

        # Determine internet dependency
        internet = has_internet_dependency(src_file.name, text)
        tier = "internet" if internet else "local"

        # Map tools
        tools_generic = [TOOL_MAPPING.get(t, t.lower()) for t in (tools_raw or [])]
        model_tier = MODEL_TIER.get(str(model_raw).lower(), "mid")

        # Clean body
        clean = clean_body(body)

        # Build output: generic header + cleaned body
        header = f"""# Agent: {name}

> **Tier**: {tier}
> **Model tier**: {model_tier} (map to your best local model if tier=best, mid otherwise)
> **Tools needed**: {', '.join(tools_generic) if tools_generic else 'none'}
> **Internet required**: {'YES' if internet else 'No'}

**Description**: {description}

---

"""
        if internet:
            header = "<!-- REQUIRES INTERNET: This agent uses external services -->\n\n" + header

        out_path = OUT_AGENTS / src_file.name
        write_file(out_path, header + clean)

        registry.append({
            "name": name,
            "file": str(src_file.name),
            "description": description,
            "tier": tier,
            "model_tier": model_tier,
            "tools": tools_generic,
            "internet_required": internet,
        })

    # Write registry
    registry_path = OUT_AGENTS / "_index.yaml"
    write_file(registry_path, yaml.dump({"agents": registry}, allow_unicode=True, sort_keys=False))
    print(f"\n  Extracted {len(registry)} agents")
    return registry


# ── Skill extraction ───────────────────────────────────────────────────────────

def extract_skills() -> list[dict]:
    registry = []
    print("\n=== Extracting Skills ===")

    for skill_dir in sorted(SRC_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        skill_name = skill_dir.name
        name = meta.get("name", skill_name)
        description = meta.get("description", "")

        tier = classify_skill(skill_name, text)
        clean = clean_body(body)

        # Build output
        tier_banner = ""
        if tier == "internet":
            tier_banner = "\n> **REQUIRES INTERNET**: This skill requires external API access.\n\n"
        elif tier == "meta":
            tier_banner = "\n> **META SKILL**: Configuration or tool-specific skill.\n\n"

        header = f"""---
name: {name}
description: {description}
tier: {tier}
origin: ECC
---
{tier_banner}"""

        out_dir = OUT_SKILLS / skill_name
        write_file(out_dir / "SKILL.md", header + clean)

        # Copy sub-agents or extra files if present (skip openai.yaml — we regenerate)
        for extra in skill_dir.iterdir():
            if extra.name in ("SKILL.md",) or extra.suffix in (".yaml", ".yml"):
                continue
            if extra.is_file():
                shutil.copy2(extra, out_dir / extra.name)

        registry.append({
            "name": name,
            "skill": skill_name,
            "description": description,
            "tier": tier,
            "internet_required": tier == "internet",
        })

    registry_path = OUT_SKILLS / "_index.yaml"
    write_file(registry_path, yaml.dump({"skills": registry}, allow_unicode=True, sort_keys=False))

    local_count = sum(1 for r in registry if r["tier"] == "local")
    internet_count = sum(1 for r in registry if r["tier"] == "internet")
    meta_count = sum(1 for r in registry if r["tier"] == "meta")
    print(f"\n  Extracted {len(registry)} skills: {local_count} local, {internet_count} internet, {meta_count} meta")
    return registry


# ── Rules extraction ───────────────────────────────────────────────────────────

def extract_rules():
    print("\n=== Copying Rules ===")
    count = 0
    for item in SRC_RULES.rglob("*"):
        if item.is_file() and item.suffix == ".md":
            rel = item.relative_to(SRC_RULES)
            out_path = OUT_RULES / rel
            text = item.read_text(encoding="utf-8")
            write_file(out_path, text)
            count += 1
    print(f"\n  Copied {count} rule files")


# ── Platform adapters ──────────────────────────────────────────────────────────

def generate_aider_configs(agents: list[dict]):
    print("\n=== Generating Aider configs ===")
    aider_dir = OUT_PROMPTS / "aider"

    readme = """# Aider Integration

Use these system prompts with Aider:

```bash
# Load a specific agent as system prompt
aider --system-prompt-file agents/planner.txt

# Or set in .aider.conf.yml
```

Each `.txt` file here is a ready-to-use Aider system prompt.
The `.aider.conf.yml` snippet shows how to configure your project.
"""
    write_file(aider_dir / "README.md", readme)

    conf_snippets = []
    for agent in agents:
        if agent["internet_required"]:
            continue
        agent_file = OUT_AGENTS / agent["file"]
        if not agent_file.exists():
            continue
        text = agent_file.read_text(encoding="utf-8")
        # Strip markdown headers for cleaner system prompt
        prompt_text = re.sub(r'^#.*\n', '', text, flags=re.MULTILINE)
        prompt_text = re.sub(r'^>.*\n', '', prompt_text, flags=re.MULTILINE)
        prompt_text = re.sub(r'---+\n', '', prompt_text)
        prompt_text = prompt_text.strip()

        out_path = aider_dir / f"{agent['name']}.txt"
        write_file(out_path, prompt_text)
        conf_snippets.append(f"# Agent: {agent['name']}\n# aider --system-prompt-file prompts/aider/{agent['name']}.txt")

    write_file(aider_dir / "usage-examples.sh", "\n\n".join(conf_snippets))
    print(f"  Generated {sum(1 for a in agents if not a['internet_required'])} Aider prompt files")


def generate_continue_configs(agents: list[dict]):
    print("\n=== Generating continue.dev configs ===")
    continue_dir = OUT_PROMPTS / "continue"

    # Build slash commands config fragment
    slash_commands = []
    for agent in agents:
        if agent["internet_required"]:
            continue
        agent_file = OUT_AGENTS / agent["file"]
        if not agent_file.exists():
            continue
        text = agent_file.read_text(encoding="utf-8")

        slash_commands.append({
            "name": agent["name"],
            "description": agent["description"][:80],
            "prompt": text[:2000],  # First 2k chars as preview
        })

    config_fragment = {
        "slashCommands": [
            {
                "name": cmd["name"],
                "description": cmd["description"],
                "systemMessageTemplate": cmd["prompt"],
            }
            for cmd in slash_commands
        ]
    }

    write_file(
        continue_dir / "config-fragment.json",
        json.dumps(config_fragment, indent=2, ensure_ascii=False)
    )

    readme = """# continue.dev Integration

Add the slash commands from `config-fragment.json` to your `~/.continue/config.json`.

## Quick Setup

1. Open `~/.continue/config.json`
2. Merge the `slashCommands` array from `config-fragment.json` into your config
3. Reload VS Code / JetBrains

## Full Agent Prompts

Each agent's full system prompt is available in `../agents/` directory.
You can reference them via continue.dev's custom system prompt feature.
"""
    write_file(continue_dir / "README.md", readme)
    print(f"  Generated continue.dev config with {len(slash_commands)} slash commands")


def generate_ollama_modelfiles(agents: list[dict]):
    print("\n=== Generating Ollama Modelfiles ===")
    ollama_dir = OUT_PROMPTS / "ollama"

    # Priority agents for Ollama Modelfiles
    priority = {"planner", "code-reviewer", "tdd-guide", "architect",
                 "security-reviewer", "build-error-resolver", "refactor-cleaner"}

    readme_entries = []
    for agent in agents:
        if agent["internet_required"]:
            continue
        if agent["name"] not in priority:
            continue

        agent_file = OUT_AGENTS / agent["file"]
        if not agent_file.exists():
            continue

        text = agent_file.read_text(encoding="utf-8")
        # Strip markdown formatting for cleaner system prompt
        system_prompt = re.sub(r'^#.*\n', '', text, flags=re.MULTILINE)
        system_prompt = re.sub(r'^>.*\n', '', system_prompt, flags=re.MULTILINE)
        system_prompt = re.sub(r'---+\n', '', system_prompt)
        system_prompt = system_prompt.strip()

        model_comment = {
            "best": "# Recommended: deepseek-coder-v2:33b, qwen2.5-coder:32b, codestral:22b",
            "mid":  "# Recommended: qwen2.5-coder:14b, deepseek-coder:6.7b, codellama:13b",
            "fast": "# Recommended: qwen2.5-coder:7b, codellama:7b, starcoder2:7b",
        }.get(agent["model_tier"], "# Recommended: any capable model")

        modelfile = f"""# Ollama Modelfile for: {agent['name']}
# {agent['description']}
#
{model_comment}
# Usage:
#   1. Replace 'your-model-name' with your chosen model
#   2. ollama create {agent['name']} -f prompts/ollama/{agent['name']}.Modelfile
#   3. ollama run {agent['name']}

FROM your-model-name

PARAMETER temperature 0.2
PARAMETER top_p 0.9

SYSTEM \"\"\"
{system_prompt}
\"\"\"
"""
        out_path = ollama_dir / f"{agent['name']}.Modelfile"
        write_file(out_path, modelfile)
        readme_entries.append(f"- `{agent['name']}.Modelfile` — {agent['description'][:60]}")

    readme = f"""# Ollama Modelfiles

Create specialized local AI models with baked-in agent system prompts.

## Quick Start

```bash
# 1. Choose your base model (examples):
#    qwen2.5-coder:14b  (best coding, 14B params)
#    deepseek-coder-v2:16b  (excellent, 16B params)
#    codellama:13b  (good, 13B params)

# 2. Edit the Modelfile, replace 'your-model-name' with your model
# 3. Create the specialized model:
ollama create planner -f prompts/ollama/planner.Modelfile

# 4. Run it:
ollama run planner
```

## Available Modelfiles

{chr(10).join(readme_entries)}

## Tips

- **Best models for planning**: qwen2.5-coder:32b, deepseek-coder-v2:33b
- **Best for code review**: qwen2.5-coder:14b, codestral:22b
- **Fast iteration**: qwen2.5-coder:7b, starcoder2:7b
"""
    write_file(ollama_dir / "README.md", readme)
    print(f"  Generated {len(readme_entries)} Ollama Modelfiles")


def generate_openai_compatible(agents: list[dict]):
    print("\n=== Generating OpenAI-compatible payloads ===")
    oai_dir = OUT_PROMPTS / "openai-compatible"

    for agent in agents:
        if agent["internet_required"]:
            continue
        agent_file = OUT_AGENTS / agent["file"]
        if not agent_file.exists():
            continue

        text = agent_file.read_text(encoding="utf-8")

        payload = {
            "model": "{{MODEL_NAME}}",
            "messages": [
                {
                    "role": "system",
                    "content": text
                },
                {
                    "role": "user",
                    "content": "{{USER_MESSAGE}}"
                }
            ],
            "temperature": 0.2,
            "max_tokens": 4096,
            "_meta": {
                "agent": agent["name"],
                "description": agent["description"],
                "model_tier": agent["model_tier"],
                "tools_needed": agent["tools"],
            }
        }

        out_path = oai_dir / f"{agent['name']}.json"
        write_file(out_path, json.dumps(payload, indent=2, ensure_ascii=False))

    readme = """# OpenAI-Compatible API Payloads

Ready-to-use JSON request bodies for any OpenAI-compatible endpoint.

## Compatible Servers

- **Ollama**: `http://localhost:11434/v1`
- **LM Studio**: `http://localhost:1234/v1`
- **llama.cpp server**: `http://localhost:8080/v1`
- **vLLM**: `http://localhost:8000/v1`
- **Jan**: `http://localhost:1337/v1`
- **GPT4All**: `http://localhost:4891/v1`

## Usage

```bash
# Replace {{MODEL_NAME}} and {{USER_MESSAGE}} then POST:
curl http://localhost:11434/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -d @prompts/openai-compatible/planner.json

# Or with Python (see scripts/query_agent.py):
python scripts/query_agent.py --agent planner --message "Plan a REST API"
```

## Workflow

1. Edit `config.yaml` to set your LLM backend URL and model names
2. Replace `{{MODEL_NAME}}` in the JSON, or use the `query_agent.py` script
3. POST to your local server
"""
    write_file(oai_dir / "README.md", readme)
    print(f"  Generated {sum(1 for a in agents if not a['internet_required'])} OpenAI-compatible payloads")


# ── Config file ────────────────────────────────────────────────────────────────

def generate_config():
    print("\n=== Generating config.yaml ===")
    config = {
        "llm_backend": {
            "type": "openai-compatible",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
            "_comment": "Change base_url for LM Studio (1234), llama.cpp (8080), vLLM (8000), Jan (1337)",
        },
        "model_mapping": {
            "best":  "qwen2.5-coder:32b",
            "mid":   "qwen2.5-coder:14b",
            "fast":  "qwen2.5-coder:7b",
            "_comment": "Map agent model tiers to your installed local models",
            "_alternatives": {
                "deepseek": {"best": "deepseek-coder-v2:33b", "mid": "deepseek-coder-v2:16b", "fast": "deepseek-coder:6.7b"},
                "codellama": {"best": "codellama:70b", "mid": "codellama:13b", "fast": "codellama:7b"},
                "mistral":  {"best": "mistral:7b", "mid": "mistral:7b", "fast": "mistral:7b"},
            }
        },
        "tool_mapping": {
            "file_read":     "Read local files",
            "file_write":    "Write local files",
            "file_edit":     "Edit local files",
            "shell_exec":    "Run shell commands",
            "search":        "Grep/ripgrep file content",
            "file_search":   "Glob file patterns",
            "task_tracker":  "Track tasks (markdown todo list)",
            "ask_user":      "Ask user for clarification",
            "spawn_subagent": "Not available in most local setups - handle sequentially",
        },
        "defaults": {
            "temperature": 0.2,
            "max_tokens":  4096,
            "timeout_seconds": 120,
        }
    }
    write_file(OUT_BASE / "config.yaml", yaml.dump(config, allow_unicode=True, sort_keys=False))


# ── Tool mapping doc ───────────────────────────────────────────────────────────

def generate_tool_mapping_doc():
    print("\n=== Generating tool mapping documentation ===")
    doc = """# Tool Mapping: Claude Code → Generic LLMs

This document explains how each Claude Code tool maps to equivalent capabilities
in other AI coding tools (Aider, continue.dev, Ollama, etc.)

## Tool Translation Table

| Claude Code Tool | Generic Equivalent | Aider | continue.dev | Direct LLM |
|-----------------|-------------------|-------|--------------|------------|
| `Read` | file_read | Read file manually | File context | Read file, paste content |
| `Write` | file_write | Aider writes files | Inline edit | Ask to output full file |
| `Edit` | file_edit | Aider diffs | Inline edit | Ask for diff |
| `Bash` | shell_exec | `!command` prefix | Terminal | Ask command, run manually |
| `Grep` | search | `!grep` / `!rg` | Search | Ask for regex, run manually |
| `Glob` | file_search | `!find` | File picker | Ask for pattern, run manually |
| `TodoWrite` | task_tracker | Markdown checklist | Custom | Ask for numbered list |
| `AskUserQuestion` | ask_user | Direct dialogue | Direct dialogue | Direct dialogue |
| `Task` / `Agent` | spawn_subagent | Not available | Not available | Sequential prompts |

## Platform-Specific Notes

### Aider
- Use `--system-prompt-file` to load an agent prompt: `aider --system-prompt-file prompts/aider/planner.txt`
- Aider handles file edits natively — the `Edit`, `Write`, `Read` tools map directly
- Use `!command` prefix for shell execution
- Multi-agent orchestration: run Aider multiple times with different system prompts

### continue.dev
- Load agents as slash commands in `~/.continue/config.json`
- Files are loaded via `@file` mention in chat
- Use `@codebase` for project-wide context
- Shell commands: use integrated terminal

### Ollama (direct)
- Create specialized models with `FROM + SYSTEM` Modelfiles (see `prompts/ollama/`)
- Tools (file read/write/exec) are not available — the LLM guides, the user executes
- For agentic workflows, use Ollama with a tool-calling framework (LangChain, CrewAI, etc.)

### LM Studio
- Use OpenAI-compatible endpoint: `http://localhost:1234/v1`
- Load agent JSON payloads from `prompts/openai-compatible/`
- Same tool limitations as direct Ollama use

### Using with Tool-Calling Frameworks
For true tool-use capability with local LLMs:
- **LangChain + Ollama**: Full tool calling support
- **CrewAI**: Multi-agent with local models
- **AutoGen**: Microsoft's agent framework (works with Ollama)
- **Instructor + Ollama**: Structured output with tool schemas

## Model Size Recommendations

| Agent Complexity | Minimum RAM | Recommended Model |
|-----------------|-------------|-------------------|
| Simple (build-fix, doc-update) | 8 GB | qwen2.5-coder:7b |
| Medium (code-review, tdd-guide) | 16 GB | qwen2.5-coder:14b |
| Complex (planner, architect) | 32 GB | qwen2.5-coder:32b, deepseek-coder-v2:33b |
"""
    write_file(OUT_BASE / "docs" / "tool-mapping.md", doc)


# ── Query helper script ────────────────────────────────────────────────────────

def generate_query_script():
    print("\n=== Generating query_agent.py helper ===")
    script = '''#!/usr/bin/env python3
"""
Query any extracted agent against a local LLM.
Usage: python scripts/query_agent.py --agent planner --message "Plan a REST API"
"""
import argparse
import json
import sys
from pathlib import Path
import urllib.request
import urllib.error

BASE = Path(__file__).parent.parent


def load_config() -> dict:
    import yaml
    config_path = BASE / "config.yaml"
    if not config_path.exists():
        return {
            "llm_backend": {"base_url": "http://localhost:11434/v1", "api_key": "ollama"},
            "model_mapping": {"best": "qwen2.5-coder:32b", "mid": "qwen2.5-coder:14b", "fast": "qwen2.5-coder:7b"},
            "defaults": {"temperature": 0.2, "max_tokens": 4096},
        }
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_agent(agent_name: str) -> tuple[str, str]:
    """Returns (system_prompt, model_tier)"""
    agent_file = BASE / "agents" / f"{agent_name}.md"
    if not agent_file.exists():
        print(f"ERROR: Agent '{agent_name}' not found at {agent_file}", file=sys.stderr)
        sys.exit(1)

    text = agent_file.read_text(encoding="utf-8")
    # Extract model tier from header comment
    model_tier = "mid"
    for line in text.splitlines():
        if "Model tier" in line:
            if "best" in line:
                model_tier = "best"
            elif "fast" in line:
                model_tier = "fast"
            break

    return text, model_tier


def query_llm(base_url: str, api_key: str, model: str, system: str,
              user_message: str, temperature: float, max_tokens: int) -> str:
    url = f"{base_url.rstrip(\'/\')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user_message},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        print(f"ERROR connecting to {url}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query an ECC agent via local LLM")
    parser.add_argument("--agent", required=True, help="Agent name (e.g. planner, code-reviewer)")
    parser.add_argument("--message", required=True, help="User message / task")
    parser.add_argument("--model", help="Override model name")
    parser.add_argument("--list", action="store_true", help="List available agents")
    args = parser.parse_args()

    if args.list:
        agents_dir = BASE / "agents"
        for f in sorted(agents_dir.glob("*.md")):
            if f.name.startswith("_"):
                continue
            print(f"  {f.stem}")
        return

    config = load_config()
    backend = config.get("llm_backend", {})
    mapping = config.get("model_mapping", {})
    defaults = config.get("defaults", {})

    system_prompt, model_tier = load_agent(args.agent)
    model = args.model or mapping.get(model_tier, mapping.get("mid", "qwen2.5-coder:14b"))

    print(f"Using agent: {args.agent} | Model tier: {model_tier} | Model: {model}")
    print(f"Backend: {backend.get('base_url', 'http://localhost:11434/v1')}")
    print("─" * 60)

    response = query_llm(
        base_url=backend.get("base_url", "http://localhost:11434/v1"),
        api_key=backend.get("api_key", "ollama"),
        model=model,
        system=system_prompt,
        user_message=args.message,
        temperature=defaults.get("temperature", 0.2),
        max_tokens=defaults.get("max_tokens", 4096),
    )
    print(response)


if __name__ == "__main__":
    main()
'''
    write_file(OUT_BASE / "scripts" / "query_agent.py", script)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("ECC Extract - Starting extraction")
    print(f"Source: {ECC_BASE}")
    print(f"Output: {OUT_BASE}")
    print("=" * 60)

    agents   = extract_agents()
    skills   = extract_skills()
    extract_rules()

    generate_aider_configs(agents)
    generate_continue_configs(agents)
    generate_ollama_modelfiles(agents)
    generate_openai_compatible(agents)

    generate_config()
    generate_tool_mapping_doc()
    generate_query_script()

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print(f"  Agents  : {len(agents)} ({sum(1 for a in agents if not a['internet_required'])} local)")
    print(f"  Skills  : {len(skills)} ({sum(1 for s in skills if s['tier'] == 'local')} local)")
    print(f"  Output  : {OUT_BASE}")
    print("\nNext steps:")
    print("  1. Edit config.yaml with your LLM backend URL and model names")
    print("  2. Test: python scripts/query_agent.py --agent planner --message 'Plan a hello world'")
    print("  3. See docs/tool-mapping.md for platform integration guides")


if __name__ == "__main__":
    main()
