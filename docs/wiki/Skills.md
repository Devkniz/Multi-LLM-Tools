# Skills

65 knowledge packs that guide the LLM on specific domains, frameworks, and workflows.  
Skills are markdown files in `skills/<name>/SKILL.md` — load them into your system prompt or reference them in your agent configuration.

**Tiers:**
- `local` — fully offline, no external services needed
- `internet` — requires external APIs (Exa, Context7, fal.ai, etc.)
- `meta` — tooling/configuration skills for the ECC ecosystem itself

---

## Testing & Quality

| Skill | Tier | Description |
|-------|------|-------------|
| `tdd-workflow` | local | Write-tests-first methodology: RED → GREEN → REFACTOR with 80%+ coverage |
| `e2e-testing` | local | Playwright E2E patterns, Page Object Model, CI/CD integration, flaky test strategies |
| `python-testing` | local | pytest patterns, fixtures, mocking, parametrization, coverage |
| `golang-testing` | local | Go testing with testify, table-driven tests, mock generation, benchmarks |
| `rust-testing` | local | Rust unit/integration tests, async testing, property-based testing, mocking |
| `kotlin-testing` | local | Kotest, MockK, coroutine testing, Kover coverage |
| `java-coding-standards` | local | Java standards based on Clean Code and Effective Java |
| `cpp-testing` | local | GoogleTest/CTest, sanitizers, coverage — use only for C++ test work |
| `perl-testing` | local | Test2::V0, Test::More, Devel::Cover coverage |
| `laravel-tdd` | local | PHPUnit and Pest for Laravel, factories, database testing |
| `django-tdd` | local | pytest-django, factory_boy, DRF API testing |
| `springboot-tdd` | local | JUnit 5, Mockito, MockMvc, Testcontainers, JaCoCo |
| `ai-regression-testing` | local | Regression testing strategies for AI-assisted development, sandbox API testing |
| `eval-harness` | local | Formal evaluation framework for Claude Code sessions (EDD principles) |
| `verification-loop` | local | Comprehensive verification system for Claude Code sessions |

---

## Security

| Skill | Tier | Description |
|-------|------|-------------|
| `security-review` | local | Security checklist and patterns for auth, user input, APIs, payment features |

---

## Languages & Frameworks — Backend

| Skill | Tier | Description |
|-------|------|-------------|
| `python-patterns` | local | Pythonic idioms, PEP 8, type hints, best practices |
| `golang-patterns` | local | Idiomatic Go, error handling, interfaces, concurrency |
| `rust-patterns` | local | Ownership, error handling, traits, concurrency, performance |
| `kotlin-patterns` | local | Idiomatic Kotlin, coroutines, null safety, DSL builders |
| `kotlin-coroutines-flows` | local | Coroutines, Flow, structured concurrency, StateFlow, SharedFlow |
| `kotlin-ktor-patterns` | local | Ktor routing DSL, plugins, auth, Koin DI, WebSockets |
| `kotlin-exposed-patterns` | local | JetBrains Exposed ORM, DSL queries, DAO, HikariCP, Flyway |
| `perl-patterns` | local | Modern Perl 5.36+ idioms, best practices |
| `cpp-coding-standards` | local | C++ Core Guidelines, modern C++ idioms |
| `java-coding-standards` | local | Java standards based on Clean Code and Effective Java |
| `backend-patterns` | local | Node.js, Express, Next.js API routes — architecture, DB, caching |
| `api-design` | local | REST resource naming, status codes, pagination, versioning, rate limiting |
| `mcp-server-patterns` | local | MCP servers with Node/TypeScript SDK — tools, resources, Zod validation |
| `bun-runtime` | local | Bun as runtime, package manager, bundler, test runner |

---

## Languages & Frameworks — Frontend

