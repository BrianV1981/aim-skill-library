---
name: aim-grok-context
description: >
  Project context for the aim-grok vessel (A.I.M. on Grok CLI). Use when working
  in an aim-grok checkout, running ./aim commands, or adapting engine code from
  aim-agy. Slash: /aim-grok-context.
---

# aim-grok project context

## Facts
- CWD should be the **aim-grok project root** (the clone that contains `./aim` and `aim-agy_os/`). Detect with: `git rev-parse --show-toplevel` or the directory where `./aim` exists.
- Engine lives in `aim-agy_os/` (name kept for path compat with aim-agy).
- CLI: `./aim <cmd>` or venv python → `.aim_core/aim_cli.py`.
- Upstream source of truth for engine: **aim-agy** main; this repo is the Grok adaptation.
- Optional env override: `AIM_GROK_ROOT` if set — prefer it over guessing.

## First actions on factual questions
```bash
# from aim-grok project root
./aim map
./aim search "<query>"
./aim doctor
```

## Do not
- Confuse this checkout with a separate **aim-agy** clone without Operator scope.
- Commit live `memory_lance/` or `venv/`.
- Hardcode machine-local absolute home paths in notes or handoffs.
