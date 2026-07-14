---
name: aim-export-cartridge
description: >
  Export A.I.M. knowledge into a portable DataJack cartridge (.engram / parquet
  exchange). Use when packaging knowledge for backup or P2P share. Slash:
  /aim-export-cartridge. Modernized for aim-agy plugins/datajack.
---

# aim-export-cartridge

## CLI path

```bash
AIM_OS="${AIM_OS:-./aim-agy_os}"
PY="$AIM_OS/venv/bin/python3"
EXCHANGE="$AIM_OS/.aim_core/plugins/datajack/aim_exchange.py"
```

## Export

```bash
# keyword filter + output name
$PY $EXCHANGE export "<keyword>" --out "<name>.engram"
```

Or via main router if registered:

```bash
$PY $AIM_OS/.aim_core/aim_cli.py export ...   # only if subcommand exists; else use exchange directly
```

## Rules

1. Confirm keyword scope with the Operator before large exports.
2. Write outputs under a project `archive/cartridges/` or `/tmp/` — do not dump into repo root.
3. Report resulting path and stderr if export fails.
4. Companion bake for docs cartridges: `aim bake` / `aim_bake.py` when rebuilding ROM from `aim-agy_os_docs/`.
