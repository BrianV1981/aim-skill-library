---
name: aim-handoff
description: >
  Ephemeral context handoff: structure Engineering Handoff docs to the gold-standard
  numbered template (LD-CLAUDE_HANDOFF style), update in place, optional Tmux baton pass
  to a fresh vessel session.
---

# `aim-handoff`

> **MANDATE:** Execute a one-command end-of-session closeout: automatically verify and ingest any unlogged session work into `memory-wiki/` (Step 1), surgically update the standardized Engineering Handoff document (`HANDOFF.md`), commit & push both directly to `origin/main` with zero confirmation prompts, and optionally pass the baton into a fresh agent via tmux.

## Relationship to other skills

| Skill | Role |
|-------|------|
| **`aim-memory-wiki`** | **Mid-session "Save Game"** — fast (~15s) autonomous checkpoint into `memory-wiki/` without ending the session |
| **`aim-handoff`** (this) | **End-of-session closeout** — auto-includes any `memory-wiki/` delta + updates `HANDOFF.md` + pushes both to `origin/main` |
| **`aim-precompact-handoff`** | **Safeguard** — Grok context-window guard; forces a handoff *before* auto-compact destroys context |

Do not confuse precompact (when/why to write under token pressure) with this skill
(what the handoff document must look like).

---

## 0. Step 1 — Idempotent Auto-Wiki Delta Check (MANDATORY)

Before touching `HANDOFF.md`, you MUST inspect `memory-wiki/log.md`:
1. **If work or architectural decisions occurred since the last `/aim-memory-wiki`** (or `/aim-memory-wiki` was not run during this session): automatically synthesize the session's discoveries, decisions, and milestones into `memory-wiki/index.md`, `memory-wiki/log.md`, and `memory-wiki/pages/*.md` (and run `./aim index` if LanceDB is active) as Step 1 of this handoff.
2. **If `memory-wiki/` is already current for the session:** skip straight to updating `HANDOFF.md`.

---

## 1. Core philosophy

1. **UPDATE, do not decapitate.** If `HANDOFF.md` / `LD-CLAUDE_HANDOFF.md` exists, **update** it. Preserve overarching context; consolidate completed work; expand future detail.
2. **Wiki first.** Long-term architecture and decisions belong in `memory-wiki/` via `aim-memory-wiki`. The handoff is the relay baton, not a second wiki.
3. **No guesses.** Unknown → write `UNKNOWN`. Proven → path, SHA, issue #, command, count.
4. **No forced architecture.** Do not invent `docs/` trees or roadmaps the Operator did not provide.

---

## 2. Gold-standard template (numbered sections)

Canonical shape: gold-standard Engineering Handoff with numbered sections **0–9**
(LeadDeed-style `LD-CLAUDE_HANDOFF.md` when that project uses it; otherwise `HANDOFF.md`).

