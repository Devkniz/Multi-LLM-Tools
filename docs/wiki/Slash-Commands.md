# Slash Commands Reference

Slash commands are available in **OpenWebUI** (via the native Function Filter) and **continue.dev** (via config fragment).  
Type a command at the start of your message, optionally followed by your request.

```
/plan Build a REST API with JWT authentication
/review                    ← paste code in the message body
/help                      ← list all commands
```

---

## All Commands

### Planning & Architecture

| Command | Aliases | Agent | Description |
|---------|---------|-------|-------------|
| `/plan` | `/planner` | planner | Create an implementation plan for a feature or refactor |
| `/architect` | `/arch` | architect | System design, architecture decisions, API contracts |

**Examples:**
```
/plan Migrate our monolith to microservices — start with the auth service
/architect Design a real-time notification system for 100k concurrent users
```

---

### Code Review

| Command | Aliases | Agent | Description |
|---------|---------|-------|-------------|
| `/review` | `/cr` | code-reviewer | Generic code review (all languages) |
| `/python` | `/py` | python-reviewer | Python — PEP 8, type hints, idioms |
| `/typescript` | `/ts`, `/js` | typescript-reviewer | TypeScript/JS — type safety, async, security |
| `/go` | `/golang` | go-reviewer | Go — idiomatic patterns, concurrency |
| `/rust` | | rust-reviewer | Rust — ownership, lifetimes, unsafe |
| `/java` | | java-reviewer | Java/Spring Boot — JPA, architecture |
| `/kotlin` | | kotlin-reviewer | Kotlin/Android — coroutines, Compose |
| `/cpp` | `/c++` | cpp-reviewer | C++ — memory safety, modern idioms |
| `/flutter` | `/dart` | flutter-reviewer | Flutter/Dart — widgets, state, null safety |
| `/db` | `/database`, `/sql` | database-reviewer | PostgreSQL — queries, schema, migrations |

**Examples:**
```
/review
[paste your code here]

/python
def get_user(id):
    return db.execute(f"SELECT * FROM users WHERE id = {id}")

/ts Check this React hook for memory leaks
```

---

### Build Error Fixers

| Command | Agent | Description |
|---------|-------|-------------|
| `/build` or `/fix` | build-error-resolver | TypeScript / generic build errors |
| `/gobuild` | go-build-resolver | Go compilation errors |
| `/rustbuild` | rust-build-resolver | Cargo / borrow checker errors |
| `/cpbuild` | cpp-build-resolver | CMake, linker, template errors |
| `/javabuild` | java-build-resolver | Maven/Gradle failures |
| `/kotlinbuild` | kotlin-build-resolver | Kotlin/Gradle errors |
| `/pytorch` | pytorch-build-resolver | CUDA, tensor shape, DataLoader errors |

**Examples:**
```
/build
error TS2345: Argument of type 'string | undefined' is not assignable to parameter of type 'string'

/rustbuild
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
```

---

### Testing

| Command | Aliases | Agent | Description |
|---------|---------|-------|-------------|
| `/tdd` | `/test` | tdd-guide | Test-Driven Development — write tests first |
| `/e2e` | | e2e-runner | E2E tests with Playwright |

**Examples:**
```
/tdd Implement a password reset flow
/e2e Generate E2E tests for the checkout flow
```

---

### Security & Quality

| Command | Aliases | Agent | Description |
|---------|---------|-------|-------------|
| `/security` | `/sec` | security-reviewer | Security audit — OWASP, secrets, injection |
| `/refactor` | `/clean` | refactor-cleaner | Remove dead code, consolidate duplicates |
| `/doc` | `/docs` | doc-updater | Update documentation and codemaps |

**Examples:**
```
/security Review this authentication middleware
/refactor Find and remove dead code in the utils/ directory
/doc Update the README to reflect the new API endpoints
```

---

### Operations

| Command | Aliases | Agent | Description |
|---------|---------|-------|-------------|
| `/loop` | | loop-operator | Autonomous agent loop control |
| `/harness` | | harness-optimizer | Agent harness configuration |
| `/cos` | | chief-of-staff | Email/Slack/comm triage |

---

### Meta

| Command | Description |
|---------|-------------|
| `/help` | Display all available commands with descriptions |

---

## Tips

**No message needed:** Some agents work on the conversation context.
```
/security          ← reviews the code already in the conversation
/review            ← reviews the last code block discussed
```

**Combined workflow:**
```
1. /plan Build a user authentication system with OAuth
2. /tdd             ← guides you through writing tests first  
3. /security        ← audits the implementation
4. /review          ← final code review before merge
```

**Case-insensitive:** `/Plan`, `/PLAN`, and `/plan` all work.

**Unknown commands:** Unknown commands are passed through unchanged (configurable in the Function's Valves).

---

## Platform Support

| Feature | OpenWebUI | continue.dev | Aider | Ollama |
|---------|-----------|-------------|-------|--------|
| Slash commands | Yes (Function Filter) | Yes (config fragment) | No | No |
| All 27 agents | Yes | Yes | N/A | 7 Modelfiles |
| Works offline | Yes | Yes | Yes | Yes |

See [OpenWebUI Integration](OpenWebUI-Integration) and [continue.dev Integration](continue.dev-Integration) for setup.
