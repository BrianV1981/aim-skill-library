# aim-skill-library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20solo%20dev-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/BrianV1981)

**Shareable A.I.M. skills — bodies in this repo, install into any vessel.**

| | |
|--|--|
| **Own your stack.** | Skills you can copy, fork, and keep when a vendor moves the goalposts. |
| **Ask, don’t thrash.** | Playbooks that tell agents *how* to work — not blind thrash loops. |

---

## Built by one person — not a SaaS

> **Solo developer.** No corporate budget. I share skills so more of us can run agents without renting every layer of the pipeline.

**Paywall fatigue** is real. **Rug-pulls** happen — pipelines change or get gated overnight; rebuilds hurt. **Micro-transactions add up.**  
**Hope, not hype:** open playbooks on *your* disk. Coffee is optional gratitude, never a paywall.

<p align="center">
  <a href="https://www.buymeacoffee.com/BrianV1981" target="_blank" rel="noopener noreferrer">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50" />
  </a>
</p>

---

## What this is

| This repo | Not this repo |
|-----------|----------------|
| **`skills/<id>/`** — real `SKILL.md` (+ scripts) | Pointer-only index with machine-local paths |
| Portable `scripts/install.sh` | Absolute install maps |
| Per-CLI manifests under `vessels/agy`, `vessels/grok`, `vessels/opencode`, … | One-size dump of every vertical |
| Featured **companion skills** (browser suite, Workspace, …) | Vendoring Chromium engines into this monorepo |

**Library skills** live here. **Companion skills** ship with heavier tools in their own repos — same desk, deliberate install (see below).

**Skills** teach tools. **Personas** teach roles. **Co-agents** are full peers spawned from blueprints — see **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** (`personas/` + `blueprints/`). Personas are **not** installed by this library.

---

## Quick install (this library)

```bash
git clone https://github.com/BrianV1981/aim-skill-library.git
cd aim-skill-library

# Grok vessel
./scripts/install.sh --vessel grok --dest /path/to/project/.grok/skills --mode symlink

# aim-agy (Antigravity / Gemini skills dir)
./scripts/install.sh --vessel agy --dest /path/to/aim-agy/.gemini/skills --mode symlink

# OpenCode
./scripts/install.sh --vessel opencode --dest /path/to/project/.opencode/skills --mode symlink
```

---

## Skills in this library

Installed by `./scripts/install.sh` from the `skills/` tree.

| Skill | Role |
|-------|------|
| **aim-communicate** | Inter-agent tmux protocol (`FROM` / `REPLY_TO`) |
| **aim-calc** | Stateful scientific calculator |
| **aim-memory-search** | Engram / hybrid search via `./aim` |
| **aim-list-sessions** | Map / list indexed work |
| **aim-export-cartridge** | Export memory cartridge |
| **aim-wiki** | Memory wiki (Grok-oriented) |
| **aim-grok-context** | aim-grok vessel context |

Manifests under `vessels/` choose the pack per CLI. Full index: [`registry/skills.yaml`](registry/skills.yaml).

---

## Companion skills (other repos)

These are **first-class A.I.M. skills**, but their code lives with the tool that powers them.  
`install.sh` here does **not** copy them — clone the companion, then install as shown.

### [aim-browser](https://github.com/BrianV1981/aim-browser) — headed CDP + skill suite

Persistent headed Chromium over CDP. Minimized by default; stop after session.

| Skill | Job |
|-------|-----|
| **aim-browser** | Full CDP exploration CLI |
| **aim-google-ai** | Google Search AI Mode (`udm=50`) |
| **aim-google-web** | Classic SERP / web-only |
| **aim-google-news** | News headlines |
| **aim-page-fetch** | URL → main text + meta |
| **aim-screenshot-url** | URL → PNG proof |
| **aim-youtube-meta** | YouTube watch-page metadata |
| **aim-maps-place** | Maps place card extract |
| **aim-google-ai-chat** | Multi-turn AI Mode |
| **aim-form-fill** | Allowlisted form fill |
| **aim-login-hold** | Human login / CAPTCHA hold |
| **aim-web-diff** | Page text snapshot diff |

```bash
git clone https://github.com/BrianV1981/aim-browser.git
cd aim-browser && npm install
npm run install-skills -- /path/to/project/.grok/skills --mode symlink
```

### [aim-google](https://github.com/BrianV1981/aim-google) — Workspace CLI

| Skill | Job |
|-------|-----|
| **aim-google** | Gmail, Drive, Calendar, Docs, Sheets, Tasks, Chat (API — not browser) |

