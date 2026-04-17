#!/usr/bin/env python3
"""
ECC Extract - Validation script
Verifies that local-tier agents and skills contain no internet-dependent content.
"""

import re
import sys
import yaml
from pathlib import Path

BASE = Path(__file__).parent.parent
AGENTS_DIR = BASE / "agents"
SKILLS_DIR = BASE / "skills"

# Patterns that must NOT appear in local-tier content
FORBIDDEN_PATTERNS = [
    (r"mcp__context7__", "Context7 MCP tool call"),
    (r"mcp__firecrawl__", "Firecrawl MCP tool call"),
    (r"mcp__exa__", "Exa MCP tool call"),
    (r"\bWebSearch\b", "WebSearch tool (requires internet)"),
    (r"\bWebFetch\b", "WebFetch tool (requires internet)"),
]

errors = []
warnings = []


def check_file(path: Path, tier: str, name: str):
    if tier != "local":
        return
    text = path.read_text(encoding="utf-8")
    for pattern, label in FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"[ERROR] {name} ({path.relative_to(BASE)}): found '{label}' in local-tier content")


def validate_agents():
    index_path = AGENTS_DIR / "_index.yaml"
    if not index_path.exists():
        errors.append("[ERROR] agents/_index.yaml not found — run extract.py first")
        return

    with open(index_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    agents = data.get("agents", [])
    print(f"Checking {len(agents)} agents...")
    for agent in agents:
        tier = "internet" if agent.get("internet_required") else "local"
        file_path = AGENTS_DIR / agent["file"]
        if not file_path.exists():
            errors.append(f"[ERROR] Agent file missing: {agent['file']}")
            continue
        check_file(file_path, tier, agent["name"])

    local = sum(1 for a in agents if not a.get("internet_required"))
    internet = len(agents) - local
    print(f"  Local: {local}  |  Internet: {internet}")


def validate_skills():
    index_path = SKILLS_DIR / "_index.yaml"
    if not index_path.exists():
        errors.append("[ERROR] skills/_index.yaml not found — run extract.py first")
        return

    with open(index_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    skills = data.get("skills", [])
    print(f"Checking {len(skills)} skills...")
    for skill in skills:
        tier = skill.get("tier", "local")
        file_path = SKILLS_DIR / skill["skill"] / "SKILL.md"
        if not file_path.exists():
            errors.append(f"[ERROR] Skill file missing: {skill['skill']}/SKILL.md")
            continue
        check_file(file_path, tier, skill["name"])

    local = sum(1 for s in skills if s.get("tier") == "local")
    internet = sum(1 for s in skills if s.get("tier") == "internet")
    meta = sum(1 for s in skills if s.get("tier") == "meta")
    print(f"  Local: {local}  |  Internet: {internet}  |  Meta: {meta}")


def validate_openai_payloads():
    oai_dir = BASE / "prompts" / "openai-compatible"
    payloads = list(oai_dir.glob("*.json"))
    import json
    invalid = []
    for p in payloads:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            assert "messages" in data
            assert "model" in data
        except Exception as e:
            invalid.append(f"{p.name}: {e}")

    if invalid:
        for i in invalid:
            errors.append(f"[ERROR] Invalid OpenAI payload: {i}")
    print(f"Checking {len(payloads)} OpenAI payloads... {'OK' if not invalid else f'{len(invalid)} invalid'}")


def validate_config():
    config_path = BASE / "config.yaml"
    if not config_path.exists():
        warnings.append("[WARN] config.yaml not found — run extract.py")
        return
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    assert "llm_backend" in config, "config.yaml missing llm_backend"
    assert "model_mapping" in config, "config.yaml missing model_mapping"
    print("config.yaml ... OK")


def main():
    print("=" * 60)
    print("ECC Extract Validation")
    print("=" * 60)

    validate_agents()
    validate_skills()
    validate_openai_payloads()
    validate_config()

    print("\n" + "=" * 60)
    if errors:
        print(f"FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    elif warnings:
        print(f"PASSED with {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  {w}")
    else:
        print("ALL CHECKS PASSED")
        print(f"  No internet dependencies leaked into local-tier content.")


if __name__ == "__main__":
    main()
