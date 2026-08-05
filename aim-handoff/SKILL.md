---
name: aim-handoff
description: Standardized instructions for structuring Ephemeral Context Handoffs and executing the Tmux Baton Pass.
---

# 🤖 AIM-HANDOFF SKILL

> **MANDATE:** This skill dictates exactly how an active agent must package its working memory into a standardized document, and optionally how to use Tmux to physically pass that document into a fresh agent session.

## 1. CORE PHILOSOPHY
Before you initiate a handoff, understand the workflow:
- **Persistent Memory (`aim-memory-wiki`):** Long-term project lore and architectural decisions. Do this FIRST.
- **Ephemeral Memory (`aim-handoff`):** Tactical, localized context (What file? What bug? What's next?). This is the "Baton" passed in a relay race. 

## 2. THE HANDOFF TEMPLATE
When instructed to prepare a handoff, you MUST generate or update a structured markdown file (e.g., `HANDOFF.md`).

### CRITICAL RULES:
1. **UPDATE, DO NOT DECAPITATE:** If a handoff document exists, **update** it. Preserve overarching context.
2. **CONSOLIDATE THE PAST:** When moving items to the "Completed Work" section, **clean and consolidate**. Keep past accomplishments brief.
3. **DETAIL THE FUTURE:** You must be extremely explicit about what **needs to be done** next. Provide exact file paths, bugs, and requirements for the incoming agent.
4. **NO FORCED ARCHITECTURE:** Do not assume the repository has a `docs/` folder or a roadmap unless explicitly provided by the Operator.

**The Gold-Standard Template:**

```markdown
# [Project Name] — Engineering Handoff

> **Updated:** [Timestamp]
> **Updated by:** [Your Session ID]
> **Priority Mission:** [High level goal]
> **Operator:** [Operator Name]

---

## 0. COMPLETED WORK (DO NOT REVISIT)
| Session | Work | Status |
|---------|------|--------|
| [ID] | [Description of work completed] | ✅ RESOLVED |
*(Keep this section clean, brief, and consolidated.)*

---

## 1. PROJECT IDENTITY
*(Brief 1-2 sentence description of what the project actually does, plus environments and key paths.)*

---

## 2. YOUR MISSION: [MISSION TITLE]
*(The overarching goal of the upcoming session.)*

### Execution Queue (in order)
*(For each task in the queue, explain IN DETAIL what needs to be done:)*
#### 1️⃣ Issue / Task
**Problem:** [Exact and detailed description of the bug or feature]
**Fix:** [Exact and detailed instructions on how to solve it]
**Key files:** [Absolute paths to the specific files required]

---

## 3. THE CRITICAL TRAPS & WARNINGS
> **⚠️ EPISTEMIC WARNINGS**
*(List the most dangerous assumptions an agent might make.)*

---

## 4. KEY PATHS
*(Provide a directory map of the 5-10 absolute file paths currently in use.)*

---

## 5. OPERATOR PREFERENCES
*(List any specific boundaries the Operator has established.)*

---

## 6. IMMEDIATE NEXT STEPS
1. Start with [Task]
2. [Imperative command for the exact next action.]
```

## 3. THE TMUX BATON PASS (OPTIONAL)
If the Operator instructs you to spin up the next agent yourself, you will use `tmux` to spawn a new session, inject the handoff document directly into its prompt, and execute it. 

**Execution Steps (using the shell):**
1. **Get Current Session Name:** Run `CURRENT_SESSION=$(tmux display-message -p '#{session_name}')`
2. **Generate New Session Name:** Append a 6-character random alphanumeric string to the current session name (e.g., if current is `aim-agy`, new is `aim-agy-6H7g0z`).
3. **Spin Up Vessel:** Spin up a new detached tmux session using the new name, running the appropriate CLI command.
   - `tmux new-session -d -s $NEW_SESSION_NAME "agy"` (or `grok`, `opencode`, etc. depending on environment).
4. **Inject Prompt:** Use the tmux clipboard buffer system to inject the handoff document. Do not use raw `send-keys` for long text.
   - `tmux set-buffer "$(cat HANDOFF.md)"`
   - `tmux paste-buffer -p -t $NEW_SESSION_NAME`
5. **Execute Prompt:** Send the execution keys.
   - For AGY targets, you MUST send `Escape` and `Enter` as two separate commands:
     `tmux send-keys -t $NEW_SESSION_NAME Escape`
     `tmux send-keys -t $NEW_SESSION_NAME Enter`
   - For Grok targets, send only `Enter`:
     `tmux send-keys -t $NEW_SESSION_NAME Enter`
6. **Report & Terminate:** Output a final message to the Operator. You MUST provide the exact command they need to copy/paste to attach to the new session (e.g., `tmux attach -t aim-agy-6H7g0z`). End your message with a witty or funny goodbye (like "Peace out", "My battery is low and it's getting dark", etc.) and terminate your tools.
