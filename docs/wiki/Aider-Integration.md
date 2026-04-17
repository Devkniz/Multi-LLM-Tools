# Aider Integration

Aider loads agent system prompts via `--system-prompt-file` at startup.  
Each agent has a pre-generated `.txt` file in `prompts/aider/`.

---

## Available Agents

| File | Agent |
|------|-------|
| `planner.txt` | planner |
| `architect.txt` | architect |
| `code-reviewer.txt` | code-reviewer |
| `tdd-guide.txt` | tdd-guide |
| `security-reviewer.txt` | security-reviewer |
| `build-error-resolver.txt` | build-error-resolver |
| `refactor-cleaner.txt` | refactor-cleaner |
| `doc-updater.txt` | doc-updater |
| `python-reviewer.txt` | python-reviewer |
| `typescript-reviewer.txt` | typescript-reviewer |
| `go-reviewer.txt` | go-reviewer |
| `rust-reviewer.txt` | rust-reviewer |
| `java-reviewer.txt` | java-reviewer |
| `kotlin-reviewer.txt` | kotlin-reviewer |
| `cpp-reviewer.txt` | cpp-reviewer |
| `flutter-reviewer.txt` | flutter-reviewer |
| `database-reviewer.txt` | database-reviewer |
| `e2e-runner.txt` | e2e-runner |
| `loop-operator.txt` | loop-operator |
| `harness-optimizer.txt` | harness-optimizer |
| `chief-of-staff.txt` | chief-of-staff |
| `go-build-resolver.txt` | go-build-resolver |
| `rust-build-resolver.txt` | rust-build-resolver |
| `cpp-build-resolver.txt` | cpp-build-resolver |
| `java-build-resolver.txt` | java-build-resolver |
| `kotlin-build-resolver.txt` | kotlin-build-resolver |
| `pytorch-build-resolver.txt` | pytorch-build-resolver |

---

## Usage

### Basic

```bash
# Start Aider with a specific agent
aider --system-prompt-file prompts/aider/planner.txt

# With a specific model (Ollama)
aider --model ollama/qwen2.5-coder:32b \
      --system-prompt-file prompts/aider/planner.txt

# With OpenAI API
aider --model gpt-4o \
      --system-prompt-file prompts/aider/code-reviewer.txt
```

### Code Review

```bash
# Review specific files
aider --system-prompt-file prompts/aider/code-reviewer.txt \
      src/auth.py src/middleware.py

# Python-specific review
aider --system-prompt-file prompts/aider/python-reviewer.txt \
      --message "Review all Python files for PEP 8 and security issues"
```

### TDD Workflow

```bash
# Start TDD session for a new feature
aider --system-prompt-file prompts/aider/tdd-guide.txt \
      --message "Implement a rate limiter for the API"
```

### Security Audit

```bash
# Audit an entire directory
aider --system-prompt-file prompts/aider/security-reviewer.txt \
      --message "Audit all files for security vulnerabilities" \
      src/
```

### Fix Build Errors

```bash
# TypeScript build errors
aider --system-prompt-file prompts/aider/build-error-resolver.txt \
      --message "Fix the TypeScript errors in this project"

# Rust borrow checker errors
aider --system-prompt-file prompts/aider/rust-build-resolver.txt
```

---

## Shell Aliases

Add to your `.bashrc` or `.zshrc` for quick access:

```bash
# Aider agent shortcuts
alias aider-plan="aider --system-prompt-file ~/Multi-LLM-Tools/prompts/aider/planner.txt"
alias aider-review="aider --system-prompt-file ~/Multi-LLM-Tools/prompts/aider/code-reviewer.txt"
alias aider-tdd="aider --system-prompt-file ~/Multi-LLM-Tools/prompts/aider/tdd-guide.txt"
alias aider-security="aider --system-prompt-file ~/Multi-LLM-Tools/prompts/aider/security-reviewer.txt"
alias aider-build="aider --system-prompt-file ~/Multi-LLM-Tools/prompts/aider/build-error-resolver.txt"
alias aider-refactor="aider --system-prompt-file ~/Multi-LLM-Tools/prompts/aider/refactor-cleaner.txt"
```

Usage:
```bash
aider-plan "Design the database schema for a multi-tenant app"
aider-review src/auth.py
aider-tdd "Add unit tests for the payment module"
```

See `prompts/aider/usage-examples.sh` for more examples.

---

## Notes

- Aider doesn't support slash commands natively — switch agents by restarting with a different `--system-prompt-file`
- The `.txt` files contain only the system prompt text (no markdown metadata)
- For OpenWebUI slash commands, see [OpenWebUI Integration](OpenWebUI-Integration)
