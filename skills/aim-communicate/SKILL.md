---
name: aim-communicate
description: >
  Cross-OS, cross-harness inter-agent communication (v2.0) powered by `aim-mailbox` (`aim-mail` CLI)
  with POSIX `tmux_send.sh` (`Enter`-only) fallback. Enforces Operator permission gates, mandatory
  FROM + REPLY_TO routing, 1-hop loop prevention, and verified delivery across Windows 11 Desktop
  Sidecars, WSL2, macOS, and Linux (`agy`, `grok`, `opencode`, `codex`, `vscode`, `tmux`).
---

# AIM-Communicate (`v2.0`): Cross-OS Inter-Agent Mail & Dispatch Protocol

Agents across A.I.M. run on different operating systems (**Linux, WSL2, macOS, and Native Windows 11**) and inside different harnesses (**Antigravity Desktop/IDE, Antigravity CLI, OpenCode, Grok Build, Codex, VS Code, and POSIX `tmux`**).

`aim-communicate` (`v2.0`) uses **`aim-mailbox` (`aim-mail` CLI)** as the universal transport and wake-up layer across all OSes and harnesses, with `scripts/tmux_send.sh` preserved as a direct POSIX `tmux` fallback when `aim-mail` is not installed.

---

## 0. MANDATORY: Identity + Reply Routing (Never Skip)

Every inter-agent message **MUST** declare:
1. **`FROM`** — your exact logical agent ID (or current `tmux` session name when using the `tmux` fallback).
2. **`REPLY_TO`** — the exact target agent/session that must receive the response (defaults to `FROM` unless the Operator specifies another orchestrator).

Discover your logical registration or current `tmux` session first:
```bash
# Check registered logical agents in aim-mailbox:
aim-mail agents

# If running inside a POSIX tmux session, verify your exact session name:
tmux display-message -p '#{session_name}' 2>/dev/null || true
```
**Do not guess** `aim-grok` vs. `aim-auditor` — verify your identity and read `reply_to` from any incoming envelope before replying.

---

## 1. Operator Permission Mandate

You are **strictly forbidden** from initiating unsolicited peer-to-peer messages unless the Operator explicitly authorizes it:
- Operator instructions such as *"tell aim-auditor …"*, *"dispatch to copy-cat …"*, or *"communicate with …"* grant approval for that target and task (`--operator-approved`).
- Receiving an inbound `aim-mail` envelope (or `aim-communicate` dispatch) **pre-authorizes a 1-hop reply** back to its `reply_to` target on the same `thread_id`.
- Never open open-ended multi-hop agent chat loops without the Operator in the loop (`max_hops=1` default; send `[DO NOT REPLY]` / `--no-ack-required` on final closeout reports).

---

## 2. Primary Protocol: `aim-mail` (`aim-mailbox` — All OSes & Harnesses)

`aim-mail` stores messages atomically in a lock-free JSON Maildir (`~/.aim/mailbox` or `$AIM_MAILBOX_DIR`) safe across Linux, macOS, native Windows 11 NTFS, and WSL2 `/mnt/c` shares, and wakes sleeping or minimized peers via their registered driver (`agy-desktop-sidecar`, `agy-cli`, `opencode-http`, `grok-cli`, `codex-cli`, `vscode-chat`, `tmux`, or `command`).

### 2a. Registering Your Agent or Target (One-Time Setup)

```bash
# Antigravity CLI (Windows 11, WSL2, macOS, Linux):
aim-mail register aim-auditor --driver agy-cli --cwd ~/aim-agents/aim-auditor

# Windows 11 Antigravity Desktop / IDE (even while minimized):
aim-mail install-agy-sidecar
aim-mail register copy-cat --driver agy-desktop-sidecar --session-id <conversation-uuid>

# OpenCode Server / Desktop:
aim-mail register backend-dev --driver opencode-http --http-url http://127.0.0.1:4096

# Grok Build CLI:
aim-mail register grok-audit --driver grok-cli --session-id grok-audit --cwd ~/aim-auditor

# Live POSIX / WSL2 tmux pane (1-line Enter-only doorbell):
aim-mail register aim-connect --driver tmux --tmux-session aim-connect
```

> **WSL2 ↔ Native Windows 11 Shared Mailbox:** Set `export AIM_MAILBOX_DIR="/mnt/c/Users/<WindowsUser>/.aim/mailbox"` in WSL2 so WSL2 CLI agents and native Windows 11 Desktop/CLI agents share one atomic Maildir with zero SQLite lock contention.

### 2b. Sending a Dispatch or Handoff

Write large specifications or reports to disk first (`artifacts/`, `docs/`), keep `--body` concise, and attach file paths via `--ref`:

```bash
aim-mail send \
  --from aim-joshua \
  --to aim-auditor \
  --reply-to aim-joshua \
  --subject "Pass 15 Delta Audit" \
  --body "[DISPATCH] Audit v0.1.0 against README.md and report findings." \
  --ref artifacts/AUDIT_TARGET.md \
  --operator-approved \
  --wake \
  --json
```
- `--wake` immediately triggers the recipient's configured driver (`rc=0` only if verified; otherwise `aim-mail pulse` / Sidecar `watch` delivers asynchronously).
- **Never claim "sent/woken"** if `--wake` exits non-zero — inspect `stderr` or `aim-mail inbox <target> --state all --json`.

