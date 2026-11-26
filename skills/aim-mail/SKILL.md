---
name: aim-mail
description: >
  Canonical A-Mail (`amail` / `aim-mail`) cross-OS, cross-harness inter-agent communication
  and wake-dispatch protocol powered by `aim-mailbox`. Supersedes `aim-communicate` and retires
  standalone `tmux` shell paste wrappers. Trigger on A-Mail, amail, aim-mail, aim-mailbox,
  or legacy aim-communicate requests. Slash: /aim-mail.
---

# A-Mail (`amail` / `aim-mail`): Cross-OS Inter-Agent Mail & Dispatch Protocol

**A-Mail** (`amail` / `aim-mail`, powered by `aim-mailbox`) is the **sole** inter-agent transport across **Linux, WSL2, macOS, and Native Windows 11** and across every supported harness (**Antigravity Desktop/IDE, Antigravity CLI, OpenCode, Grok Build, Codex CLI, VS Code Agent Mode, and POSIX `tmux`**).

- `amail` and `aim-mail` are identical first-class entrypoints (`0` runtime pip dependencies, `0` resident daemons).
- **Sole Transport Rule:** Never use deprecated `aim-communicate`, retired shell paste wrappers, raw `tmux send-keys`, `Escape`-before-`Enter`, or `aim-chalkboard`. POSIX `tmux` targets route exclusively through `amail`'s native `--driver tmux` (exact `=session:` targeting + `Enter`-only 1-line doorbell).

---

## 0. MANDATORY: Identity, Permission Gate & Fleet Guards

1. **`FROM` + `REPLY_TO` Required:** Every message must set `--from <your-agent-id>` and `--reply-to <target-agent-id>` (defaults to `--from` unless an orchestrator specifies another recipient). Verify your logical registration first:
   ```bash
   amail agents
   tmux display-message -p '#{session_name}' 2>/dev/null || true
   ```
2. **Operator Permission Mandate (`--operator-approved`):**
   - Never initiate unsolicited peer-to-peer conversations without explicit Operator authorization (`--operator-approved`).
   - Receiving an inbound A-Mail envelope pre-authorizes a **1-hop reply** (`max_hops=1`) back to `reply_to` on the same `thread_id`.
   - End final closeout reports with `DO NOT reply` (and `--no-ack-required` when sending via `amail send`).
3. **DND & Live-Vertical WIP Guards:**
   - Respect `agents.json` / workspace DND and BUSY states and WIP locks. Never wake a DND-protected agent or mutate an active vertical mid-batch—file a follow-up ticket instead.

---

## 1. Registering Project Workspaces (One-Time, Handoff-Proof Setup)

Register **project workspaces** (`--cwd` or `--tmux-session`) rather than pinning ephemeral conversation UUIDs so `/aim-handoff` session rotations resolve automatically:

```bash
# Antigravity CLI (auto-resolves latest top-level conversation for --cwd):
amail register aim-auditor --driver agy-cli --cwd ~/aim-agents/aim-auditor --clear-session-id

# Windows 11 Antigravity Desktop / IDE (wakes even while minimized):
amail install-agy-sidecar
amail register copy-cat --driver agy-desktop-sidecar --cwd "C:\Projects\copy-cat" --clear-session-id

# POSIX / WSL2 tmux pane (exact =session: targeting + Enter-only 1-line doorbell):
amail register aim-connect --driver tmux --tmux-session aim-connect --cwd ~/aim-connect

# OpenCode HTTP / Grok Build / Codex CLI / VS Code:
amail register backend-dev --driver opencode-http --http-url http://127.0.0.1:4096
amail register grok-audit --driver grok-cli --cwd ~/aim-agents/aim-auditor
amail register codex-dev --driver codex-cli --cwd ~/aim-codex
amail register ide-agent --driver vscode-chat --cwd ~/my-project

# Optional (<2ms empty-inbox) turn-boundary hook installer:
amail install-hooks --harness agy --agent aim-auditor
```

