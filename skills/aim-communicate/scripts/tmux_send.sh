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
umask 077

TARGET=""
MESSAGE=""
FILE=""
FORCE_VESSEL=""
FROM_SESSION=""
REPLY_TO=""
NO_ENVELOPE=0
NO_VERIFY=0
ALLOW_DND="${AIM_ALLOW_DND:-${AIM_ALLOW_AIM_LD:-0}}"
BUF="aim_comm_$$"
VERIFY_LOG="$(mktemp "${TMPDIR:-/tmp}/aim_comm_verify.XXXXXX")"

cleanup() {
  tmux delete-buffer -b "$BUF" 2>/dev/null || true
  rm -f "$VERIFY_LOG"
}
trap cleanup EXIT INT TERM

usage() {
  cat <<'EOF'
Usage:
  tmux_send.sh --target <session> --message 'text'
  tmux_send.sh --target <session> --from <session> --reply-to <session> --message 'text'
  tmux_send.sh --target <session> --file /path/to/msg.txt
  --force-vessel grok|agy|opencode|codex
  --allow-dnd     # bypass AIM_DND_SESSIONS / AIM_TMUX_DND_TARGETS guard
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
    --allow-dnd) ALLOW_DND=1; shift ;;
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

CLEAN_TARGET="${TARGET#=}"
SESSION_NAME="${CLEAN_TARGET%%:*}"
SESSION_TARGET="=${SESSION_NAME}"
if [[ "$CLEAN_TARGET" == *:* ]]; then
  PANE_TARGET="=${CLEAN_TARGET}"
else
  PANE_TARGET="=${CLEAN_TARGET}:"
fi

# DND session guard
DND_LIST="${AIM_DND_SESSIONS:-${AIM_TMUX_DND_TARGETS:-aim-ld}}"
if [[ "$ALLOW_DND" != "1" && -n "$DND_LIST" ]]; then
  for dnd_item in ${DND_LIST//,/ }; do
    [[ -n "$dnd_item" ]] || continue
    if [[ "$SESSION_NAME" == "${dnd_item#=}" ]]; then
      echo "[tmux_send] DND_BLOCKED: target session '$SESSION_NAME' is in DND list ($DND_LIST); pass --allow-dnd or AIM_ALLOW_DND=1 to override" >&2
      exit 2
    fi
  done
fi

if ! tmux has-session -t "$SESSION_TARGET" 2>/dev/null; then
  echo "error: tmux session not found: $SESSION_NAME" >&2
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

CMD="$(tmux list-panes -t "$PANE_TARGET" -F '#{pane_current_command}' 2>/dev/null | head -1 || true)"
VESSEL="${FORCE_VESSEL:-${CMD:-auto}}"

# Full first-line fingerprint needle (includes FROM/REPLY_TO + message snippet so stale [FROM:x] lines never collide)
FIRST_LINE="$(printf '%s' "$MESSAGE" | head -n 1)"
NEEDLE="$(printf '%s' "$FIRST_LINE" | head -c 72)"
HEADER_NEEDLE=""
if [[ "$FIRST_LINE" =~ \[FROM:[^\]]+\] ]]; then
  HEADER_NEEDLE="${BASH_REMATCH[0]}"
fi

echo "[tmux_send] from=$FROM_SESSION reply_to=$REPLY_TO target=$SESSION_NAME pane=$PANE_TARGET cmd=$CMD vessel=$VESSEL"
echo "[tmux_send] verify_needle=${NEEDLE:0:60}"

capture_deep() {
  tmux capture-pane -t "$PANE_TARGET" -p -J -S -300 2>/dev/null || true
}

count_fixed() {
  local needle="$1"
  local haystack="$2"
  if [[ -z "$needle" ]]; then
    echo 0
    return
  fi
  local c
  c="$(grep -F -c -- "$needle" <<<"$haystack" || true)"
  echo "${c:-0}"
}

composer_has_pending_paste() {
  local pane="$1"
  local bottom_lines
  bottom_lines="$(printf '%s\n' "$pane" | awk 'NF{buf[NR]=$0} END{start=NR-5; if(start<1) start=1; for(i=start;i<=NR;i++) if(buf[i]!="") print buf[i]}')"
  [[ -n "$bottom_lines" ]] || return 1
  local prompt_lines
  prompt_lines="$(printf '%s\n' "$bottom_lines" | grep -E '^[>❯›$#%➜][[:space:]]+' || true)"
  [[ -n "$prompt_lines" ]] || return 1
  if grep -Fq "[Pasted text" <<<"$prompt_lines" \
    || grep -Fq -- "$NEEDLE" <<<"$prompt_lines" \
    || { [[ -n "$HEADER_NEEDLE" ]] && grep -Fq -- "$HEADER_NEEDLE" <<<"$prompt_lines"; }; then
    return 0
  fi
  return 1
}

