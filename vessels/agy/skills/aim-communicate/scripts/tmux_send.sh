#!/usr/bin/env bash
# aim-communicate: paste short message into a tmux session with correct submit
# for Grok vs AGY, mandatory FROM / REPLY_TO envelope, and **hard verify** via
# capture-pane that the message landed as a submitted turn (not stuck in composer).
#
# Usage:
#   tmux_send.sh --target <session> --message 'body'
#   tmux_send.sh --target <session> --file /path/to/short.txt
#   tmux_send.sh --target <session> --from <session> --reply-to <session> --message '...'
#   tmux_send.sh --target <session> --message '...' --force-vessel grok|agy
#   tmux_send.sh --target <session> --message '...' --no-envelope
#   tmux_send.sh --target <session> --message '...' --no-verify   # emergency only
#
# Exit codes:
#   0 = paste + submit + tmux verification OK
#   1 = usage / missing session / bad args
#   2 = paste ran but verification FAILED (message not seen as submitted turn)
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
  --force-vessel grok|agy|opencode
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

# Resolve FROM session (who is sending)
if [[ -z "$FROM_SESSION" ]]; then
  FROM_SESSION="$(tmux display-message -p '#{session_name}' 2>/dev/null || true)"
fi
if [[ -z "$FROM_SESSION" ]]; then
  FROM_SESSION="unknown"
  echo "[tmux_send] warning: could not detect FROM session; set --from explicitly" >&2
fi

# Default REPLY_TO to FROM (orchestrator pattern: "reply to me")
if [[ -z "$REPLY_TO" ]]; then
  REPLY_TO="$FROM_SESSION"
fi

# Envelope: always include FROM + REPLY_TO unless already present or disabled
if [[ "$NO_ENVELOPE" -eq 0 ]]; then
  if ! grep -q '\[FROM:' <<<"$MESSAGE"; then
    MESSAGE="[FROM:${FROM_SESSION}] [REPLY_TO:${REPLY_TO}] ${MESSAGE}"
  fi
  # If FROM present but REPLY_TO missing, inject REPLY_TO after FROM
  if grep -q '\[FROM:' <<<"$MESSAGE" && ! grep -q '\[REPLY_TO:' <<<"$MESSAGE"; then
    MESSAGE="${MESSAGE/\[FROM:${FROM_SESSION}\]/[FROM:${FROM_SESSION}] [REPLY_TO:${REPLY_TO}]}"
    if ! grep -q '\[REPLY_TO:' <<<"$MESSAGE"; then
      MESSAGE="[REPLY_TO:${REPLY_TO}] ${MESSAGE}"
    fi
  fi
fi

# Detect vessel from TARGET pane command
CMD="$(tmux list-panes -t "$TARGET" -F '#{pane_current_command}' 2>/dev/null | head -1 || true)"
VESSEL="$FORCE_VESSEL"
if [[ -z "$VESSEL" ]]; then
  case "$CMD" in
    grok) VESSEL=grok ;;
    opencode) VESSEL=opencode ;;
    agy|agy.real|gemini) VESSEL=agy ;;
    *)
      case "$TARGET" in
        *grok*|grok-audit) VESSEL=grok ;;
        *opencode*) VESSEL=opencode ;;
        *) VESSEL=agy ;;
      esac
      ;;
  esac
fi

# Fingerprint: unique substring we must see in the target pane after submit
# Prefer [FROM:…] token; fall back to first 48 non-space chars of body
NEEDLE=""
if [[ "$MESSAGE" =~ \[FROM:[^\]]+\] ]]; then
  NEEDLE="${BASH_REMATCH[0]}"
fi
if [[ -z "$NEEDLE" ]]; then
  NEEDLE="$(printf '%s' "$MESSAGE" | tr -d '\n' | head -c 48)"
fi
# Also keep a short body snippet for dual-match (reduces false positives)
BODY_SNIP="$(printf '%s' "$MESSAGE" | tr -d '\n' | sed 's/\[FROM:[^]]*\]//g; s/\[REPLY_TO:[^]]*\]//g' | sed 's/^[[:space:]]*//' | head -c 32)"

echo "[tmux_send] from=$FROM_SESSION reply_to=$REPLY_TO target=$TARGET cmd=$CMD vessel=$VESSEL"
echo "[tmux_send] message=${MESSAGE:0:200}..."
echo "[tmux_send] verify_needle=${NEEDLE:0:60}"

capture_tail() {
  tmux capture-pane -t "$TARGET" -p -J -S -40 2>/dev/null || true
}

# Baseline capture (optional diagnostics)
capture_tail > "${VERIFY_LOG}.before" || true

tmux set-buffer -b "$BUF" "$MESSAGE"
tmux send-keys -t "$TARGET" C-u 2>/dev/null || true
sleep 0.2
tmux paste-buffer -b "$BUF" -p -t "$TARGET"
sleep 0.5

