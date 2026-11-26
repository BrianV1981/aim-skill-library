---
name: aim-communicate
description: >
  [DEPRECATED — Redirects to `aim-mail`] Legacy inter-agent communication alias.
  Use the canonical `aim-mail` skill (`skills/aim-mail/SKILL.md`, CLI `amail` / `aim-mail`
  powered by `aim-mailbox`) for all cross-OS and cross-harness messaging.
---

# `aim-communicate` — DEPRECATED (Use `aim-mail` / `amail`)

> **DEPRECATION NOTICE (`aim-joshua#181` / `aim-skill-library#35`):** `aim-communicate` and standalone `tmux` paste helpers have been superseded by **A-Mail** (`amail` / `aim-mail`, powered by `aim-mailbox`). Retained for one transition cycle solely as a redirect stub.

## Required Action

Immediately load and follow the canonical **`aim-mail`** skill instead:

- **Skill Locations:** `${PROJECT_ROOT:-.}/.gemini/skills/aim-mail/SKILL.md`, `$HOME/.gemini/antigravity-cli/skills/aim-mail/SKILL.md`, `${PROJECT_ROOT:-.}/.grok/skills/aim-mail/SKILL.md`, `$HOME/.grok/skills/aim-mail/SKILL.md`, `$HOME/.codex/skills/aim-mail/SKILL.md`, or `$HOME/.config/opencode/skills/aim-mail/SKILL.md`
- **CLI Entrypoints:** `amail` or `aim-mail` (`register`, `agents`, `send`, `inbox`, `read`, `reply`, `ack`, `check`, `wait`, `pulse`, `watch`, `gc`, `install-agy-sidecar`, `install-hooks`, `describe`)
- **Mandates:** Always set `--from` and `--reply-to`, pass `--operator-approved` on initial dispatches, obey `max_hops=1` bounded replies (`DO NOT reply` on closeout), respect DND/WIP locks, and route POSIX `tmux` panes exclusively via `amail`'s built-in `--driver tmux` (never raw `tmux send-keys` or legacy shell paste wrappers).