last_line_is_unsubmitted_prompt() {
  local pane="$1"
  local last_line
  last_line="$(printf '%s\n' "$pane" | awk 'NF{line=$0} END{print line}')"
  [[ -n "$last_line" ]] || return 1
  if printf '%s\n' "$last_line" | grep -Eq '^[>❯›$#%➜][[:space:]]+' \
    && { grep -Fq "[Pasted text" <<<"$last_line" \
      || grep -Fq -- "$NEEDLE" <<<"$last_line" \
      || { [[ -n "$HEADER_NEEDLE" ]] && grep -Fq -- "$HEADER_NEEDLE" <<<"$last_line"; }; }; then
    return 0
  fi
  return 1
}

BEFORE_PANE="$(capture_deep)"
BEFORE_NEEDLE_COUNT="$(count_fixed "$NEEDLE" "$BEFORE_PANE")"
BEFORE_CHIP_COUNT="$(count_fixed "[Pasted text" "$BEFORE_PANE")"

tmux set-buffer -b "$BUF" -- "$MESSAGE"
tmux paste-buffer -b "$BUF" -d -p -t "$PANE_TARGET"
sleep 0.25

AFTER_PASTE_PANE="$(capture_deep)"
AFTER_NEEDLE_COUNT="$(count_fixed "$NEEDLE" "$AFTER_PASTE_PANE")"
AFTER_CHIP_COUNT="$(count_fixed "[Pasted text" "$AFTER_PASTE_PANE")"

# AC2: Pre-submit composer check — require strict count increase (needle or [Pasted text chip) before sending Enter
if [[ "$AFTER_NEEDLE_COUNT" -le "$BEFORE_NEEDLE_COUNT" && "$AFTER_CHIP_COUNT" -le "$BEFORE_CHIP_COUNT" ]]; then
  echo "[tmux_send] PASTE_FAIL: composer unchanged after paste-buffer (needle $BEFORE_NEEDLE_COUNT->$AFTER_NEEDLE_COUNT, chip $BEFORE_CHIP_COUNT->$AFTER_CHIP_COUNT); sending no keys" >&2
  exit 2
fi

# AC1: Enter ONLY across ALL vessels (agy, grok, opencode, codex). NEVER send Escape.
tmux send-keys -t "$PANE_TARGET" Enter
sleep 0.8

verify_delivery() {
  local pane attempt=1 max_attempts=3 cur_needle_count cur_chip_count
  while [[ $attempt -le $max_attempts ]]; do
    pane="$(capture_deep)"
    printf '%s\n' "$pane" > "$VERIFY_LOG"
    cur_needle_count="$(count_fixed "$NEEDLE" "$pane")"
    cur_chip_count="$(count_fixed "[Pasted text" "$pane")"

    # If paste is STILL sitting unsubmitted in the bottom composer prompt, retry Enter once
    if composer_has_pending_paste "$pane" || last_line_is_unsubmitted_prompt "$pane"; then
      if [[ $attempt -lt $max_attempts ]]; then
        echo "[tmux_send] verify attempt $attempt: paste still in composer; retrying Enter..." >&2
        tmux send-keys -t "$PANE_TARGET" Enter
        sleep 0.8
        attempt=$((attempt + 1))
        continue
      fi
      return 1
    fi

    # Composer is clear: NEVER re-send Enter (AC4 — prevents duplicate turns).
    # Require strict occurrence increase vs pre-paste baseline (never match stale scrollback).
    if [[ "$cur_needle_count" -gt "$BEFORE_NEEDLE_COUNT" || "$cur_chip_count" -gt "$BEFORE_CHIP_COUNT" ]]; then
      echo "[tmux_send] VERIFY_OK: turn submitted on target=$SESSION_NAME (needle $BEFORE_NEEDLE_COUNT->$cur_needle_count, chip $BEFORE_CHIP_COUNT->$cur_chip_count)"
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
    echo "[tmux_send] VERIFY_FAIL: message not confirmed in tmux session '$SESSION_NAME'" >&2
    tail -n 30 "$VERIFY_LOG" >&2 || true
  fi
fi

if [[ "$VERIFY_RC" -ne 0 ]]; then
  echo "[tmux_send] FAILED delivery verification — agent must NOT claim success" >&2
  exit 2
fi

echo "[tmux_send] done — VERIFIED on target=$SESSION_NAME; peer reports must hit REPLY_TO=$REPLY_TO"
exit 0
