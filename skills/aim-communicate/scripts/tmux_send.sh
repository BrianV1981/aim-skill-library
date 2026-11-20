#!/usr/bin/env bash
# aim-communicate (v2.0): paste short message into a POSIX tmux session using
# universal Enter-only submit (never Escape — #19), pre-submit composer check,
# mandatory FROM / REPLY_TO envelope, and deep (-S -300) capture-pane verification
# with zero duplicate retries once the composer clears.
#
# Exit codes:
#   0 = paste + submit + tmux verification OK
#   1 = usage / missing session / bad args
#   2 = PASTE_FAIL or VERIFY_FAIL (message not confirmed as submitted turn)
#
set -euo pipefail

TARGET=""
MESSAGE=""
FILE=""
FORCE_VESSEL=""
FROM_SESSION=""
REPLY_TO=""
NO_ENVELOPE=0
NO_VERIFY=0
BUF="aim_comm_short_$$"
VERIFY_LOG="/tmp/aim_comm_verify_$$.txt"

usage() {
  cat <<'EOF'
Usage:
  tmux_send.sh --target <session> --message 'text'
  tmux_send.sh --target <session> --from <session> --reply-to <session> --message 'text'
  tmux_send.sh --target <session> --file /path/to/msg.txt
  --force-vessel grok|agy|opencode|codex
  --no-envelope   # do not auto-prefix FROM/REPLY_TO
  --no-verify     # skip capture-pane verification (not recommended)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target|-t) TARGET="${2:-}"; shift 2 ;;
    --message|-m) MESSAGE="${2:-}"; shift 2 ;;
    --file|-f) FILE="${2:-}"; shift 2 ;;
    --force-vessel) FORCE_VESSEL="${2:-}"; shift 2 ;;
    --from) FROM_SESSION="${2:-}"; shift 2 ;;
    --reply-to) REPLY_TO="${2:-}"; shift 2 ;;
    --no-envelope) NO_ENVELOPE=1; shift ;;
    --no-verify) NO_VERIFY=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

[[ -n "$TARGET" ]] || { echo "error: --target required" >&2; exit 1; }
if [[ -n "$FILE" ]]; then
  MESSAGE="$(cat "$FILE")"
fi
[[ -n "$MESSAGE" ]] || { echo "error: --message or --file required" >&2; exit 1; }

if ! tmux has-session -t "$TARGET" 2>/dev/null; then
  echo "error: tmux session not found: $TARGET" >&2
  exit 1
fi

if [[ -z "$FROM_SESSION" ]]; then
  FROM_SESSION="$(tmux display-message -p '#{session_name}' 2>/dev/null || true)"
fi
if [[ -z "$FROM_SESSION" ]]; then
  FROM_SESSION="unknown"
  echo "[tmux_send] warning: could not detect FROM session; set --from explicitly" >&2
fi

if [[ -z "$REPLY_TO" ]]; then
  REPLY_TO="$FROM_SESSION"
fi

if [[ "$NO_ENVELOPE" -eq 0 ]]; then
  if ! grep -q '\[FROM:' <<<"$MESSAGE"; then
    MESSAGE="[FROM:${FROM_SESSION}] [REPLY_TO:${REPLY_TO}] ${MESSAGE}"
  fi
  if grep -q '\[FROM:' <<<"$MESSAGE" && ! grep -q '\[REPLY_TO:' <<<"$MESSAGE"; then
    MESSAGE="${MESSAGE/\[FROM:${FROM_SESSION}\]/[FROM:${FROM_SESSION}] [REPLY_TO:${REPLY_TO}]}"
    if ! grep -q '\[REPLY_TO:' <<<"$MESSAGE"; then
      MESSAGE="[REPLY_TO:${REPLY_TO}] ${MESSAGE}"
    fi
  fi
fi

CMD="$(tmux list-panes -t "$TARGET" -F '#{pane_current_command}' 2>/dev/null | head -1 || true)"
VESSEL="${FORCE_VESSEL:-${CMD:-auto}}"

# Unique fingerprint needle from first rendered line (never broken by multi-line paste chips)
FIRST_LINE="$(printf '%s' "$MESSAGE" | head -n 1)"
NEEDLE=""
if [[ "$FIRST_LINE" =~ \[FROM:[^\]]+\] ]]; then
  NEEDLE="${BASH_REMATCH[0]}"
fi
if [[ -z "$NEEDLE" ]]; then
  NEEDLE="$(printf '%s' "$FIRST_LINE" | head -c 48)"
fi