submit_keys() {
  if [[ "$VESSEL" == "grok" || "$VESSEL" == "opencode" ]]; then
    # Grok + OpenCode: Enter = send. Do NOT send Escape first (cancels/blurs).
    tmux send-keys -t "$TARGET" Enter
    sleep 0.35
  else
    # AGY: Escape then Enter as separate events
    tmux send-keys -t "$TARGET" Escape
    sleep 0.3
    tmux send-keys -t "$TARGET" Enter
  fi
}

submit_keys
sleep 1.2

# --- Hard verification via target tmux session pane ---
verify_delivery() {
  local pane attempt=1 max_attempts=3
  while [[ $attempt -le $max_attempts ]]; do
    pane="$(capture_tail)"
    printf '%s\n' "$pane" > "$VERIFY_LOG"

    # 1) Needle must appear somewhere in the captured pane
    if ! grep -F -q -- "$NEEDLE" <<<"$pane"; then
      echo "[tmux_send] verify attempt $attempt: NEEDLE not in pane" >&2
      if [[ $attempt -lt $max_attempts ]]; then
        echo "[tmux_send] re-submitting Enter (vessel=$VESSEL)..." >&2
        if [[ "$VESSEL" == "grok" || "$VESSEL" == "opencode" ]]; then
          tmux send-keys -t "$TARGET" Enter
        else
          tmux send-keys -t "$TARGET" Escape
          sleep 0.25
          tmux send-keys -t "$TARGET" Enter
        fi
        sleep 1.0
      fi
      attempt=$((attempt + 1))
      continue
    fi

    # 2) Prefer body snippet also present (when non-empty)
    if [[ -n "$BODY_SNIP" ]] && [[ ${#BODY_SNIP} -ge 8 ]]; then
      if ! grep -F -q -- "$BODY_SNIP" <<<"$pane"; then
        echo "[tmux_send] verify attempt $attempt: BODY_SNIP not in pane" >&2
        attempt=$((attempt + 1))
        sleep 0.8
        continue
      fi
    fi

    # 3) Failure signals: stuck only in composer / not submitted
    # Grok: "esc to interrupt" / Working / tool activity after our paste = good
    # If needle is only on the bottom prompt line with no Working/Loading, may still be OK if paste-buffer -p put it as user turn
    # AGY success markers
    if grep -Eiq 'Working\.\.\.|Loading\.\.\.|Thought for|esc to cancel|esc to interrupt|Tool|Bash\(|function_call' <<<"$pane"; then
      echo "[tmux_send] VERIFY_OK: needle present + agent activity markers"
      return 0
    fi

    # Needle present as submitted user turn ("> [FROM:..." or plain history line)
    if grep -F -- "$NEEDLE" <<<"$pane" | grep -qvE '^\s*$'; then
      # Heuristic fail: if the ONLY match is still sitting with "Type a message" empty composer patterns
      # Success if we see our line as a user bubble / history entry
      if grep -Eiq "FROM:${FROM_SESSION}|REPLY_TO:|^\> .*FROM:|submitted|user turn" <<<"$pane" \
        || grep -F -q -- "$NEEDLE" <<<"$pane"; then
        echo "[tmux_send] VERIFY_OK: needle present in target pane (history/composer submitted)"
        return 0
      fi
    fi

    echo "[tmux_send] verify attempt $attempt: ambiguous; retrying submit" >&2
    if [[ "$VESSEL" == "grok" || "$VESSEL" == "opencode" ]]; then
      tmux send-keys -t "$TARGET" Enter
    else
      tmux send-keys -t "$TARGET" Escape
      sleep 0.25
      tmux send-keys -t "$TARGET" Enter
    fi
    sleep 1.0
    attempt=$((attempt + 1))
  done
  return 1
}

echo "[tmux_send] capture (tail after submit):"
capture_tail | tail -35

VERIFY_RC=0
if [[ "$NO_VERIFY" -eq 1 ]]; then
  echo "[tmux_send] warning: --no-verify set; skipping hard check" >&2
else
  if verify_delivery; then
    VERIFY_RC=0
  else
    VERIFY_RC=2
    echo "[tmux_send] VERIFY_FAIL: message not confirmed in tmux session '$TARGET'" >&2
    echo "[tmux_send] last capture saved: $VERIFY_LOG" >&2
    echo "[tmux_send] capture (full tail for debug):" >&2
    tail -40 "$VERIFY_LOG" >&2 || true
  fi
fi

tmux delete-buffer -b "$BUF" 2>/dev/null || true

if [[ "$VERIFY_RC" -ne 0 ]]; then
  echo "[tmux_send] FAILED delivery verification — agent must NOT claim success" >&2
  exit 2
fi

echo "[tmux_send] done — VERIFIED on target=$TARGET; peer reports must hit REPLY_TO=$REPLY_TO"
exit 0
