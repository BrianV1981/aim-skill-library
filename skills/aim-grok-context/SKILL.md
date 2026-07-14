---
name: aim-grok-context
description: >
  Context for the aim-grok vessel (A.I.M. engine on Grok CLI): layout, CLI, and
  first actions. Use when working in aim-grok or adapting engine code. Slash:
  /aim-grok-context.
---

# aim-grok-context

## Layout

- Work from the **vessel project root**.  
- Engine tree: typically `aim-agy_os/` (shared naming with aim-agy for path compat).  
- CLI: `./aim <cmd>` or the project venv → `.aim_core/aim_cli.py`.  
- Engine upstream: **aim-agy**; this vessel is the Grok-host adaptation.

## First actions (facts / status)

```bash
./aim map
./aim search "<query>"
./aim doctor
```

## Do not

- Edit or commit `memory_lance/`, `venv/`, or other generated stores unless the Operator asks.  
- Confuse this vessel with aim-agy (or others) without clear Operator scope.  
- Invent Engram facts when search is empty.
