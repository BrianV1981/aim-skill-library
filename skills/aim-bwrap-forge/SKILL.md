---
name: aim-bwrap-forge
description: >
  Dynamically spin up bubblewrap (bwrap) isolated sandbox directories and optional
  tmux co-agent sessions for untrusted or multi-tenant work. Use when the Operator
  asks for a bwrap sandbox, isolated co-agent, or forge a sandbox tenant. Slash:
  /aim-bwrap-forge.
---

# aim-bwrap-forge

## Overview

Spawn a **bubblewrap-isolated** workspace under `~/.aim/sandboxes/`, optionally launch
a co-agent CLI inside it via **tmux**, and tear down safely when done.

Works on **Grok** and **AGY** vessels. Communication with the sandbox agent uses
`aim-communicate` (same FROM / REPLY_TO rules). Co-agent DNA lives in **aim-coagents**
(companion repo) — this skill does not vendor it.

## Requirements

```bash
command -v bwrap   # bubblewrap
command -v tmux
# optional: co-agent blueprints from aim-coagents companion
```

If `bwrap` is missing, stop and tell the Operator (do not invent a sandbox).

## 1. Create sandbox directory

```bash
SANDBOX_ID="sb_$(date +%s)_$RANDOM"
SANDBOX_ROOT="${AIM_SANDBOX_ROOT:-$HOME/.aim/sandboxes}/$SANDBOX_ID"
mkdir -p "$SANDBOX_ROOT"/{work,tmp,home}
echo "$SANDBOX_ROOT"
```

Never use machine-local hard-coded home paths other than `$HOME` / env overrides.

## 2. Minimal bwrap shell (interactive proof)

Read-only host OS; write only inside the sandbox:

```bash
bwrap \
  --unshare-all \
  --die-with-parent \
  --ro-bind /usr /usr \
  --ro-bind /lib /lib \
  --ro-bind /lib64 /lib64 \
  --ro-bind /bin /bin \
  --ro-bind /sbin /sbin \
  --ro-bind /etc /etc \
  --proc /proc \
  --dev /dev \
  --tmpfs /tmp \
  --bind "$SANDBOX_ROOT/work" /work \
  --bind "$SANDBOX_ROOT/home" /sbox-home \
  --setenv HOME /sbox-home \
  --chdir /work \
  -- /bin/bash
```

Adjust binds if `/lib64` is absent (some hosts use only `/lib`). Prefer **adding**
read-only binds for project tools the Operator approves; never bind secrets dirs
unless explicitly approved.

## 3. Optional: tmux co-agent inside sandbox

Detect host CLI before choosing the inner command:

| Host vessel | Inner command example |
|-------------|----------------------|
| Grok | `grok` (or path to grok in approved bind) |
| AGY | `agy` / `agy.real` |

```bash
SESSION="bwrap_${SANDBOX_ID}"
# Example: confined shell first (safer default)
tmux new-session -d -s "$SESSION" \
  "bwrap --unshare-all --die-with-parent \
    --ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /bin /bin \
    --proc /proc --dev /dev --tmpfs /tmp \
    --bind \"$SANDBOX_ROOT/work\" /work \
    --bind \"$SANDBOX_ROOT/home\" /sbox-home \
    --setenv HOME /sbox-home --chdir /work \
    -- /bin/bash"

tmux list-sessions | grep -F "$SESSION"
```

Only start a full agent CLI inside bwrap when the Operator approves, and only with
binds that include that CLI’s runtime. Prefer confining a **task script** over a full
interactive agent when isolation is the goal.

## 4. Communicate

Use **`aim-communicate`**: declare FROM (your session) and REPLY_TO; paste short
messages; verify with capture-pane / `tmux_send.sh`. Do not open open-ended multi-hop
chat without Operator approval.

## 5. Tear-down

1. Confirm the sandbox agent finished (or Operator aborts).
2. Collect outputs from `$SANDBOX_ROOT/work`.
3. Kill session: `tmux kill-session -t "$SESSION"` (if created).
4. Remove sandbox only with Operator OK: `rm -rf "$SANDBOX_ROOT"`.

## Safety

- No secrets in sandbox binds unless Operator-approved.
- No `rm -rf` of paths outside `$SANDBOX_ROOT`.
- Do not force-push or touch host git repos from inside the sandbox without scope.
- If bwrap flags fail on this distro, report stderr; do not weaken isolation silently.
