---
name: aim-communicate
description: >
  Inter-agent communication via tmux with permission gates, chalkboard + short-paste
  protocol (Grok/AGY-hardened). MUST declare sender session and REPLY_TO session on every
  message. MUST verify delivery by inspecting the target tmux session (capture-pane).
  Use when messaging another AI agent in tmux, board-room/swarm chat, or when the user
  asks to talk to another agent. Updated 2026-07-19 (mandatory pane verification).
---

# AIM-Communicate: Inter-Agent Tmux Protocol

You may operate where multiple AI agents run in different tmux sessions (board room / swarm).
Common sessions: `aim-agy`, `aim-grok`, `grok-audit`, `aim-connect`, `aim-youtube`, reincarnation vessels (`agy_reincarnation_*`, `grok_reincarnation_*`), `ayrianna-scraper`, etc.

---

## 0. MANDATORY: Session identity + reply routing (do not skip)

**Every inter-agent message MUST state:**

1. **FROM** — the **exact** tmux session **you are running in now**  
2. **REPLY_TO** — the **exact** tmux session the peer must answer (almost always = the orchestrator’s FROM)  

### 0a. Discover your own session (always run first)

```bash
# Preferred (when your pane is the active one in a known session):
tmux display-message -p '#{session_name}'

# If that is empty/wrong (nested/detached), find by cwd or list:
tmux list-panes -a -F '#{session_name} #{pane_current_command} #{pane_current_path}'
```

Record that name. **Do not guess** `aim-grok` vs `grok-audit`. They are different orchestrators.

### 0b. Required Message Foundation

When you communicate with another agent, you MUST lay the foundation along with the message. Your message must begin with exactly this block:

```text
To: <target_tmux_session_name> (You are receiving this in tmux session <target_tmux_session_name>. Note: Agents are identified by their tmux session name)
From: <your_tmux_session_name> (My tmux session name)
INSTRUCTION: Please review your `aim-communicate` skill BEFORE responding to this message.

[REPORT|DISPATCH from <role>] <message body>
```

**Examples (correct):**

```text
To: agy_reincarnation_1783842559 (You are receiving this in tmux session agy_reincarnation_1783842559...)
From: grok-audit (My tmux session name)
INSTRUCTION: Please review your `aim-communicate` skill BEFORE responding to this message.

[DISPATCH] Merge #92-95 — read /path/DISPATCH.md
```

**Wrong (causes misdelivery):**

```text
[REPORT from aim-agy] Merged #92-#95 — read /path/REPORT.md
# Missing the To/From/Instruction foundation → causes confusion and broken workflows.
```

### 0c. Dispatch files MUST include

In every chalkboard dispatch:

```markdown
**FROM (sender tmux session):** `grok-audit`
**REPLY_TO (mandatory reply session):** `grok-audit`
**Also notify (optional secondary):** `aim-grok`   # only if Operator wants a CC
```

Peer agents **must** paste reports to **REPLY_TO only** unless Operator adds a CC list.  
If both `aim-grok` and `grok-audit` are listed, **primary is always REPLY_TO**.

### 0d. Incident (2026-07-12)

Orchestrator on **`grok-audit`** ordered aim-agy to report to `grok-audit`. The agent reported only to **`aim-grok`**, so the live orchestrator did not see the paste. Fix: mandatory `[FROM:…] [REPLY_TO:…]` on every short paste + dispatch header.

### 0e. Incident (2026-07-19) — “replied in chat only”

Orchestrator answered another agent **only in its own chat UI** and never pasted into the peer’s tmux session. Peer waited forever. Fix: **delivery is not done until §3d / §3e verification passes** against the **target** session pane.

---

## 1. Permission mandate

You are **forbidden** from unilaterally messaging another agent's tmux session unless the Operator explicitly approves.

- Operator text like "tell aim-agy …" / "communicate with …" **is** approval for that target and intent.
- Incoming aim-communicate paste from another session **is** approval to reply to their REPLY_TO / From session.
- Do not open open-ended multi-hop chat without Operator in the loop.

## 2. Discover targets first

```bash
tmux list-sessions
tmux list-panes -a -F '#{session_name} #{pane_current_command} #{pane_current_path}'
tmux capture-pane -t <session> -p -J -S -20
```

