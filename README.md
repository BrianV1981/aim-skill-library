# aim-skill-library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20solo%20dev-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/BrianV1981)

**Shareable A.I.M. skills — bodies in this repo, install into any vessel.**

| | |
|--|--|
| **Own your stack.** | Skills you can copy, fork, and keep when a vendor moves the goalposts. |
| **Ask, don’t thrash.** | Playbooks that tell agents *how* to work — not blind thrash loops. |
| **Dual vessel.** | **Grok CLI** and **AGY** packs; Grok improvements must not strip AGY tools/paths. |

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
| Portable `scripts/install.sh` | Absolute install maps / hardcoded home usernames |
| Per-CLI manifests under `vessels/agy`, `vessels/grok`, `vessels/opencode`, … | One-size dump of every vertical |
| Featured **companion skills** (browser suite, Workspace, flight recorder, …) | Vendoring Chromium engines into this monorepo |

**Library skills** live here. **Companion skills** ship with heavier tools in their own repos — same desk, deliberate install (see below).

**Skills** teach tools. **Personas** teach roles. **Co-agents** are full peers spawned from blueprints — see **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** (`personas/` + `blueprints/`). Personas are **not** installed by this library.

---

## Quick install (this library)

Paths are **portable** — use your project root or `~`. Do **not** hardcode machine usernames or `/home/<user>/…`.

```bash
git clone https://github.com/BrianV1981/aim-skill-library.git
cd aim-skill-library

# Grok vessel (project-local)
./scripts/install.sh --vessel grok --dest "${PROJECT_ROOT:-.}/.grok/skills" --mode symlink
# or user-global:  --dest "$HOME/.grok/skills"

# AGY / Antigravity (project-local)
./scripts/install.sh --vessel agy --dest "${PROJECT_ROOT:-.}/.gemini/skills" --mode symlink
# or AGY CLI skills: --dest "$HOME/.gemini/antigravity-cli/skills"

# OpenCode
./scripts/install.sh --vessel opencode --dest "${PROJECT_ROOT:-.}/.opencode/skills" --mode symlink
```

`--mode symlink` (default) or `copy`. Ensure the host CLI scans that skills directory.

---

## Skills in this library

Installed by `./scripts/install.sh` from the `skills/` tree. Pack membership is per vessel (`vessels/<cli>/manifest.txt`).

| Skill | Role | Typical vessels |
|-------|------|-----------------|
| **aim-communicate** | Inter-agent tmux protocol (`FROM` / `REPLY_TO`) | agy, grok, opencode |
| **aim-calc** | Stateful scientific calculator | agy, grok, opencode, codex |
| **aim-memory-search** | Engram / hybrid search via `./aim` | agy, grok, opencode |
| **aim-list-sessions** | Map / list indexed work | agy, grok, opencode |
| **aim-export-cartridge** | Export memory cartridge | agy, grok, opencode |
| **aim-memory-wiki** | Session ingest into `memory-wiki/` (replaces deprecated `aim-wiki`) | agy, grok, opencode |
| **aim-handoff** | Ephemeral Engineering Handoff (sections 0–9) + optional tmux baton | agy, grok, opencode |
| **aim-grok-context** | aim-grok vessel context | **grok only** |
| **aim-bwrap-forge** | bubblewrap sandbox forge + optional tmux isolation | agy, grok, opencode, codex |
| **aim-mega-guide** | Single-source Mega Guide / SOP from long-form transcript | agy, grok, opencode |

Full catalog: [`registry/skills.yaml`](registry/skills.yaml).

### Dual vessel (Grok + AGY)

- Host-specific tools are documented **side by side** (e.g. Grok `search_replace` / `write` and AGY `replace_file_content` / `write_to_file`).
- **Do not** strip AGY paths or tool names when improving Grok compatibility.
- Policy: [`docs/VESSEL_DUAL_COMPAT.md`](docs/VESSEL_DUAL_COMPAT.md).

### Tests

```bash
python3 -m unittest tests.test_skill_compat -v
```

Guards: valid frontmatter, portable paths (no machine-local homes), dual tools where required, registry/manifest parity, install smoke for **grok** and **agy**.

---

## Companion skills (other repos)

