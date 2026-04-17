# Agents

28 agents extracted from Everything Claude Code and adapted for any LLM backend.  
27 work fully offline — only `docs-lookup` requires internet (Context7 MCP).

**Model tiers** map to entries in `config.yaml`:
- `best` → your strongest model (planning, architecture)
- `mid` → your balanced model (reviews, tests, security)
- `fast` → your lightest model (docs, quick fixes)

---

## Planning & Architecture

### `planner`
| | |
|---|---|
| **OpenWebUI command** | `/plan` or `/planner` |
| **Model tier** | best |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search |

Expert planning specialist for complex features and refactoring. Analyzes requirements, breaks down features into phases, identifies dependencies and risks, and produces actionable task lists. Use proactively before any significant implementation — it saves time by surfacing design issues before they become code issues.

**Best for:** New features, large refactors, migrating between frameworks, estimating work.

---

### `architect`
| | |
|---|---|
| **OpenWebUI command** | `/architect` or `/arch` |
| **Model tier** | best |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search |

Software architecture specialist for system design, scalability, and technical decision-making. Evaluates trade-offs between patterns (monolith vs microservices, SQL vs NoSQL, sync vs async), proposes data models, API contracts, and module boundaries. Use when the scope of a change affects multiple systems.

**Best for:** System design, API contracts, database schema design, tech stack decisions.

---

## Code Review — Generic

### `code-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/review` or `/cr` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Expert code review specialist for quality, security, and maintainability. Reviews code across all languages for common issues: missing error handling, security vulnerabilities, naming clarity, test coverage gaps, unnecessary complexity, and SOLID violations. Classifies findings as CRITICAL / HIGH / MEDIUM / LOW.

**Best for:** PR review, code audit before merge, reviewing AI-generated code.

---

## Code Review — Language-Specific

### `python-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/python` or `/py` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Checks for mutable default arguments, incorrect use of `is` vs `==`, missing type annotations, inefficient list comprehensions, and common security issues like unsafe `eval()` usage.

---

### `typescript-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/typescript` or `/ts` or `/js` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

TypeScript/JavaScript reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Flags `any` abuse, missing `await`, prototype pollution, XSS vectors, and unsafe use of `eval()` or `innerHTML`. Covers both frontend (React) and backend (Node.js) patterns.

---

### `go-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/go` or `/golang` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Go code reviewer specializing in idiomatic Go, concurrency patterns, and error handling. Catches goroutine leaks, unchecked errors, missing context propagation, improper mutex usage, and violations of the Go proverbs. Enforces `gofmt` / `golangci-lint` conventions.

---

### `rust-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/rust` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Rust code reviewer specializing in ownership, lifetimes, error handling, unsafe usage, and idiomatic patterns. Reviews borrow checker soundness, unnecessary clones, `unwrap()` abuse, missing `?` propagation, and `unsafe` blocks without justification.

---

### `java-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/java` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Java and Spring Boot code reviewer specializing in layered architecture, JPA patterns, security, and concurrency. Catches N+1 queries, missing `@Transactional`, incorrect `equals()`/`hashCode()`, thread safety issues, and Spring anti-patterns like field injection.

---

### `kotlin-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/kotlin` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Kotlin and Android/KMP code reviewer. Reviews coroutine safety (`GlobalScope` misuse, missing `SupervisorJob`), Compose best practices, `!!` operator abuse, clean architecture violations, and common Android pitfalls like context leaks and blocking the main thread.

---

### `cpp-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/cpp` or `/c++` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

C++ code reviewer specializing in memory safety, modern C++ idioms, concurrency, and performance. Flags raw pointer usage where smart pointers are appropriate, missing RAII patterns, undefined behavior, data races, and violations of the C++ Core Guidelines.

---

### `flutter-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/flutter` or `/dart` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec |

Flutter and Dart code reviewer. Reviews widget best practices (avoiding `setState` abuse, correct `const` usage), state management patterns, Dart null safety idioms, performance pitfalls (rebuilds, heavy `build()` methods), and accessibility issues. Library-agnostic.

---

### `database-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/db` or `/database` or `/sql` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search, file_search |

PostgreSQL specialist for query optimization, schema design, security, and performance. Identifies missing indexes, N+1 query patterns, unsafe raw SQL, non-transactional migrations, and schema design issues. Incorporates Supabase best practices (RLS, connection pooling via PgBouncer).

---

## Build Error Fixers

### `build-error-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/build` or `/fix` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search, file_search |

Build and TypeScript error resolution specialist. Fixes build and type errors with minimal diffs — no architectural changes. Focuses on getting the build green quickly: resolves type mismatches, missing imports, version conflicts, and configuration issues.

---

### `go-build-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/gobuild` |
| **Model tier** | mid |
| **Offline** | Yes |

