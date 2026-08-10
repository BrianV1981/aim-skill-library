# Vessel dual compatibility (Grok + AGY)

**Rule:** When editing skills for Grok CLI, **do not strip AGY paths or tool names**. Prefer dual documentation so one library body serves both hosts.

See also: [issue #5](https://github.com/BrianV1981/aim-skill-library/issues/5), Grok skills guide (host CLI), `vessels/*/manifest.txt`.

## Strategies

| Strategy | When | How |
|----------|------|-----|
| **A. Dual body** | Same procedure; only tool/path names differ | One `SKILL.md` with explicit **Grok** and **AGY** sections or a vessel tool table |
| **B. Vessel overlay** | Divergence is large | Shared core + vessel-specific files / install-time select (use sparingly) |
| **C. Neutral wording** | No host-specific tools | “Use file write/edit tools” without host tool IDs |
| **D. Grok-only pack** | Skill only applies on Grok | List only under `vessels/grok` (e.g. `aim-grok-context`); leave AGY free of it |

**Hard rule:** If a change would break AGY install or AGY tool names with no dual path, use **B** (or dual table) instead of overwriting the AGY-facing body.

## Install roots

| Vessel | Typical skills path |
|--------|---------------------|
| Grok | `<project>/.grok/skills/` or `~/.grok/skills/` |
| AGY | `<project>/.gemini/skills/` |
| OpenCode | `<project>/.opencode/skills/` |

Install:

```bash
./scripts/install.sh --vessel grok --dest /path/to/project/.grok/skills --mode symlink
./scripts/install.sh --vessel agy  --dest /path/to/aim-agy/.gemini/skills --mode symlink
```

## Tool name tables (common)

### File edit

| Vessel | Create / overwrite | Edit in place | Read |
|--------|--------------------|---------------|------|
| Grok | `write` | `search_replace` | `read_file` |
| AGY | `write_to_file` | `replace_file_content`, `multi_replace_file_content` | host read tools |

### Images

| Vessel | Generate |
|--------|----------|
| Grok | `image_gen` (edit: `image_edit`) |
| AGY / other | host image tool (often `generate_image`) |

### Shell

Both: run shell via the host’s terminal tool (`run_terminal_command` on Grok). Prefer documenting the **shell command** itself so either host can run it.

## Path hygiene

- **Forbidden** in skill bodies: machine-local absolute homes (`/home/<user>/...`, `/Users/<user>/...`).
- **Allowed:** `$PROJECT_ROOT`, `$HOME`, `~`, env vars (`AIM_GROK_ROOT`, `AIM_SANDBOX_ROOT`), relative repo paths.

## Registry / manifests

- Every on-disk `skills/<id>/` library skill must appear in `registry/skills.yaml` with `type: library` and a non-empty `vessels` list.
- Every id in `vessels/<cli>/manifest.txt` must exist as `skills/<id>/` and list that vessel in the registry.
- Directory name **must** equal frontmatter `name` (no `*.skill` suffixes).

## Tests

```bash
python3 -m unittest tests.test_skill_compat -v
```

These tests guard Grok readiness **and** AGY regression (dual tools, dual install smoke).