When instructed to prepare a handoff, generate or **update** a structured markdown file
(e.g. `HANDOFF.md` or project-specific `LD-CLAUDE_HANDOFF.md`) with **all** of the following
sections. Mission-specific titles may specialize (e.g. “MODULE-BY-MODULE ANALYSIS FOR #173”)
but the **numbers and roles must remain**:

```markdown
# [Project Name] — Engineering Handoff

> **Updated:** [Timestamp]
> **Updated by:** [Session / vessel id]
> **Priority Mission:** [One-line goal]
> **Operator:** Brian Vasquez (`@BrianV1981` / `brianv1981@gmail.com` — or project-specific: `bvasquez@leaddeeds.com`, `bvasquez@ayrianna.com`, `bvasquez@skorbane.com`; never invent an email)

---

## 0. COMPLETED WORK (DO NOT REVISIT)
| Session | Work | Status |
|---------|------|--------|
| [id] | [brief] | ✅ RESOLVED |

*(Keep clean and consolidated. Point to wiki/issues for deep history — do not re-audit.)*

---

## 1. PROJECT IDENTITY
*(1–3 sentences: what the system is, prod vs local, monorepo root. Bullet key envs/URLs.)*

### Your Knowledge Base
*(Absolute paths to memory-wiki index + 3–5 critical pages/docs.)*

---

## 2. YOUR MISSION: [TITLE]
*(Overarching goal for the *incoming* session.)*

### Execution Queue (in order)
#### 1️⃣ [Task]
**Problem:** …
**Fix:** …
**Key files:** [absolute paths]

---

## 3. DETAILED ANALYSIS / BREAKDOWN
*(Mission-specific depth: module-by-module, system-by-system, or risk-ordered breakdown.
Expand freely; this is where complexity lives so §2 stays scannable.)*

---

## 4. IMPLEMENTATION STRATEGY
*(Ordered approach, tiers, pass structure, tests expected. How to attack §2/§3 without thrash.)*

---

## 5. THE CRITICAL TRAPS & WARNINGS
> **⚠️ EPISTEMIC / OPERATIONAL WARNINGS**
*(Top landmines — e.g. Vercel vs local, wrong env files, destructive git habits.)*

---

## 6. KEY PATHS
*(5–15 absolute paths grouped by concern: infra, targets of the mission, config.)*

---

## 7. THE FULL PICTURE / WHAT COMES AFTER
*(Dependency graph or short roadmap after the priority mission. Parallel quick wins table OK.)*

---

## 8. OPERATOR PREFERENCES
*(Boundaries: do/don't, proof standards, multi-agent coordination, push discipline.)*

---

## 9. IMMEDIATE NEXT STEPS
1. …
2. … *(Imperative, ordered, first command the incoming agent should run.)*
```

### Section count note
The gold standard is **sections 0–9** (ten numbered blocks), matching `LD-CLAUDE_HANDOFF.md`.
Older drafts used a shorter 0–6 skeleton; **prefer 0–9** for full coherence with LeadDeed handoffs.
Do not drop §3–§4 or §7 when the mission is non-trivial.

---

## 3. Update rules (anti-bloat)

1. Move finished items into **§0** with one-line status; strip stale “still open” prose.
2. Rewrite **§2 / §9** for the *next* agent — more detail on the future than on the past.
3. Prefer editing the existing handoff path the project already uses.
4. After structural facts change, also run **`aim-memory-wiki`** so the wiki stays the long-term store.

---

## 4. Blackbox Ingestion (Mandatory Pre-Handoff)

Before executing the final Tmux baton pass or exiting, you MUST seal your current session's raw logs into the immutable blackbox vault using the Grok specific extraction hook:

1. Run: `./aim grok-blackbox --session-id <your-session-uuid>`

> **⚠️ NON-FATAL KEY WARNING:** The blackbox vault uses a headless key fallback. If it reports a missing keyring or a vault warning, DO NOT attempt to fix it or abort the handoff. It is non-fatal. Proceed with the handoff normally.

---

## 5. Tmux baton pass (optional)

Only if the Operator asks you to spawn the next agent:

1. `CURRENT_SESSION=$(tmux display-message -p '#{session_name}')`
2. New name: `${CURRENT_SESSION}-` + 6 random alphanumerics
3. `tmux new-session -d -s "$NEW" "grok"` (or `agy` / `opencode` as appropriate)
4. Load handoff into buffer and paste (not long `send-keys` novels):
   - `tmux set-buffer "$(cat /abs/path/HANDOFF.md)"`
   - `tmux paste-buffer -p -t "$NEW"`
5. Submit:
   - **Grok / OpenCode:** `tmux send-keys -t "$NEW" Enter` only
   - **AGY:** `Escape` then `Enter` (separate calls)
6. Prefer `aim-communicate` / `tmux_send.sh` when messaging an *existing* peer session.
7. Report `tmux attach -t <new>` to Operator; witty goodbye optional.

---

## 6. Slash / triggers

Triggers: handoff, baton, reincarnation doc, `HANDOFF.md`, `LD-CLAUDE_HANDOFF`, session transfer.

Default filename preference: use the project’s existing handoff file if present; else `HANDOFF.md` at vessel/project root.

---

## 7. Finalization & Direct-to-`main` Atomic Push (ZERO PROMPTS)

`memory-wiki/**` and `HANDOFF.md` are living OS memory state exempt from GitHub Issues and worktrees. After updating `memory-wiki/` (if needed) and `HANDOFF.md`, you MUST immediately execute from the repository root with **zero confirmation prompts**:

```bash
git add memory-wiki/ HANDOFF.md
git diff --cached --quiet || git commit -m "docs(handoff): update memory-wiki and HANDOFF.md for session closeout"
git pull --rebase --autostash origin main
git push origin main
```

1. **Surgical Path-Scoped Staging Only:** Never run `git add .` or `git commit -a`. Stage only `memory-wiki/` and `HANDOFF.md` (or the project's existing handoff filename).
2. **Zero Friction:** Do NOT open a GitHub Issue, do NOT spawn a worktree, and do NOT ask the Operator for permission to commit or push.