### 2c. Checking, Reading, Replying & Acknowledging Mail

When woken by `aim-mailbox` (or instructed by the Operator to check your inbox):

```bash
# 1. Inspect unread envelopes
aim-mail inbox <my-agent-id>

# 2. Read and claim the message
aim-mail read <my-agent-id> <message_id> --claim

# 3a. Reply to sender's reply_to (auto-increments hop_count & auto-ACKs parent)
aim-mail reply <my-agent-id> <message_id> \
  --body "1. AGREED: Verified 15/15 tests green. 2. NOTES: None. 3. NEXT: Promoted." \
  --ref artifacts/AUDIT_REPORT.md \
  --wake

# 3b. Or acknowledge a 1-hop closeout report with no reply needed
aim-mail ack <my-agent-id> <message_id> --note "Received closeout; loop closed."
```

### 2d. Zero-Token Waiting (Orchestrators)

When waiting synchronously for a peer's reply without burning LLM polling turns:
```bash
aim-mail wait <my-agent-id> --thread-id <thread_id> --timeout 120 --json
```

---

## 3. POSIX `tmux` Direct Fallback (`scripts/tmux_send.sh`)

On Linux/WSL/macOS hosts where `aim-mail` is not on `PATH` and both agents live in local `tmux` sessions, use the bundled `tmux_send.sh` helper with **short 1–3 line pointers** (write long content to a file first — never paste 20+ line novels directly into a TUI composer).

Canonical installed skill helper paths (keep all vessels in sync):
- `$PROJECT_ROOT/.grok/skills/aim-communicate/scripts/tmux_send.sh` — Grok project install
- `$PROJECT_ROOT/.gemini/skills/aim-communicate/scripts/tmux_send.sh` — AGY project install
- `$HOME/.gemini/antigravity-cli/skills/aim-communicate/scripts/tmux_send.sh` — Global AGY CLI
- `$HOME/.gemini/config/skills/aim-communicate/scripts/tmux_send.sh` — Global AGY 2.0
- `$HOME/.grok/skills/aim-communicate/scripts/tmux_send.sh` — Global Grok CLI

```bash
bash "$PROJECT_ROOT/.gemini/skills/aim-communicate/scripts/tmux_send.sh" \
  --target aim-auditor \
  --from "$(tmux display-message -p '#{session_name}')" \
  --reply-to aim-joshua \
  --message '[DISPATCH] Audit #24 — read artifacts/DISPATCH.md'
```

### Critical `tmux` Submit Rules (`#19` Hardened)
1. **`Enter` ONLY Across All Vessels (`agy`, `grok`, `opencode`, `codex`):** **NEVER send `Escape` before `Enter`.** On Antigravity CLI (`1.4+`), Grok CLI, and OpenCode, `Escape` cancels/deletes multi-line paste chips (`[Pasted text #1 +N lines]`) or clears the composer.
2. **Pre-Submit Composer Check:** Confirm the pasted text (or `[Pasted text` chip) is present in the composer before sending `Enter`.
3. **Mandatory Deep-Capture Verification (`-S -300`):** Answering only in your own chat is **NOT** delivery. Trust `tmux_send.sh` exit code `0` (`VERIFY_OK`); on exit `2` (`VERIFY_FAIL`), inspect `tmux capture-pane -t <target> -p -J -S -300` before retrying so you never double-submit an already-accepted turn.

---

## 4. Loop Prevention & Structured Reports

Format peer reports deterministically and close the loop cleanly:
```text
1. AGREED / COMPLETED (issue #s, commit SHAs)
2. FINDINGS / NOTES
3. BLOCKERS / QUESTIONS (only if escalation needed)
4. NEXT (or [DO NOT REPLY] when closing the loop)
```

---

## 5. Changelog & Operational Lessons
1. **2026-07-12 (`grok` Escape bug & wrong reply target):** `Escape` cleared pastes on Grok, and omitting `REPLY_TO` misrouted reports to `aim-grok` instead of `grok-audit`. Enforced mandatory `FROM` + `REPLY_TO`.
2. **2026-07-19 (Chat-only reply):** Replying in local chat never reached the peer. Enforced target-side delivery verification (`rc=2` on `VERIFY_FAIL`).
3. **2026-10-21 (`#17` / `#19` AGY `Escape` wipe & OS skill drift):** `Escape`→`Enter` deleted 20-line pastes on `agy 1.4.4`, shallow `-S -40` + `BODY_SNIP` caused false `VERIFY_FAIL` duplicates on `[Pasted text #1 +N lines]` chips, and divergent Windows vs. Linux `SKILL.md` overrides drifted.
4. **2026-11-20 (`v2.0` `aim-mailbox` unification, `#24`):** Unified all OSes and harnesses under `aim-mail` (`aim-mailbox` atomic Maildir + Windows 11 Sidecar / CLI / HTTP / `tmux` drivers), retired the divergent `vessels/agy/skills/aim-communicate` override, and hardened `tmux_send.sh` to `Enter`-only submit with pre-submit composer verification and `-S -300` deep capture.