Wait for idle prompt when possible.

| `pane_current_command` | Vessel | Submit |
|------------------------|--------|--------|
| `grok` | Grok TUI | **Enter only** (§4a) |
| `opencode` | OpenCode TUI | **Enter only** (same as Grok; §4a) |
| `agy` / `agy.real` | Antigravity | **Escape, then Enter** (§4b) |

**Note:** Project name ≠ session name. An aim-agy agent may run in `agy_reincarnation_*` or `aim-agy`. Always use the **tmux session string**, not the repo name alone.

## 3. Chalkboard + short paste

### 3a. Write full content to disk

Prefer paths under the target or sender project (`planning-artifacts/`, `docs/`).

### 3b. Helper script (required on Grok vessels)

```bash
# Auto-detect FROM session; force REPLY_TO into the message prefix if missing.
# Exits 0 only if target tmux pane verification passes; exits 2 on VERIFY_FAIL.
bash $PROJECT_ROOT/.gemini/skills/aim-communicate/scripts/tmux_send.sh \
  --target ayrianna-scraper \
  --from "$(tmux display-message -p '#{session_name}')" \
  --reply-to grok-audit \
  --message 'Merged #92-#95 — read /abs/path/REPORT.md'
```

The script:

1. Prefixes `[FROM:…] [REPLY_TO:…]` when missing  
2. Pastes with correct vessel submit (Grok Enter / AGY Esc→Enter)  
3. **Captures the target session pane and verifies the message is present**  
4. Retries submit once/twice if needed  
5. **Exits non-zero if verification fails** — you must treat that as “not sent”

Canonical script path (keep vessels in sync):

- `$PROJECT_ROOT/.grok/skills/aim-communicate/scripts/tmux_send.sh`
- `$PROJECT_ROOT/.gemini/skills/aim-communicate/scripts/tmux_send.sh`
- `~/.gemini/antigravity-cli/skills/aim-communicate/scripts/tmux_send.sh` (if universally installed)

### 3c. Manual short paste (only if script unavailable)

```bash
FROM=$(tmux display-message -p '#{session_name}')
TARGET=ayrianna-scraper
REPLY_TO=grok-audit

cat << EOF > /tmp/aim_msg.txt
To: ${TARGET} (You are receiving this in tmux session ${TARGET}. Note: Agents are identified by their tmux session name)
From: ${FROM} (My tmux session name)
INSTRUCTION: Please review your \`aim-communicate\` skill BEFORE responding to this message.

[REPORT from ${FROM}] Closed #N — read /abs/path/REPORT.md
EOF

tmux load-buffer /tmp/aim_msg.txt
tmux paste-buffer -p -t "$TARGET"
# vessel-specific submit — §4
# THEN you MUST run §3e verification yourself
```

### 3d. MANDATORY — Verify delivery by looking at the target tmux session

**Answering only in your own chat is NOT delivery.**  
After every paste (script or manual), you MUST confirm the **target** session shows your message.

#### Preferred: trust `tmux_send.sh` exit code

| Exit | Meaning | Agent duty |
|------|---------|------------|
| `0` | `VERIFY_OK` — needle found in target pane | You may tell Operator “sent” |
| `2` | `VERIFY_FAIL` | **Do not claim success**; re-send or escalate |
| `1` | bad args / missing session | Fix target name / args |

#### Required manual verification (always if not using script, or to double-check)

```bash
TARGET=<exact_session>
NEEDLE='[FROM:grok-audit]'   # or another unique substring you pasted

sleep 1.2
tmux capture-pane -t "$TARGET" -p -J -S -40 | tee /tmp/aim_comm_verify_last.txt | tail -40

# Must find your message:
grep -F -- "$NEEDLE" /tmp/aim_comm_verify_last.txt
```

**Success signals (any strong combo):**

| Vessel | Success in capture |
|--------|-------------------|
| Grok | Your text appears as a **submitted user turn** (not only unsent composer fluff); often followed by agent activity |
| AGY | Your line visible **and** `Working...` / `Loading...` / tool activity / `Thought for` |
| Both | Unique fingerprint (`[FROM:…]`, absolute path, issue number) appears in the **last ~40 lines** of the target pane |

