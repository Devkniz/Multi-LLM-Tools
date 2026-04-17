"""
Multi-LLM Tools — OpenWebUI Slash Commands Pipeline
====================================================
Filter pipeline that intercepts /command patterns in user messages
and injects the corresponding agent system prompt before the LLM call.

Usage in OpenWebUI chat:
  /plan Build a REST API for a todo app
  /review                         (paste code in message)
  /tdd Write a user auth module
  /security                       (review conversation context)
  /help                           (list all commands)

Installation: see prompts/openwebui/README.md
"""

from typing import List, Optional
from pydantic import BaseModel
import os
import re


# ---------------------------------------------------------------------------
# Command → agent file mapping
# ---------------------------------------------------------------------------
COMMAND_MAP: dict[str, str] = {
    # Planning & architecture
    "plan":          "planner",
    "planner":       "planner",
    "architect":     "architect",
    "arch":          "architect",
    # Code review — generic
    "review":        "code-reviewer",
    "cr":            "code-reviewer",
    # Language-specific reviewers
    "python":        "python-reviewer",
    "py":            "python-reviewer",
    "typescript":    "typescript-reviewer",
    "ts":            "typescript-reviewer",
    "js":            "typescript-reviewer",
    "go":            "go-reviewer",
    "golang":        "go-reviewer",
    "rust":          "rust-reviewer",
    "java":          "java-reviewer",
    "kotlin":        "kotlin-reviewer",
    "cpp":           "cpp-reviewer",
    "c++":           "cpp-reviewer",
    "flutter":       "flutter-reviewer",
    "dart":          "flutter-reviewer",
    "db":            "database-reviewer",
    "database":      "database-reviewer",
    "sql":           "database-reviewer",
    # Build fixers
    "build":         "build-error-resolver",
    "fix":           "build-error-resolver",
    "gobuild":       "go-build-resolver",
    "rustbuild":     "rust-build-resolver",
    "cpbuild":       "cpp-build-resolver",
    "javabuild":     "java-build-resolver",
    "kotlinbuild":   "kotlin-build-resolver",
    "pytorch":       "pytorch-build-resolver",
    # TDD & testing
    "tdd":           "tdd-guide",
    "test":          "tdd-guide",
    "e2e":           "e2e-runner",
    # Security
    "security":      "security-reviewer",
    "sec":           "security-reviewer",
    # Maintenance
    "refactor":      "refactor-cleaner",
    "clean":         "refactor-cleaner",
    "doc":           "doc-updater",
    "docs":          "doc-updater",
    # Ops
    "loop":          "loop-operator",
    "harness":       "harness-optimizer",
    "cos":           "chief-of-staff",
}

# Human-readable descriptions shown in /help
COMMAND_HELP: dict[str, str] = {
    "/plan [task]":       "Implementation planning for features or refactoring",
    "/architect [task]":  "System design and architectural decisions",
    "/review [code]":     "Generic code review (quality, security, maintainability)",
    "/tdd [feature]":     "Test-Driven Development — write tests first",
    "/security [code]":   "Security audit — OWASP, secrets, injection, XSS",
    "/refactor [code]":   "Dead code cleanup and consolidation",
    "/doc [task]":        "Documentation and codemap updates",
    "/build [error]":     "Fix build / TypeScript errors",
    "/e2e [flow]":        "E2E test generation and maintenance",
    "/python [code]":     "Python code review (PEP 8, type hints, idioms)",
    "/typescript [code]": "TypeScript/JS review (type safety, async, security)",
    "/go [code]":         "Go code review (idiomatic, concurrency, errors)",
    "/rust [code]":       "Rust review (ownership, lifetimes, unsafe)",
    "/java [code]":       "Java/Spring Boot review",
    "/kotlin [code]":     "Kotlin/Android/KMP review",
    "/cpp [code]":        "C++ review (memory safety, modern idioms)",
    "/flutter [code]":    "Flutter/Dart review (widgets, state, Compose)",
    "/db [query]":        "PostgreSQL query, schema, and migration review",
    "/loop [task]":       "Autonomous agent loop control",
    "/help":              "Show this help message",
}


