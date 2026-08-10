---
name: aim-calc
description: >
  Stateful scientific calculator for agents. Use for expressions, variables, and
  unit-aware math instead of mental arithmetic. Slash: /aim-calc.
---

# aim-calc

**Do not** compute non-trivial math from model weights. Use this skill.

Evaluates deterministic Python expressions; keeps variables across calls; supports units via `pint` (`u`).

## Run

From a context where the skill is installed (pick the path for your vessel):

```bash
# library checkout (before install)
python skills/aim-calc/scripts/aim_calc.py "<expression>"

# after vessel install — Grok
python "$PROJECT_ROOT/.grok/skills/aim-calc/scripts/aim_calc.py" "<expression>"
# or user-global: ~/.grok/skills/aim-calc/scripts/aim_calc.py

# after vessel install — AGY / Antigravity
python "$PROJECT_ROOT/.gemini/skills/aim-calc/scripts/aim_calc.py" "<expression>"
```

Optional dependency: `pint` for unit-aware math (`u`). Output is JSON (success/error, values, messages).

## Examples

```bash
# Basic
python …/aim_calc.py "sqrt(398600 / 6678.0)"

# Assign (persists in .calc_state.json)
python …/aim_calc.py "v_leo = sqrt(398600 / 6678.0)"

# Reuse variables
python …/aim_calc.py "burn1 = v_tp - v_leo"

# Units
python …/aim_calc.py "speed = 12 * u.meter / u.second"
python …/aim_calc.py "distance = speed * (2 * u.minute)"
python …/aim_calc.py "distance.to(u.km)"
```

State files (`.calc_state.json`, `.calc_audit.log`) are local to the working directory — do not commit them unless the Operator wants them tracked.
