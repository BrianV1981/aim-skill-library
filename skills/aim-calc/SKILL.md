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

From a context where the skill is installed (adjust path if needed):

```bash
python skills/aim-calc/scripts/aim_calc.py "<expression>"
# after vessel install, often:
python <skills-dir>/aim-calc/scripts/aim_calc.py "<expression>"
```

Output is JSON (success/error, values, messages).

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