- **WSL2 ↔ Native Windows 11 Shared Mailbox:** Set `export AIM_MAILBOX_DIR="/mnt/c/Users/<WindowsUser>/.aim/mailbox"` in WSL2 (`~/.bashrc`) so Windows 11 (`%USERPROFILE%\.aim\mailbox`) and WSL2 share one lock-free atomic Maildir with zero SQLite WAL contention.
- **Canonical Skill Install Roots:** `${PROJECT_ROOT:-.}/.gemini/skills/aim-mail`, `$HOME/.gemini/antigravity-cli/skills/aim-mail`, `${PROJECT_ROOT:-.}/.grok/skills/aim-mail`, `$HOME/.grok/skills/aim-mail`, `$HOME/.codex/skills/aim-mail`, and `$HOME/.config/opencode/skills/aim-mail`.

---

## 2. Sending a Dispatch (`amail send` / `aim-mail send`)

Write large specs or audit reports to disk first (`artifacts/`, `docs/`), keep `--body` concise, and attach paths with `--ref`:

```bash
# Synchronous wake for tmux, CLI, or HTTP peers:
amail send \
  --from aim-joshua \
  --to aim-auditor \
  --reply-to aim-joshua \
  --subject "Delta Audit" \
  --body "[DISPATCH] Audit latest release against README.md and report findings." \
  --ref artifacts/AUDIT_TARGET.md \
  --priority normal \
  --operator-approved \
  --wake \
  --json

# Messaging a Windows 11 `agy-desktop-sidecar` target from WSL2 (OMIT --wake!):
# `ANTIGRAVITY_LS_ADDRESS` exists inside the Windows Sidecar process; omitting `--wake`
# queues the envelope for the live Sidecar `watch` loop (~1.5s delivery).
amail send \
  --from aim-mailbox \
  --to joshua-win11 \
  --reply-to aim-mailbox \
  --subject "Cross-OS Sync" \
  --body "[DISPATCH] Verify Windows desktop build." \
  --operator-approved \
  --json
```

- **Fail-Closed Wake Verification:** `--wake` exits `0` only on verified delivery (`rc=2` on unregistered target, `driver=none`, missing `--operator-approved`, cross-OS `HOST_MISMATCH` / `SIDECAR_CONTEXT_REQUIRED`, or deferred priority/busy state without `--allow-deferred`). Never claim "sent/woken" on a non-zero exit—inspect `stderr` and `amail inbox <target> --state all --json`.

---

## 3. Turn-Boundary Check, Reading, Replying, Waiting & ACKing

Run `amail check` at turn boundaries (never in a busy spin loop), read active mail before acting, and close loops cleanly:

```bash
# 1. Fast (<2ms) turn-boundary check & active inbox inspection
amail check <my-agent-id> --inject --quiet
amail inbox <my-agent-id> --state active

# 2. Read and claim an inbound envelope
amail read <my-agent-id> <message_id> --claim

# 3a. 1-hop reply to sender's reply_to (auto-increments hop_count & auto-ACKs parent;
#     omit --wake when reply_to uses agy-desktop-sidecar on another OS)
amail reply <my-agent-id> <message_id> \
  --body "1. COMPLETED: Landed SHA abc1234, CI green. 2. NOTES: None. 3. NEXT: DO NOT reply." \
  --ref artifacts/REPORT.md \
  --no-ack-required \
  --wake

# 3b. Or acknowledge a closeout report with no reply needed
amail ack <my-agent-id> <message_id> --note "Received closeout; loop closed."

# 4. Zero-LLM synchronous wait (orchestrators awaiting a thread reply)
amail wait <my-agent-id> --thread-id <thread_id> --timeout 120 --json
```

---

## 4. Deterministic Report Format

Structure inter-agent replies concisely and close bounded threads explicitly:

```text
1. COMPLETED / AGREED (issue #s, commit SHAs, CI status)
2. FINDINGS / NOTES
3. BLOCKERS / QUESTIONS (only if escalation is required)
4. NEXT (end with "DO NOT reply" when closing the 1-hop loop)
```
