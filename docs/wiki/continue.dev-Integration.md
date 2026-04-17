# continue.dev Integration

continue.dev is a VS Code and JetBrains extension with native slash command support.  
The `config-fragment.json` adds all agents as `/command` entries directly in the chat panel.

---

## Installation

### 1. Locate your continue.dev config

```bash
# macOS / Linux
~/.continue/config.json

# Windows
%USERPROFILE%\.continue\config.json
```

### 2. Merge the slash commands

Open `prompts/continue/config-fragment.json` and copy the `slashCommands` array into your `config.json`:

**config-fragment.json (excerpt):**
```json
{
  "slashCommands": [
    {
      "name": "planner",
      "description": "Expert planning specialist for features and refactoring",
      "prompt": "..."
    },
    {
      "name": "code-reviewer",
      "description": "Code review for quality, security, and maintainability",
      "prompt": "..."
    }
  ]
}
```

**Your config.json:**
```json
{
  "models": [...],
  "slashCommands": [
    // paste the slashCommands array here
    // merge with any existing entries
  ]
}
```

### 3. Reload the IDE

- **VS Code:** Cmd/Ctrl+Shift+P → "Developer: Reload Window"
- **JetBrains:** File → Invalidate Caches → Restart

---

## Usage

In the Continue chat panel (Cmd/Ctrl+L), type `/` to see the agent list:

```
/planner        → planner agent
/code-reviewer  → code review
/tdd-guide      → test-driven development
/security-reviewer → security audit
/architect      → system design
/python-reviewer → Python review
/typescript-reviewer → TypeScript/JS review
/go-reviewer    → Go review
/rust-reviewer  → Rust review
```

Then type your message after the command:
```
/planner Build a real-time chat feature with WebSockets
/tdd-guide Implement the user registration endpoint
```

Or select code in the editor, press Cmd/Ctrl+L to send it to Continue, then type:
```
/code-reviewer Review the selected code
/security-reviewer Check this for vulnerabilities
```

---

## All Available Commands

| Command | Agent |
|---------|-------|
| `/planner` | planner |
| `/architect` | architect |
| `/code-reviewer` | code-reviewer |
| `/tdd-guide` | tdd-guide |
| `/security-reviewer` | security-reviewer |
| `/build-error-resolver` | build-error-resolver |
| `/refactor-cleaner` | refactor-cleaner |
| `/doc-updater` | doc-updater |
| `/python-reviewer` | python-reviewer |
| `/typescript-reviewer` | typescript-reviewer |
| `/go-reviewer` | go-reviewer |
| `/rust-reviewer` | rust-reviewer |
| `/java-reviewer` | java-reviewer |
| `/kotlin-reviewer` | kotlin-reviewer |
| `/cpp-reviewer` | cpp-reviewer |
| `/flutter-reviewer` | flutter-reviewer |
| `/database-reviewer` | database-reviewer |
| `/e2e-runner` | e2e-runner |

---

## Model Configuration

continue.dev uses whatever model you have configured. Pair agents with appropriate models:

```json
{
  "models": [
    {
      "title": "Planner (Ollama)",
      "provider": "ollama",
      "model": "qwen2.5-coder:32b"
    },
    {
      "title": "Code Review (Ollama)",
      "provider": "ollama",
      "model": "qwen2.5-coder:14b"
    }
  ]
}
```

Use `@model Planner (Ollama)` in the chat to switch to the stronger model when using `/planner`.

---

## Notes

- continue.dev slash commands are client-side — they inject the system prompt into the request
- Works with any provider: Ollama, OpenAI, Anthropic, Azure OpenAI, etc.
- For shorter commands like `/plan` instead of `/planner`, see [OpenWebUI Integration](OpenWebUI-Integration)
