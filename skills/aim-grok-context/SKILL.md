---
name: aim-grok-context
description: >
  Project context for the aim-grok vessel (A.I.M. on Grok CLI). Use when working
  in /home/kingb/aim-grok, running ./aim commands, or adapting engine code from
  aim-agy. Slash: /aim-grok-context.
---

# aim-grok project context

## Facts
- CWD should be `/home/kingb/aim-grok`.
- Engine lives in `aim-agy_os/` (name kept for path compat with aim-agy).
- CLI: `./aim <cmd>` or venv python → `.aim_core/aim_cli.py`.
- Upstream source of truth for engine: `aim-agy` main; this repo is the Grok adaptation.

## First actions on factual questions
```bash
./aim map
./aim search "<query>"
./aim doctor
```

## Do not
- Confuse this repo with `/home/kingb/aim-agy` without Operator scope.
- Commit live `memory_lance/` or `venv/`.