Clone the repo and link `agent-skill/aim-google` (or that repo’s documented path) into your vessel skills dir.

### [aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)

| Skill | Job |
|-------|-----|
| **aim-flight-recorder** | Extract forensic Markdown from CLI sessions |

### [aim-coagents](https://github.com/BrianV1981/aim-coagents)

| Skill | Job |
|-------|-----|
| **aim-coagents** | DNA bank / blueprints for sovereign co-agents (equip when spawning peers) |

More install notes: [`docs/COMPANIONS.md`](docs/COMPANIONS.md).

---

## Layout

```text
skills/                 # library skill bodies (source of truth)
vessels/<cli>/manifest.txt
scripts/install.sh      # symlink or copy library skills into a vessel
registry/skills.yaml    # catalog + companion pointers
docs/COMPANIONS.md      # companion install notes
```

---

## Vessels

| Vessel | Host CLI | Typical skills path |
|--------|----------|---------------------|
| **agy** | Antigravity / aim-agy | `.gemini/skills/` |
| **grok** | Grok CLI | `.grok/skills/` |
| **opencode** | OpenCode | `.opencode/skills/` |
| **codex** | Codex (horizon) | stub manifest |

---

## Design rules

1. **No absolute home-directory paths** in skills or install scripts.  
2. **Public library only** — proprietary vertical playbooks stay out of this repo.  
3. **Skill body in-repo** or don’t list it as `type: library`.  
4. **Companions** install from their own repos after clone.  

---

## Support

**[Buy Me a Coffee →](https://www.buymeacoffee.com/BrianV1981)**

MIT — fork it, keep it, walk away with the files.

---

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

Modular A.I.M. (Actual Intelligent Memory) repositories. **Flagship engine: [aim-agy](https://github.com/BrianV1981/aim-agy).**

**Active vessels (CLI hosts):**
- **[aim-agy](https://github.com/BrianV1981/aim-agy)** — Core engine (Antigravity / post–Gemini-CLI line). *Flagship.* Memory, GitOps, `./aim`, co-agent spawn.
- **[aim-grok](https://github.com/BrianV1981/aim-grok)** — Grok CLI vessel (same engine DNA, Grok host).
- **[aim-opencode](https://github.com/BrianV1981/aim-opencode)** — OpenCode CLI vessel.
- **[aim-codex](https://github.com/BrianV1981/aim-codex)** — OpenAI Codex CLI vessel (greenfield nested soul + Codex overlays; primary `main`).

**Tools & workspaces:**
- **[aim-connect](https://github.com/BrianV1981/aim-connect)** — Self-hosted remote workspace web UI (tmux panes in the browser).
- **[aim-tmux-dashboard](https://github.com/BrianV1981/aim-tmux-dashboard)** — Terminal multi-session monitor.
- **[aim-browser](https://github.com/BrianV1981/aim-browser)** — Headed Chromium CDP engine + browser **skill suite**.
- **[aim-google](https://github.com/BrianV1981/aim-google)** — Google Workspace CLI (Gmail, Drive, Calendar, …).
- **[aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)** — Forensic Markdown session extractor.
- **[aim-boardroom](https://github.com/BrianV1981/aim-boardroom)** — Multi-agent orchestration room (OS multiplexing + artifacts).
- **[aim-skill-library](https://github.com/BrianV1981/aim-skill-library)** — **This repo** — shareable **tool skills** (communicate, calc, memory, …) + companion index.

**DNA, comms & lore:**
- **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** — DNA bank: **personas** (roles) + **blueprints** (sovereign co-agents).
- **[aim-knowledge](https://github.com/BrianV1981/aim-knowledge)** — Public Obsidian vault / deep-lore archive.
- **[aim-chalkboard](https://github.com/BrianV1981/aim-chalkboard)** — Optional cross-host async git mailbox (PoC; default same-host comms = **aim-communicate** skill).

**Horizon (not deprecated):**
- **[aim-antigravity](https://github.com/BrianV1981/aim-antigravity)** — IDE-line vessel (neglected since agy CLI; still on the map).

**Deprecated / not maintained:**
- **[aim](https://github.com/BrianV1981/aim)** — Original **Gemini CLI** framework. Deprecated after loss of practical subscription access; **Great Migration → aim-agy**.
- **[aim-swarm](https://github.com/BrianV1981/aim-swarm)** — Legacy Python swarm factory → use **aim-coagents** + aim-agy spawn.
- **aim-claude / Anthropic-line vessels** — **Done.** Operator does not develop against Anthropic. Use **aim-agy / aim-grok / aim-opencode / aim-codex**.
<!-- AIM_ECOSYSTEM_END -->
