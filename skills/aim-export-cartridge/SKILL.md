---
name: aim-export-cartridge
description: >
  Export A.I.M. knowledge into a portable cartridge (.engram / exchange format)
  for backup or share. Slash: /aim-export-cartridge.
---

# aim-export-cartridge

## Paths (relative to vessel)

```bash
AIM_OS="${AIM_OS:-./aim-agy_os}"
PY="${AIM_OS}/venv/bin/python3"
EXCHANGE="${AIM_OS}/.aim_core/plugins/datajack/aim_exchange.py"
```

Adjust `AIM_OS` if this vessel uses a different engine root.

## Export

```bash
"$PY" "$EXCHANGE" export "<keyword>" --out "<name>.engram"
```

If the vessel exposes a CLI subcommand, prefer that when documented:

```bash
./aim …   # only when export is registered on this vessel
```

## Rules

1. Confirm keyword/scope with the Operator before large exports.  
2. Write outputs under `archive/cartridges/` or `/tmp/` — not repo root.  
3. Report output path and any errors.  
4. Do not include secrets or live credentials in cartridges.