Go build, vet, and compilation error specialist. Fixes import cycles, type errors, `go vet` warnings, and linter issues with minimal changes.

---

### `rust-build-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/rustbuild` |
| **Model tier** | mid |
| **Offline** | Yes |

Rust build and compilation specialist. Resolves `cargo build` errors, borrow checker violations, and `Cargo.toml` dependency issues with minimal changes.

---

### `cpp-build-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/cpbuild` |
| **Model tier** | mid |
| **Offline** | Yes |

C++ build specialist. Fixes CMake errors, linker failures, template instantiation errors, and include path issues.

---

### `java-build-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/javabuild` |
| **Model tier** | mid |
| **Offline** | Yes |

Java/Maven/Gradle build specialist. Fixes compilation errors, dependency conflicts, and build tool configuration issues for Java and Spring Boot projects.

---

### `kotlin-build-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/kotlinbuild` |
| **Model tier** | mid |
| **Offline** | Yes |

Kotlin/Gradle build specialist. Resolves Kotlin compiler errors, Gradle sync issues, and dependency resolution failures.

---

### `pytorch-build-resolver`
| | |
|---|---|
| **OpenWebUI command** | `/pytorch` |
| **Model tier** | mid |
| **Offline** | Yes |

PyTorch runtime and CUDA error specialist. Fixes tensor shape mismatches, device placement errors (`cpu` vs `cuda`), gradient graph issues, DataLoader problems, and mixed precision (`autocast`) failures.

---

## Testing

### `tdd-guide`
| | |
|---|---|
| **OpenWebUI command** | `/tdd` or `/test` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search |

Test-Driven Development specialist enforcing write-tests-first methodology. Guides through the RED → GREEN → REFACTOR cycle: writes failing tests first, implements minimal code to pass, then refactors. Targets 80%+ coverage including unit, integration, and E2E tests.

**Best for:** Any new feature or bug fix. Use it BEFORE writing implementation code.

---

### `e2e-runner`
| | |
|---|---|
| **OpenWebUI command** | `/e2e` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search, file_search |

End-to-end testing specialist using Playwright. Generates and maintains E2E test suites for critical user flows, manages test journeys, quarantines flaky tests, and uploads artifacts (screenshots, videos, traces) on failure.

---

## Security & Quality

### `security-reviewer`
| | |
|---|---|
| **OpenWebUI command** | `/security` or `/sec` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search, file_search |

Security vulnerability detection and remediation specialist. Proactively reviews code handling user input, authentication, API endpoints, or sensitive data. Flags hardcoded secrets, SSRF, SQL injection, XSS, unsafe crypto, CSRF gaps, and OWASP Top 10 vulnerabilities. Classifies findings by severity.

---

### `refactor-cleaner`
| | |
|---|---|
| **OpenWebUI command** | `/refactor` or `/clean` |
| **Model tier** | mid |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search, file_search |

Dead code cleanup and consolidation specialist. Runs analysis tools (knip, depcheck, ts-prune) to identify unused exports, dead imports, and duplicate logic. Removes safely — no functional changes.

---

### `doc-updater`
| | |
|---|---|
| **OpenWebUI command** | `/doc` or `/docs` |
| **Model tier** | fast |
| **Offline** | Yes |
| **Tools** | file_read, file_write, file_edit, shell_exec, search, file_search |

Documentation and codemap specialist. Updates READMEs, generates `docs/CODEMAPS/*`, and keeps documentation synchronized with code changes.

---

## Operations

### `loop-operator`
| | |
|---|---|
| **OpenWebUI command** | `/loop` |
| **Model tier** | mid |
| **Offline** | Yes |

Operates autonomous agent loops, monitors progress, and intervenes safely when loops stall or diverge.

---

### `harness-optimizer`
| | |
|---|---|
| **OpenWebUI command** | `/harness` |
| **Model tier** | mid |
| **Offline** | Yes |

Analyzes and improves the local agent harness configuration for reliability, cost efficiency, and throughput.

---

### `chief-of-staff`
| | |
|---|---|
| **OpenWebUI command** | `/cos` |
| **Model tier** | best |
| **Offline** | Yes |
| **Tools** | file_read, search, file_search, shell_exec, file_edit, file_write |

Personal communication chief of staff. Triages email, Slack, LINE, and Messenger by classifying messages into four tiers: `skip`, `info_only`, `meeting_info`, `action_required`. Generates draft replies and tracks follow-through.

---

## Internet-Required

### `docs-lookup`
| | |
|---|---|
| **Model tier** | mid |
| **Offline** | **No** — requires Context7 MCP |
| **Tools** | file_read, search, mcp__context7__resolve-library-id, mcp__context7__query-docs |

Fetches up-to-date library and framework documentation via Context7 MCP instead of relying on training data. Use for setup questions, API references, and code examples when you need current information.
