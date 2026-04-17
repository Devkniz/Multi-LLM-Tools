# Multi LLM Tools

> **Boîte à outils d'agents LLM-agnostique** — utilisez des agents IA puissants avec n'importe quel LLM local ou cloud.  
> Compatible Ollama, OpenWebUI, LM Studio, Aider, continue.dev, et toute API compatible OpenAI.  
> Extrait et étendu depuis [Everything Claude Code](https://github.com/steipete/everything-claude-code).

[**English version**](README.md) | [**Wiki**](https://github.com/Devkniz/Multi-LLM-Tools/wiki)

---

## Contenu

| Catégorie | Total | Utilisable hors ligne |
|-----------|-------|----------------------|
| Agents    | 28    | **27** (seul `docs-lookup` nécessite internet) |
| Skills    | 65    | **52** (10 nécessitent internet, 3 sont méta) |
| Règles    | 74    | **74** (toutes hors ligne) |

---

## Démarrage rapide

### 1. Cloner le repo

```bash
git clone https://github.com/Devkniz/Multi-LLM-Tools.git
cd Multi-LLM-Tools
```

### 2. Configurer le backend LLM

Modifier `config.yaml` :

```yaml
llm_backend:
  base_url: "http://localhost:11434/v1"   # Ollama (par défaut)
  # base_url: "http://localhost:1234/v1"  # LM Studio
  # base_url: "http://localhost:8080/v1"  # llama.cpp server

model_mapping:
  best: "qwen2.5-coder:32b"   # planner, architect, chief-of-staff
  mid:  "qwen2.5-coder:14b"   # code-reviewer, tdd-guide, security-reviewer
  fast: "qwen2.5-coder:7b"    # build-error-resolver, doc-updater
```

### 3. Lancer un premier agent

```bash
python scripts/query_agent.py --agent planner --message "Planifier une REST API pour une app todo"

# Lister tous les agents disponibles
python scripts/query_agent.py --list
```

---

## Intégrations

### OpenWebUI — Commandes slash natives

Installez la Filter Pipeline pour utiliser `/plan`, `/review`, `/tdd` et plus directement dans le chat :

```
/plan Construire une REST API avec authentification JWT
/review              ← coller votre code dans le message
/tdd Écrire un module d'authentification utilisateur
/security            ← auditer la conversation courante
/help                ← lister toutes les commandes disponibles
```

**Installation rapide (Docker Compose) :**

```yaml
services:
  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    volumes:
      - ./prompts/openwebui/slash_commands_pipeline.py:/app/pipelines/slash_commands_pipeline.py
      - ./agents:/app/pipelines/agents
    ports:
      - "9099:9099"
```

Puis dans OpenWebUI → **Paramètres → Admin → Pipelines** → définir l'URL sur `http://pipelines:9099`.

Voir [`prompts/openwebui/README.md`](prompts/openwebui/README.md) pour le guide complet.

---

### Ollama — Modèles spécialisés

Créez des modèles dédiés avec les system prompts intégrés :

```bash
# Créer le modèle (modifier le Modelfile pour définir votre modèle de base d'abord)
ollama create planner        -f prompts/ollama/planner.Modelfile
ollama create code-reviewer  -f prompts/ollama/code-reviewer.Modelfile
ollama create tdd-guide      -f prompts/ollama/tdd-guide.Modelfile

# Utiliser
ollama run planner
```

Modelfiles disponibles : `planner`, `architect`, `build-error-resolver`, `refactor-cleaner`,
`tdd-guide`, `code-reviewer`, `security-reviewer`.

---

### Aider

```bash
# Charger n'importe quel agent comme system prompt
aider --system-prompt-file prompts/aider/planner.txt
aider --system-prompt-file prompts/aider/code-reviewer.txt
```

Voir [`prompts/aider/usage-examples.sh`](prompts/aider/usage-examples.sh) pour tous les exemples.

---

### continue.dev (VS Code / JetBrains)

1. Ouvrir `~/.continue/config.json`
2. Fusionner le tableau `slashCommands` depuis [`prompts/continue/config-fragment.json`](prompts/continue/config-fragment.json)
3. Recharger votre IDE

Puis utiliser `/planner`, `/code-reviewer`, `/tdd-guide`, etc. directement dans le panneau Continue.

---

### LM Studio

1. Démarrer LM Studio et activer le serveur local (`http://localhost:1234`)
2. Mettre à jour `config.yaml` : `base_url: "http://localhost:1234/v1"`
3. Utiliser `python scripts/query_agent.py` ou POST les payloads JSON depuis `prompts/openai-compatible/`

---

## Agents disponibles (27 hors ligne)

### Planification & Architecture

| Agent | Commande OpenWebUI | Tier | Description |
|-------|-------------------|------|-------------|
| `planner` | `/plan` | best | Planification d'implémentation pour features et refactoring |
| `architect` | `/architect` | best | Design système et décisions architecturales |

### Revue de code — Générique

| Agent | Commande OpenWebUI | Tier | Description |
|-------|-------------------|------|-------------|
| `code-reviewer` | `/review` | mid | Qualité, sécurité et maintenabilité |

### Revue de code — Par langage

| Agent | Commande | Tier | Description |
|-------|----------|------|-------------|
| `python-reviewer` | `/python` | mid | PEP 8, type hints, idiomes Pythoniques |
| `typescript-reviewer` | `/typescript` | mid | Type safety, async, sécurité Node/web |
| `go-reviewer` | `/go` | mid | Go idiomatique, concurrence, gestion d'erreurs |
| `rust-reviewer` | `/rust` | mid | Ownership, lifetimes, unsafe |
| `java-reviewer` | `/java` | mid | Spring Boot, JPA, architecture en couches |
| `kotlin-reviewer` | `/kotlin` | mid | Coroutines, Compose, KMP |
| `cpp-reviewer` | `/cpp` | mid | Sécurité mémoire, idiomes C++ modernes |
| `flutter-reviewer` | `/flutter` | mid | Widgets, gestion d'état, idiomes Dart |
| `database-reviewer` | `/db` | mid | PostgreSQL, schéma, optimisation de requêtes |

### Correcteurs d'erreurs de build

| Agent | Commande | Tier | Description |
|-------|----------|------|-------------|
| `build-error-resolver` | `/build` | mid | Erreurs de build et TypeScript |
| `go-build-resolver` | `/gobuild` | mid | Erreurs de compilation Go |
| `rust-build-resolver` | `/rustbuild` | mid | Erreurs Cargo / borrow checker |
| `cpp-build-resolver` | `/cpbuild` | mid | Erreurs CMake, linker, templates |
| `java-build-resolver` | `/javabuild` | mid | Échecs de build Maven/Gradle |
| `kotlin-build-resolver` | `/kotlinbuild` | mid | Erreurs Kotlin/Gradle |
| `pytorch-build-resolver` | `/pytorch` | mid | Erreurs CUDA, forme de tenseur, DataLoader |

### Tests

| Agent | Commande | Tier | Description |
|-------|----------|------|-------------|
| `tdd-guide` | `/tdd` | mid | Test-Driven Development, écrire les tests en premier |
| `e2e-runner` | `/e2e` | mid | Tests E2E avec Playwright |

### Sécurité & Qualité

| Agent | Commande | Tier | Description |
|-------|----------|------|-------------|
| `security-reviewer` | `/security` | mid | OWASP, secrets, injection, XSS |
| `refactor-cleaner` | `/refactor` | mid | Suppression de code mort, consolidation |
| `doc-updater` | `/doc` | fast | Mises à jour de documentation |

### Opérations

| Agent | Commande | Tier | Description |
|-------|----------|------|-------------|
| `loop-operator` | `/loop` | mid | Contrôle de boucles d'agents autonomes |
| `harness-optimizer` | `/harness` | mid | Configuration du harness d'agents |
| `chief-of-staff` | `/cos` | best | Tri d'emails/Slack/communications |

**Nécessite internet :** `docs-lookup` (Context7 MCP)

---

## Système de règles

74 directives de code organisées par langage :

```
rules/
├── common/          # Principes universels
│   ├── coding-style.md
│   ├── testing.md
│   ├── security.md
│   └── ...
├── python/
├── typescript/
├── golang/
├── rust/
└── ...
```

Copiez les répertoires pertinents dans le dossier `.claude/rules/` de votre projet.

---

## Recommandations de modèles

| Cas d'usage | RAM min | Modèles recommandés |
|-------------|---------|---------------------|
| Corrections de build, docs | 8 Go | qwen2.5-coder:7b, codellama:7b |
| Revue de code, TDD | 16 Go | qwen2.5-coder:14b, deepseek-coder:6.7b |
| Planification, architecture | 32 Go | qwen2.5-coder:32b, deepseek-coder-v2:33b |

---

## Structure des répertoires

```
Multi-LLM-Tools/
├── config.yaml                        ← Config backend LLM & modèles
├── agents/                            ← System prompts des agents
├── skills/                            ← Packs de connaissances
├── rules/                             ← Directives de code
├── prompts/
│   ├── openwebui/                     ← Filter Pipeline + guide
│   ├── aider/                         ← Fichiers .txt system prompt
│   ├── continue/                      ← Fragment config.json
│   ├── ollama/                        ← Modelfiles
│   └── openai-compatible/             ← Payloads JSON
├── docs/
│   └── tool-mapping.md
└── scripts/
    ├── query_agent.py                 ← Runner d'agents CLI
    ├── extract.py                     ← Ré-extraction depuis ECC
    └── validate.py                    ← Vérification hors ligne
```

---

[**English version →**](README.md)
