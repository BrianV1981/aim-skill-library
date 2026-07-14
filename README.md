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
| **`skills/<id>/`** — real `SKILL.md` (+ scripts) | Pointer-only index with `/home/you` paths |
| Portable `scripts/install.sh` | Machine-local absolute install maps |
| Per-CLI manifests (`vessels/agy|grok|opencode|…`) | One-size dump of every private vertical |
| Companion list for heavy tools | Vendoring Chromium engines / Workspace CLIs |

**Library skills** live here. **Companion tools** (browser suite, Google Workspace, …) stay in their own public repos — see [`docs/COMPANIONS.md`](docs/COMPANIONS.md).

---

## Quick install

```bash
git clone https://github.com/BrianV1981/aim-skill-library.git
cd aim-skill-library

# Grok vessel
./scripts/install.sh --vessel grok --dest /path/to/project/.grok/skills --mode symlink

# aim-agy (Gemini / Antigravity skills dir)
./scripts/install.sh --vessel agy --dest /path/to/aim-agy/.gemini/skills --mode symlink

# OpenCode
./scripts/install.sh --vessel opencode --dest /path/to/project/.opencode/skills --mode symlink
```

Then equip **companions** you need (example — public browser suite):

```bash
git clone https://github.com/BrianV1981/aim-browser.git
cd aim-browser && npm install
npm run install-skills -- /path/to/project/.grok/skills --mode symlink
```

---

## Skills in this library

| Skill | Role |
|-------|------|
| **aim-communicate** | Inter-agent tmux protocol (`FROM` / `REPLY_TO`) |
| **aim-calc** | Stateful scientific calculator |
| **aim-memory-search** | Engram / hybrid search via `./aim` |
| **aim-list-sessions** | Map / list indexed work |
| **aim-export-cartridge** | Export memory cartridge |
| **aim-wiki** | Memory wiki (Grok-oriented) |
| **aim-grok-context** | aim-grok vessel context |
| **aim-technical-auditor** | Architecture review persona |
| **aim-python-specialist** | TDD Python implementer persona |

Manifests under `vessels/` choose the pack per CLI. Edit manifests freely for your desk.

Full index: [`registry/skills.yaml`](registry/skills.yaml).

---

## Layout

```text
skills/                 # skill bodies (source of truth)
vessels/<cli>/manifest.txt
scripts/install.sh      # symlink or copy into a vessel
registry/skills.yaml    # catalog + companion pointers
docs/COMPANIONS.md      # heavy tools not vendored here
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
2. **No private verticals** (lead ops, site-specific harvest playbooks) in this public library.  
3. **Skill body in-repo** or don’t list it as `type: library`.  
4. **Companions** install from their own repos after clone.  

---

## Support

**[Buy Me a Coffee →](https://www.buymeacoffee.com/BrianV1981)**

MIT — fork it, keep it, walk away with the files.

---

### Related

- **[aim-browser](https://github.com/BrianV1981/aim-browser)** — headed CDP + browser skill suite (public)  
- **[aim-agy](https://github.com/BrianV1981/aim-agy)** — flagship A.I.M. engine vessel  
- Older private **aim-skills** registry (if present on your account) is superseded by this library for sharing
