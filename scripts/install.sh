#!/usr/bin/env bash
# Install library skills into a vessel skills directory.
# Bodies come ONLY from this repo (skills/). No machine-local absolute paths.
#
# Usage:
#   ./scripts/install.sh --vessel grok --dest /path/to/project/.grok/skills
#   ./scripts/install.sh --vessel agy  --dest /path/to/aim-agy/.gemini/skills --mode symlink
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VESSEL=""
DEST=""
MODE="symlink" # symlink | copy

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vessel) VESSEL="$2"; shift 2 ;;
    --dest) DEST="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,8p' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$VESSEL" || -z "$DEST" ]]; then
  echo "Usage: $0 --vessel agy|grok|opencode|codex --dest <skills-dir> [--mode symlink|copy]" >&2
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
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  id="$line"
  src="$ROOT/skills/$id"
  if [[ ! -d "$src" ]]; then
    echo "SKIP $id (missing skills/$id — not in this library)"
    continue
  fi
  target="$DEST/$id"
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

echo "Done. Companion tools (browser suite, google Workspace, …) install from their own repos — see docs/COMPANIONS.md"
echo "Ensure the host CLI scans: $DEST"
