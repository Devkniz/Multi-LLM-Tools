# Ollama Modelfiles

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

- `architect.Modelfile` — Software architecture specialist for system design, scalabil
- `build-error-resolver.Modelfile` — Build and TypeScript error resolution specialist. Use PROACT
- `code-reviewer.Modelfile` — Expert code review specialist. Proactively reviews code for 
- `planner.Modelfile` — Expert planning specialist for complex features and refactor
- `refactor-cleaner.Modelfile` — Dead code cleanup and consolidation specialist. Use PROACTIV
- `security-reviewer.Modelfile` — Security vulnerability detection and remediation specialist.
- `tdd-guide.Modelfile` — Test-Driven Development specialist enforcing write-tests-fir

## Tips

- **Best models for planning**: qwen2.5-coder:32b, deepseek-coder-v2:33b
- **Best for code review**: qwen2.5-coder:14b, codestral:22b
- **Fast iteration**: qwen2.5-coder:7b, starcoder2:7b
