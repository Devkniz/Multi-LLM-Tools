# OpenAI-Compatible API Payloads

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
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @prompts/openai-compatible/planner.json

# Or with Python (see scripts/query_agent.py):
python scripts/query_agent.py --agent planner --message "Plan a REST API"
```

## Workflow

1. Edit `config.yaml` to set your LLM backend URL and model names
2. Replace `{{MODEL_NAME}}` in the JSON, or use the `query_agent.py` script
3. POST to your local server