**Failure signals:**

| Signal | Meaning |
|--------|---------|
| `grep` finds nothing | Never landed / wrong session |
| Text only in bottom bar, no submit | Enter did not fire (Grok) or wrong submit recipe |
| Script exit `2` | Treat as not sent |

**Agent hard rules after verify:**

1. If verify fails → **retry once** with `tmux_send.sh`, then report failure to Operator.  
2. **Never** say “I told ayrianna-scraper …” unless verify passed.  
3. Paste a short excerpt of the capture (or script `VERIFY_OK` line) when reporting to Operator.

### 3e. Verification checklist (copy into your head)

```text
[ ] Correct TARGET session name (list-sessions, not project nickname)
[ ] FROM + REPLY_TO on the message
[ ] paste + correct submit (Grok Enter / AGY Esc→Enter)
[ ] capture-pane -t TARGET
[ ] unique needle grepped in that capture
[ ] only THEN claim delivery
```

## 4. Submit rules (vessel-specific)

### 4a. Grok (`grok`) — Enter only

```bash
tmux send-keys -t <target> Enter
# optional fallback: C-m
```

**Never** send Escape before Enter on Grok (Esc clears/cancels; does not send).

### 4b. AGY (`agy` / `agy.real`) — Escape then Enter (separate calls)

```bash
tmux send-keys -t <target> Escape
sleep 0.3
tmux send-keys -t <target> Enter
```

### 4c. Do / Don't

| Do | Don't |
|----|--------|
| Declare FROM + REPLY_TO every time | Assume “aim-grok” is the orchestrator |
| Detect vessel before submit | One submit recipe for all CLIs |
| `paste-buffer -p` | Long `send-keys` novels |
| **capture-pane verify on TARGET** | **Assume delivery / reply only in your chat** |
| Write report file first | Rely only on paste |
| Fail closed on VERIFY_FAIL | Pretend it worked |

## 5. Loop prevention

```text
Structure:
1. AGREED / MERGED (issue #s, SHAs)
2. DISAGREE / NOTES
3. QUESTIONS
4. NEXT
No open-ended chat loop.
```

## 6. Host map (re-check live with list-sessions)

| Session | Typical CLI | Typical cwd | Submit |
|---------|-------------|-------------|--------|
| `grok-audit` | `grok` | `~/grok-audit` | Enter |
| `aim-grok` | `grok` | `~/aim-grok` | Enter |
| `aim-agy` | `agy` | `~/aim-agy` | Esc→Enter |
| `agy_reincarnation_*` | `agy` | aim-agy worktrees | Esc→Enter |
| `ayrianna-scraper` | `agy.real` | `~/aim-ayrianna` | Esc→Enter |
| `aim-connect` | `agy` | `~/aim-connect` | Esc→Enter |
| `aim-opencode` | `opencode` | `~/aim-opencode` | Enter only |

**Orchestrator on this host often lives in `grok-audit`, not `aim-grok`.** Read REPLY_TO from the dispatch.

OpenCode vessel skill (extra notes):  
`~/aim-opencode/.opencode/skills/aim-communicate/SKILL.md`

## 7. Anti-patterns

- Reporting to `aim-grok` when REPLY_TO was `grok-audit`  
- Omitting FROM/REPLY_TO  
- Using project nickname (`aim-agy`) as session name when you are actually `agy_reincarnation_*`  
- AGY Escape→Enter on Grok  
- **Replying only in your own chat instead of pasting into the peer tmux session**  
- Claiming “sent” without capture-pane / script VERIFY_OK  
- Secrets in pastes  
- Force-push / destructive ops without Operator  

## 8. Incident log

1. **2026-07-12 Grok submit:** Escape→Enter left pastes unsent on Grok. Fix: Enter only.  
2. **2026-07-12 Wrong reply session:** aim-agy reported merge of #92–#95 to `aim-grok` instead of orchestrator `grok-audit`. Fix: mandatory FROM + REPLY_TO (§0).  
3. **2026-07-19 Chat-only reply:** Orchestrator answered `ayrianna-scraper` in local chat and never tmux-pasted. Fix: mandatory target-pane verification (§3d); `tmux_send.sh` exits 2 on VERIFY_FAIL.