class Pipeline:

    class Valves(BaseModel):
        # Path to the agents/ directory — adjust to where you mounted the files
        agents_dir: str = "/app/pipelines/agents"
        # Show a banner in the response when an agent is activated
        show_activation_banner: bool = True
        # Prefix to show in the banner (empty = no banner)
        banner_prefix: str = "**Agent activated:** "
        # If True, unknown /commands are passed through unchanged
        passthrough_unknown: bool = True

    def __init__(self):
        self.type = "filter"
        self.name = "Multi-LLM Tools — Slash Commands"
        self.valves = self.Valves()
        self._agent_cache: dict[str, str] = {}

    async def on_startup(self):
        print(f"[MultiLLMTools] Pipeline started. agents_dir={self.valves.agents_dir}")

    async def on_shutdown(self):
        print("[MultiLLMTools] Pipeline stopped.")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_agent(self, agent_name: str) -> Optional[str]:
        """Load and cache an agent system prompt, stripping the metadata header."""
        if agent_name in self._agent_cache:
            return self._agent_cache[agent_name]

        path = os.path.join(self.valves.agents_dir, f"{agent_name}.md")
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()

        # The agent files have a metadata block that ends with '---'
        # Everything after the first '---' separator is the actual system prompt.
        # Format:
        #   # Agent: name
        #   > **Tier**: ...
        #   > **Description**: ...
        #   ---
        #   You are an expert...
        parts = raw.split("\n---\n", 1)
        prompt = parts[1].strip() if len(parts) == 2 else raw.strip()

        self._agent_cache[agent_name] = prompt
        return prompt

    def _build_help_message(self) -> str:
        lines = ["## Multi-LLM Tools — Available Commands\n"]
        for cmd, desc in COMMAND_HELP.items():
            lines.append(f"- `{cmd}` — {desc}")
        lines.append(
            "\n> Tip: commands are case-insensitive. "
            "You can add your message directly after the command.\n"
            "> Example: `/plan Build a REST API with authentication`"
        )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Filter inlet — runs before the LLM call
    # ------------------------------------------------------------------

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        messages: List[dict] = body.get("messages", [])
        if not messages:
            return body

        last = messages[-1]
        if last.get("role") != "user":
            return body

        content: str = last.get("content", "")

        # Match /command [optional rest of message]
        match = re.match(r"^/([a-zA-Z][\w+-]*)\s*([\s\S]*)", content.strip())
        if not match:
            return body

        command = match.group(1).lower()
        remainder = match.group(2).strip()

        # /help is handled locally — no LLM call needed
        if command == "help":
            # We inject a fake assistant response by adding a system note.
            # OpenWebUI will show it after the pipeline processes the request.
            # Best approach: replace user message with a meta-prompt that
            # makes the LLM output the help text.
            last["content"] = (
                "Please output the following help text exactly as-is, "
                "with no additions:\n\n" + self._build_help_message()
            )
            return body

        # Look up agent
        agent_name = COMMAND_MAP.get(command)
        if agent_name is None:
            if self.valves.passthrough_unknown:
                return body  # not our command, let it through
            last["content"] = (
                f"Unknown command `/{command}`. Type `/help` to see available commands."
            )
            return body

        system_prompt = self._load_agent(agent_name)
        if system_prompt is None:
            last["content"] = (
                f"Agent `{agent_name}` not found. "
                f"Make sure the agents directory is correctly mounted at "
                f"`{self.valves.agents_dir}`."
            )
            return body

        # Replace or inject system message
        existing_system = next((m for m in messages if m["role"] == "system"), None)
        if existing_system:
            existing_system["content"] = system_prompt
        else:
            messages.insert(0, {"role": "system", "content": system_prompt})

        # Update user message — remove the slash command prefix
        if remainder:
            last["content"] = remainder
        else:
            last["content"] = "Please proceed with your role. Introduce yourself briefly."

        # Optionally prepend a visible banner (goes into the system prompt footer)
        if self.valves.show_activation_banner and self.valves.banner_prefix:
            agent_display = agent_name.replace("-", " ").title()
            banner = f"\n\n---\n{self.valves.banner_prefix}{agent_display}"
            # Append to system prompt so it's visible in the context
            existing_system = next((m for m in messages if m["role"] == "system"), None)
            if existing_system:
                existing_system["content"] += banner

        body["messages"] = messages
        return body

    # outlet is a no-op — we don't modify LLM responses
    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        return body