| Skill | Tier | Description |
|-------|------|-------------|
| `frontend-patterns` | local | React, Next.js, state management, performance, UI best practices |
| `nextjs-turbopack` | local | Next.js 16+, Turbopack — incremental bundling, FS caching |
| `coding-standards` | local | Universal standards for TypeScript, JavaScript, React, Node.js |
| `frontend-slides` | local | HTML presentation creation from scratch or from PowerPoint files |

---

## Mobile & Cross-Platform

| Skill | Tier | Description |
|-------|------|-------------|
| `android-clean-architecture` | local | Clean Architecture for Android/KMP — modules, UseCases, Repositories |
| `compose-multiplatform-patterns` | local | Compose Multiplatform for KMP — state, navigation, theming, platform UI |

---

## Databases

| Skill | Tier | Description |
|-------|------|-------------|
| `django-patterns` | local | Django architecture, DRF, ORM, caching, signals, middleware |
| `laravel-patterns` | local | Laravel architecture, Eloquent, queues, events, API resources |
| `springboot-patterns` | local | Spring Boot REST, layered services, caching, async, logging |

---

## Verification & DevOps

| Skill | Tier | Description |
|-------|------|-------------|
| `django-verification` | local | Django verification loop: migrations, linting, tests, security scans |
| `laravel-verification` | local | Laravel verification loop before release or PR |
| `springboot-verification` | local | Spring Boot verification: build, static analysis, tests, coverage |
| `plankton-code-quality` | local | Write-time code quality with Plankton — auto-format, lint, fix on edit |
| `strategic-compact` | local | Context compaction suggestions at logical intervals |

---

## Content & Writing

| Skill | Tier | Description |
|-------|------|-------------|
| `article-writing` | local | Long-form content — articles, guides, blog posts, tutorials |
| `content-engine` | internet | Platform-native content for X, LinkedIn, TikTok, YouTube, newsletters |
| `crosspost` | internet | Multi-platform distribution across X, LinkedIn, Threads, Bluesky |
| `x-api` | internet | X/Twitter API — posting tweets, threads, timelines, analytics |
| `investor-materials` | local | Pitch decks, financial models, investor documentation |
| `investor-outreach` | local | Investor outreach strategy, email templates, follow-up sequences |
| `market-research` | internet | Market sizing, competitive analysis, industry intelligence with sources |

---

## AI & Research

| Skill | Tier | Description |
|-------|------|-------------|
| `deep-research` | internet | Multi-source research via firecrawl + Exa MCPs, cited reports |
| `exa-search` | internet | Neural search via Exa MCP — web, code, company research |
| `documentation-lookup` | internet | Up-to-date library docs via Context7 MCP |
| `search-first` | internet | Research-before-coding workflow — find existing solutions first |
| `claude-api` | local | Anthropic Claude API patterns — streaming, tool use, caching, batches |
| `fal-ai-media` | internet | AI media generation via fal.ai — images, video, audio |
| `video-editing` | internet | AI video editing — FFmpeg, Remotion, ElevenLabs, fal.ai pipeline |

---

## Learning & Meta

| Skill | Tier | Description |
|-------|------|-------------|
| `continuous-learning` | local | Extract reusable patterns from Claude Code sessions automatically |
| `continuous-learning-v2` | local | Instinct-based learning with confidence scoring, project-scoped |
| `configure-ecc` | meta | Interactive installer for Everything Claude Code |
| `everything-claude-code` | meta | ECC development conventions and project patterns |
| `skill-stocktake` | internet | Audit skill quality — Quick Scan or Full Stocktake modes |

---

## How to Use a Skill

Skills are used differently per platform:

**Claude Code / any LLM via system prompt:**
```bash
# Read the skill content and include it in your system prompt
cat skills/python-patterns/SKILL.md
```

**OpenWebUI (manual):**
Paste the skill content into a system prompt in the model settings.

**via query_agent.py:**
```bash
python scripts/query_agent.py --agent python-reviewer --skill python-patterns --message "Review this code"
```

See [Configuration](Configuration) for how to wire skills into agents.