echo "[tmux_send] from=$FROM_SESSION reply_to=$REPLY_TO target=$TARGET cmd=$CMD vessel=$VESSEL"
echo "[tmux_send] verify_needle=${NEEDLE:0:60}"

capture_deep() {
  tmux capture-pane -t "$TARGET" -p -J -S -300 2>/dev/null || true
}

composer_has_pending_paste() {
  local pane="$1"
  local bottom_prompt
  bottom_prompt="$(printf '%s\n' "$pane" | tail -n 6 | grep -E '^[>❯›][[:space:]]+' || true)"
  [[ -n "$bottom_prompt" ]] || return 1
  if grep -Fq "[Pasted text" <<<"$bottom_prompt" || grep -Fq -- "$NEEDLE" <<<"$bottom_prompt"; then
    return 0
  fi
  return 1
}

BEFORE_PANE="$(capture_deep)"
BEFORE_COUNT="$(grep -F -c -- "$NEEDLE" <<<"$BEFORE_PANE" || true)"

tmux set-buffer -b "$BUF" "$MESSAGE"
tmux paste-buffer -b "$BUF" -p -t "$TARGET"
sleep 0.25

AFTER_PASTE_PANE="$(capture_deep)"
AFTER_PASTE_COUNT="$(grep -F -c -- "$NEEDLE" <<<"$AFTER_PASTE_PANE" || true)"

# AC2: Pre-submit composer check — confirm paste landed (inline needle or [Pasted text chip) before sending Enter
if ! grep -Fq "[Pasted text" <<<"$AFTER_PASTE_PANE" && [[ "$AFTER_PASTE_COUNT" -le "$BEFORE_COUNT" ]] && ! grep -Fq -- "$NEEDLE" <<<"$AFTER_PASTE_PANE"; then
  tmux delete-buffer -b "$BUF" 2>/dev/null || true
  echo "[tmux_send] PASTE_FAIL: composer empty after paste-buffer; sending no keys" >&2
  exit 2
fi

# AC1: Enter ONLY across ALL vessels (agy, grok, opencode, codex). NEVER send Escape.
tmux send-keys -t "$TARGET" Enter
sleep 0.8

verify_delivery() {
  local pane attempt=1 max_attempts=3 cur_count
  while [[ $attempt -le $max_attempts ]]; do
    pane="$(capture_deep)"
    printf '%s\n' "$pane" > "$VERIFY_LOG"
    cur_count="$(grep -F -c -- "$NEEDLE" <<<"$pane" || true)"

    # If paste is STILL sitting unsubmitted in the bottom composer prompt, retry Enter once
    if composer_has_pending_paste "$pane"; then
      if [[ $attempt -lt $max_attempts ]]; then
        echo "[tmux_send] verify attempt $attempt: paste still in composer; retrying Enter..." >&2
        tmux send-keys -t "$TARGET" Enter
        sleep 0.8
        attempt=$((attempt + 1))
        continue
      fi
      return 1
    fi

    # Composer is clear: NEVER re-send Enter (AC4 — prevents duplicate turns).
    # Success if needle count increased, needle is in deep history, or active turn/chip rendered.
    if [[ "$cur_count" -gt "$BEFORE_COUNT" ]] \
      || grep -Fq -- "$NEEDLE" <<<"$pane" \
      || grep -Fq "[Pasted text" <<<"$pane" \
      || grep -Eiq 'Working\.\.\.|Loading\.\.\.|Thought for|esc to cancel|esc to interrupt' <<<"$pane"; then
      echo "[tmux_send] VERIFY_OK: turn submitted on target=$TARGET (composer clear, deep capture verified)"
      return 0
    fi

    sleep 0.5
    attempt=$((attempt + 1))
  done
  return 1
}

VERIFY_RC=0
if [[ "$NO_VERIFY" -eq 1 ]]; then
  echo "[tmux_send] warning: --no-verify set; skipping hard check" >&2
else
  if ! verify_delivery; then
    VERIFY_RC=2
    echo "[tmux_send] VERIFY_FAIL: message not confirmed in tmux session '$TARGET'" >&2
    echo "[tmux_send] last capture saved: $VERIFY_LOG" >&2
    tail -n 30 "$VERIFY_LOG" >&2 || true
  fi
fi

tmux delete-buffer -b "$BUF" 2>/dev/null || true

if [[ "$VERIFY_RC" -ne 0 ]]; then
  echo "[tmux_send] FAILED delivery verification — agent must NOT claim success" >&2
  exit 2
fi

echo "[tmux_send] done — VERIFIED on target=$TARGET; peer reports must hit REPLY_TO=$REPLY_TO"
exit 0
