#!/usr/bin/env python3
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
    url = f"{base_url.rstrip('/')}/chat/completions"
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
