# Tool Mapping: Claude Code → Generic LLMs

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
