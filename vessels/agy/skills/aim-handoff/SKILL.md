---
name: aim-handoff
description: >
  Ephemeral context handoff: structure Engineering Handoff docs to the gold-standard
  numbered template (HANDOFF style), update in place, optional Tmux baton pass
  to a fresh vessel session.
---

# `aim-handoff`

> **⚠️ CRITICAL PREREQUISITE:** Have you run `/aim-memory-wiki`? Before initiating a handoff, always ensure the latest architectural decisions and context have been synthesized into the memory wiki first.

> **MANDATE:** Package tactical working memory into a standardized Engineering Handoff
> document, and optionally pass that baton into a fresh agent via tmux.

## Relationship to other skills

| Skill | Role |
|-------|------|
| **`aim-memory-wiki`** | **Persistent** project lore — do this **first** (or ensure wiki is current) |
| **`aim-handoff`** (this) | **Ephemeral** baton — mission, traps, exact next steps for the *next* session |
| **`aim-precompact-handoff`** | **Safeguard** — Grok context-window guard; forces a handoff *before* auto-compact destroys context |

Do not confuse precompact (when/why to write under token pressure) with this skill
(what the handoff document must look like).

---

## 1. Core philosophy

1. **UPDATE, do not decapitate.** If `HANDOFF.md` / `HANDOFF.md` exists, **update** it. Preserve overarching context; consolidate completed work; expand future detail.
2. **Wiki first.** Long-term architecture and decisions belong in `memory-wiki/` via `aim-memory-wiki`. The handoff is the relay baton, not a second wiki.
3. **No guesses.** Unknown → write `UNKNOWN`. Proven → path, SHA, issue #, command, count.
4. **No forced architecture.** Do not invent `docs/` trees or roadmaps the Operator did not provide.

---

## 2. Gold-standard template (numbered sections)

Canonical shape: gold-standard Engineering Handoff with numbered sections **0–9**
(LeadDeed-style `HANDOFF.md` when that project uses it; otherwise `HANDOFF.md`).

When instructed to prepare a handoff, generate or **update** a structured markdown file
(e.g. `HANDOFF.md` or project-specific `HANDOFF.md`) with **all** of the following
sections. Mission-specific titles may specialize (e.g. “MODULE-BY-MODULE ANALYSIS FOR #173”)
but the **numbers and roles must remain**:

```markdown
# [Project Name] — Engineering Handoff

> **Updated:** [Timestamp]
> **Updated by:** [Session / vessel id]
> **Priority Mission:** [One-line goal]
> **Operator:** [Name / email]

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
The gold standard is **sections 0–9** (ten numbered blocks), matching `HANDOFF.md`.
Older drafts used a shorter 0–6 skeleton; **prefer 0–9** for full coherence with LeadDeed handoffs.
Do not drop §3–§4 or §7 when the mission is non-trivial.

---

## 3. Update rules (anti-bloat)

1. Move finished items into **§0** with one-line status; strip stale “still open” prose.
2. Rewrite **§2 / §9** for the *next* agent — more detail on the future than on the past.
3. Prefer editing the existing handoff path the project already uses.
4. After structural facts change, also run **`aim-memory-wiki`** so the wiki stays the long-term store.

---

## 4. Tmux baton pass (optional)

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

## 5. Slash / triggers

Triggers: handoff, baton, reincarnation doc, `HANDOFF.md`, `HANDOFF`, session transfer.

Default filename preference: use the project’s existing handoff file if present; else `HANDOFF.md` at vessel/project root.
