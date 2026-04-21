# Multi LLM Tools — Wiki

> LLM-agnostic agent toolkit. Use powerful AI agents with Ollama, OpenWebUI, LM Studio, Aider, continue.dev, or any OpenAI-compatible API.

## Navigation

| Page | Description |
|------|-------------|
| [Agents](Agents) | All 28 agents — descriptions, model tiers, slash commands |
| [Skills](Skills) | All 65 skills organized by category |
| [Slash Commands](Slash-Commands) | Complete `/command` reference for OpenWebUI |
| [OpenWebUI Integration](OpenWebUI-Integration) | Native Function Filter installation and configuration |
| [Ollama Integration](Ollama-Integration) | Specialized models with baked-in system prompts |
| [Aider Integration](Aider-Integration) | System prompt files for Aider |
| [continue.dev Integration](continue.dev-Integration) | Slash commands for VS Code / JetBrains |
| [Rules System](Rules) | 74 coding guidelines by language |
| [Configuration](Configuration) | `config.yaml` reference |
| [Scripts](Scripts) | CLI tools — query, extract, validate |

---

## At a Glance

| Category | Total | Offline |
|----------|-------|---------|
| Agents | 28 | 27 |
| Skills | 65 | 52 |
| Rules | 74 | 74 |

---

## Quick Install

```bash
git clone https://github.com/Devkniz/Multi-LLM-Tools.git
cd Multi-LLM-Tools
# Edit config.yaml with your LLM backend URL
python scripts/query_agent.py --agent planner --message "Plan a REST API"
```

See [Configuration](Configuration) for all options.

---

## Platform Summary

| Platform | How agents are used | Slash commands? |
|----------|--------------------|--------------:|
| **OpenWebUI** | Native Function Filter injects system prompts | Yes — `/plan`, `/review`, etc. |
| **continue.dev** | `slashCommands` in config.json | Yes — `/planner`, `/code-reviewer`, etc. |
| **Aider** | `--system-prompt-file` at startup | No (switch files) |
| **Ollama CLI** | Dedicated model per agent via Modelfile | No (switch models) |
| **LM Studio / API** | JSON payload per request | No (swap payload) |

---

## Source

Extracted from [steipete/everything-claude-code](https://github.com/steipete/everything-claude-code) and adapted for LLM-agnostic use.