First-class A.I.M. skills whose code lives with the tool. `install.sh` here does **not** copy them — clone the companion, then install as that repo documents.

### [aim-browser](https://github.com/BrianV1981/aim-browser) — headed CDP + skill suite

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
npm run install-skills -- "${PROJECT_ROOT:-.}/.grok/skills" --mode symlink
```

### [aim-google](https://github.com/BrianV1981/aim-google) — Workspace CLI

| Skill | Job |
|-------|-----|
| **aim-google** | Gmail, Drive, Calendar, Docs, Sheets, Tasks, Chat (API — not browser) |

Clone the repo and link that repo’s skill path into your vessel skills dir (see its README).

### [aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder) — dual vessel

| Skill | Job |
|-------|-----|
| **aim-flight-recorder** | Forensic Markdown from **AGY** brain JSONL **and** **Grok** `updates.jsonl` |

```bash
git clone https://github.com/BrianV1981/aim-flight-recorder.git
cd aim-flight-recorder
# Grok
mkdir -p "${HOME}/.grok/skills" && ln -sfn "$(pwd)" "${HOME}/.grok/skills/aim-flight-recorder"
# AGY
mkdir -p "${HOME}/.gemini/antigravity-cli/skills" && ln -sfn "$(pwd)" "${HOME}/.gemini/antigravity-cli/skills/aim-flight-recorder"
```

### [aim-coagents](https://github.com/BrianV1981/aim-coagents)

| Skill / pack | Job |
|--------------|-----|
| **aim-coagents** | DNA bank / blueprints for sovereign co-agents (equip when spawning peers) |

More install notes: [`docs/COMPANIONS.md`](docs/COMPANIONS.md).

---

## Base + Override Architecture

To prevent massive duplication, this library uses a **Base + Override** architecture:

1. **Global Base (`skills/`)**: All tool skills default to this directory. If a skill's instructions apply universally across all harnesses (e.g., `aim-memory-wiki`), it lives here.
2. **Vessel Overrides (`vessels/<cli>/skills/`)**: If a specific vessel requires uniquely tailored mechanics (e.g., `aim-handoff` needing different CLI commands for SQLite vs JSONL), a vessel-specific copy is placed here.

When executing `scripts/install.sh`, the installer seamlessly checks for a vessel-specific override first. If none exists, it securely falls back to symlinking the universal global skill.

---

## Layout

```text
skills/                      # library skill bodies (source of truth, global base)
vessels/<cli>/manifest.txt   # pack per host CLI
vessels/<cli>/skills/        # vessel-specific skill overrides (takes precedence)
scripts/install.sh           # symlink or copy library skills into a vessel (checks overrides first)
registry/skills.yaml         # catalog + companion pointers
docs/COMPANIONS.md           # companion install notes
docs/VESSEL_DUAL_COMPAT.md   # Grok + AGY dual-compat rules
tests/test_skill_compat.py   # portability + install smoke
```

---

## Vessels

| Vessel | Host CLI | Typical skills path |
|--------|----------|---------------------|
| **agy** | Antigravity / aim-agy | `<project>/.gemini/skills/` or `~/.gemini/antigravity-cli/skills/` |
| **grok** | Grok CLI | `<project>/.grok/skills/` or `~/.grok/skills/` |
| **opencode** | OpenCode | `<project>/.opencode/skills/` |
| **codex** | Codex CLI | Greenfield vessel + overlays (subset pack) |

---

## Design rules

1. **No absolute home-directory paths** and **no machine usernames** in skills, install scripts, or docs. Use `$HOME`, `~`, `$PROJECT_ROOT`, or relative paths.  
2. **Public library only** — proprietary vertical playbooks stay out of this repo.  
3. **Skill body in-repo** or don’t list it as `type: library`.  
4. **Companions** install from their own repos after clone.  
5. **Dual vessel** — Grok improvements must preserve AGY tool names/paths (or use an overlay). See [`docs/VESSEL_DUAL_COMPAT.md`](docs/VESSEL_DUAL_COMPAT.md).  
6. **Directory name = frontmatter `name`** (no `*.skill` suffixes).  

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
- **[aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)** — Forensic Markdown session extractor (AGY + Grok).
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
