#!/usr/bin/env bash
# Install library skills into a vessel skills directory.
# Bodies come ONLY from this repo (skills/). No machine-local absolute paths.
#
# Usage:
#   ./scripts/install.sh --vessel grok     --dest "$HOME/.grok/skills"
#   ./scripts/install.sh --vessel agy      --dest "$HOME/.gemini/antigravity-cli/skills" --mode symlink
#   ./scripts/install.sh --vessel opencode --dest "$HOME/.config/opencode/skills" --mode symlink
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VESSEL=""
DEST=""
MODE="symlink" # symlink | copy
COMMANDS_DEST=""
NO_COMMANDS=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vessel) VESSEL="$2"; shift 2 ;;
    --dest) DEST="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --commands-dest) COMMANDS_DEST="$2"; shift 2 ;;
    --no-commands) NO_COMMANDS=1; shift ;;
    -h|--help)
      sed -n '2,9p' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$VESSEL" || -z "$DEST" ]]; then
  echo "Usage: $0 --vessel agy|grok|opencode|codex --dest <skills-dir> [--mode symlink|copy] [--commands-dest <dir>] [--no-commands]" >&2
  exit 1
fi

MANIFEST="$ROOT/vessels/$VESSEL/manifest.txt"
if [[ ! -f "$MANIFEST" ]]; then
  echo "No manifest for vessel: $VESSEL" >&2
  exit 1
fi

mkdir -p "$DEST"
echo "Vessel=$VESSEL dest=$DEST mode=$MODE root=$ROOT"

while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%$'\r'}"
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  id="$line"

  # Check for vessel-specific override first
  src_override="$ROOT/vessels/$VESSEL/skills/$id"
  src_global="$ROOT/skills/$id"

  if [[ -d "$src_override" ]]; then
    src="$src_override"
    echo "Using vessel override for $id"
  elif [[ -d "$src_global" ]]; then
    src="$src_global"
  else
    echo "SKIP $id (missing skills/$id — not in this library)"
    continue
  fi
  target="$DEST/$id"

  # Auto-remove legacy .skill directories to prevent shadowing
  if [[ -d "${target}.skill" || -L "${target}.skill" ]]; then
    rm -rf "${target}.skill"
    echo "clean  ${target}.skill (removed legacy directory)"
  fi

  src_real=$(readlink -f "$src" 2>/dev/null || realpath "$src")
  tgt_real=$(readlink -f "$target" 2>/dev/null || true)
  if [[ -n "${tgt_real:-}" && "$src_real" == "$tgt_real" ]]; then
    echo "keep   $target"
    continue
  fi
  rm -rf "$target"
  if [[ "$MODE" == "symlink" ]]; then
    ln -sfn "$src_real" "$target"
    echo "symlink $target -> $src_real"
  else
    cp -a "$src" "$target"
    echo "copied  $target"
  fi
done < "$MANIFEST"

# For OpenCode, also generate `/` slash-command wrappers in sibling `commands/` (unless --no-commands)
if [[ "$VESSEL" == "opencode" && "$NO_COMMANDS" -eq 0 ]]; then
  PY_BIN="$(command -v python3 || command -v python || true)"
  if [[ -n "$PY_BIN" ]]; then
    CMD_ARGS=(--vessel opencode --dest "$DEST" --sync-commands-only)
    [[ -n "$COMMANDS_DEST" ]] && CMD_ARGS+=(--commands-dest "$COMMANDS_DEST")
    "$PY_BIN" "$ROOT/scripts/install.py" "${CMD_ARGS[@]}"
  else
    EFF_CMDS="$COMMANDS_DEST"
    if [[ -z "$EFF_CMDS" && "$(basename "$DEST")" == "skills" ]]; then
      EFF_CMDS="$(dirname "$DEST")/commands"
    fi
    if [[ -n "$EFF_CMDS" ]]; then
      mkdir -p "$EFF_CMDS"
      for sdir in "$DEST"/*; do
        [[ -d "$sdir" && -f "$sdir/SKILL.md" ]] || continue
        sid="$(basename "$sdir")"
        cat > "$EFF_CMDS/$sid.md" <<EOF
---
description: "Load and execute the $sid skill"
---
Use the \`$sid\` skill via the \`skill\` tool and follow its instructions. \$ARGUMENTS
EOF
      done
      cat > "$EFF_CMDS/aim.md" <<'EOF'
---
description: "Load and run an installed A.I.M. skill by ID (e.g. /aim aim-handoff)"
---
The user invoked `/aim` with: $ARGUMENTS
Treat the first token as the skill ID, load that skill via the `skill` tool, and follow its instructions for the remaining request.
EOF
      echo "commands $EFF_CMDS (generated OpenCode slash wrappers)"
    fi
  fi
fi

echo "Done. Companion tools (browser suite, google Workspace, …) install from their own repos — see docs/COMPANIONS.md"
echo "Ensure the host CLI scans: $DEST"
