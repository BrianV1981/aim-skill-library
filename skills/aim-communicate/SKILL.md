---
name: aim-communicate
description: >
  Inter-agent messaging via tmux: short paste with FROM/REPLY_TO, vessel-specific
  submit keys, optional chalkboard file for bulk content. Use when messaging another
  agent in a tmux session or when the Operator asks you to talk to another agent.
---

# aim-communicate

Protocol for agents in different **tmux sessions** on the same host.

## Rules

1. **Operator approval required** — do not message another agent unless the Operator asked for it.
2. **Every message declares routing:**
   - **FROM** — exact tmux session *you* are in now  
   - **REPLY_TO** — exact session that must receive the reply (usually the orchestrator)
3. **Session name ≠ project name** — always use `tmux display-message` / `list-sessions`, never invent names.
4. **No secrets** in pastes. No open-ended agent↔agent chat loops.

## Discover sessions

```bash
tmux display-message -p '#{session_name}'   # your session
tmux list-sessions
tmux list-panes -a -F '#{session_name} #{pane_current_command} #{pane_current_path}'
tmux capture-pane -t <session> -p -J -S -20
```

Prefer idle peers (stable prompt) before pasting.

## Message envelope

```text
[FROM:<your_session>] [REPLY_TO:<session_to_answer>] [REPORT|DISPATCH] <one-line body>
```

Example:

```text
[FROM:my-orchestrator] [REPLY_TO:peer-session] [DISPATCH] Review PR — see planning-artifacts/NOTES.md
```

Dispatch files (bulk content on disk) should also state **FROM** and **REPLY_TO** in the header. Peers reply to **REPLY_TO** only unless the Operator lists a CC.

## Short paste (helper)

After install, from the skill directory:

```bash
bash scripts/tmux_send.sh \
  --target <peer_session> \
  --from "$(tmux display-message -p '#{session_name}')" \
  --reply-to <orchestrator_session> \
  --message 'Short status — full notes in planning-artifacts/REPORT.md'
```

The helper prefixes FROM/REPLY_TO when missing and applies the correct submit sequence.

## Manual short paste

```bash
FROM=$(tmux display-message -p '#{session_name}')
REPLY_TO=<session_from_dispatch>
SHORT="[FROM:${FROM}] [REPLY_TO:${REPLY_TO}] [REPORT] Closed task — see path/to/REPORT.md"

tmux set-buffer -b aim_comm_short "$SHORT"
tmux send-keys -t "$REPLY_TO" C-u
sleep 0.2
tmux paste-buffer -b aim_comm_short -p -t "$REPLY_TO"
sleep 0.5
# then submit — see below
```

## Submit by vessel (`pane_current_command`)

| Command | Vessel | Submit |
|---------|--------|--------|
| `grok` | Grok TUI | **Enter only** (never Escape first — Esc cancels) |
| `opencode` | OpenCode TUI | **Enter only** |
| `agy` | Antigravity | **Escape**, pause, then **Enter** (separate `send-keys`) |

```bash
# Grok / OpenCode
tmux send-keys -t <target> Enter

# AGY
tmux send-keys -t <target> Escape
sleep 0.3
tmux send-keys -t <target> Enter
```

## Verify delivery

```bash
sleep 1.2
tmux capture-pane -t <target> -p -J -S -30 | tail -35
```

Success: message is a **submitted** user turn (not stuck in the composer).

## Bulk content

Write long specs/patches to a file under the project (`planning-artifacts/`, `docs/`).  
Paste only a one-line pointer + envelope. Structure multi-step replies as:

```text
1. DONE / AGREED
2. NOTES
3. QUESTIONS
4. NEXT
```

No free-form back-and-forth without the Operator.
