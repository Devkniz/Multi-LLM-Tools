# Rules System

74 coding guidelines organized into a layered system: universal `common/` rules plus language-specific overrides.  
All 74 rules work fully offline — no external services required.

---

## Structure

```
rules/
├── common/                  # Universal principles (all languages)
│   ├── coding-style.md      # Immutability, file organization, error handling
│   ├── testing.md           # 80% coverage, TDD, test types
│   ├── security.md          # Secret management, OWASP checklist
│   ├── git-workflow.md      # Commit format, PR process
│   ├── development-workflow.md  # Research → Plan → TDD → Review → Commit
│   ├── performance.md       # Model selection, context management
│   ├── patterns.md          # Repository pattern, API response format
│   ├── hooks.md             # Pre/PostToolUse hooks, TodoWrite
│   └── agents.md            # Agent orchestration, parallel execution
│
├── typescript/              # TypeScript / JavaScript specific
│   ├── coding-style.md
│   ├── testing.md
│   ├── security.md
│   ├── patterns.md
│   └── hooks.md
│
├── python/                  # Python specific
├── golang/                  # Go specific
├── rust/                    # Rust specific
├── java/                    # Java / Spring Boot specific
├── kotlin/                  # Kotlin / Android / KMP specific
├── cpp/                     # C++ specific
├── swift/                   # Swift / iOS specific
├── php/                     # PHP / Laravel specific
├── perl/                    # Perl specific
└── csharp/                  # C# / .NET specific
```

---

## Installation

### Copy to a project

```bash
# Universal rules (always install)
cp -r rules/common ~/.claude/rules/common

# Add language-specific rules for your project
cp -r rules/typescript ~/.claude/rules/typescript
cp -r rules/python ~/.claude/rules/python
cp -r rules/golang ~/.claude/rules/golang
```

**Important:** Copy entire directories — do NOT flatten with `/*`.  
Language directories contain files with the same names as `common/` — flattening overwrites common rules.

### Using the install script

```bash
# Install common + one language
python scripts/extract.py --install typescript

# Install multiple languages
python scripts/extract.py --install typescript python golang
```

---

## Common Rules Overview

### `coding-style.md`
- **Immutability**: Always create new objects, never mutate in place
- **File size**: 200-400 lines typical, 800 max
- **Functions**: Under 50 lines
- **Nesting**: Max 4 levels deep
- **Error handling**: Explicit at every level, never swallow errors
- **No hardcoded values**: Use constants or config

### `testing.md`
- **Minimum 80% coverage** — non-negotiable
- **All test types required**: unit, integration, E2E
- **TDD workflow mandatory**: write test first (RED), implement (GREEN), refactor
- Agent: use `tdd-guide` proactively for all new features

### `security.md`
- Mandatory checklist before every commit
- No hardcoded secrets — use environment variables
- Parameterized queries only — no string interpolation in SQL
- Sanitize all HTML output
- Rate limiting on all endpoints
- If issue found: STOP → use `security-reviewer` agent → fix → rotate secrets

### `git-workflow.md`
- Commit format: `<type>: <description>` (feat, fix, refactor, docs, test, chore, perf, ci)
- PR: analyze full commit history, comprehensive summary, include test plan

### `development-workflow.md`
Full pipeline:
1. **Research** — GitHub search, library docs, package registries before writing anything
2. **Plan** — use `planner` agent, generate PRD/architecture/task_list
3. **TDD** — use `tdd-guide` agent, write tests first
4. **Code Review** — use `code-reviewer` agent immediately after writing code
5. **Commit** — follow git-workflow.md

### `agents.md`
- Use agents proactively — no user prompt needed
- Complex feature → `planner`, code written → `code-reviewer`, new feature → `tdd-guide`
- Run independent agents **in parallel**

---

## Rule Priority

Language-specific rules override common rules where they conflict.  
Example: `common/coding-style.md` recommends immutability; `golang/coding-style.md` allows pointer receivers for struct mutation (idiomatic Go).

---

## Available Languages

| Directory | Languages / Frameworks |
|-----------|----------------------|
| `typescript/` | TypeScript, JavaScript, Node.js, React, Next.js |
| `python/` | Python 3.x, FastAPI, Django, Flask |
| `golang/` | Go |
| `rust/` | Rust |
| `java/` | Java 17+, Spring Boot |
| `kotlin/` | Kotlin, Android, KMP |
| `cpp/` | C++17/20, CMake |
| `swift/` | Swift, iOS, SwiftUI |
| `php/` | PHP 8+, Laravel |
| `perl/` | Perl 5.36+ |
| `csharp/` | C#, .NET |
