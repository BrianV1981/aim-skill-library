---
name: aim-sessions
description: >
  Project-scoped session notebook (NotebookLM for sessions): list, search, and
  synthesize all handed-off / blackbox-sealed sessions exclusively within the
  current project without global /resume clutter or 500-session eviction loss.
  Slash: /aim-sessions.
---

# `aim-sessions` — Project-Scoped Session Notebook

> **MANDATE:** Provide a NotebookLM-style review and search experience strictly scoped to the current project's handed-off sessions (`<project>/archive/.raw_jsonl_blackbox/` and `<project>/joshua_os/archive/history.db`). Never pollute with other projects or ephemeral 2-step pipeline runs.

## 1. Core Capabilities

1. **List All Archived Project Sessions (Unlimited Retention):**
   ```bash
   ./aim sessions
   ```
   - Automatically syncs any `.enc` transcripts in `<project>/archive/.raw_jsonl_blackbox/` into `<project>/joshua_os/archive/history/` (clean Markdown Flight Records) and `<project>/joshua_os/archive/history.db` (SQLite FTS5 index).
   - Displays Date, Status (`LIVE+VAULT` if still in `~/.gemini/antigravity-cli/conversations/` vs `VAULTED` if preserved after `agy`'s 500-session global rotation), Turn Count, Full Session UUID, and Title/Summary.

2. **Full-Text Search Across Project Sessions (FTS5):**
   ```bash
   ./aim search-sessions "<keyword or phrase>"
   ```
   - Searches every archived session transcript in the current project and returns matching Session UUIDs, timestamps, and context snippets.

3. **NotebookLM-Style Synthesized Recall (Q&A Over Past Sessions):**
   ```bash
   ./aim recall "<question about past project sessions>"
   ```
   - Retrieves the top matching session transcripts from `joshua_os/archive/history.db` and synthesizes a direct, grounded answer.

4. **Read a Full Session Flight Record:**
   - Every archived session is stored as a clean, readable Markdown file at:
     `<project>/joshua_os/archive/history/<YYYY-MM-DD>_<session_id>.md`
   - To resume a `LIVE+VAULT` session in the terminal:
     `agy --conversation <session_id>`

## 2. Agent Execution Protocol

When the Operator invokes `/aim-sessions` (or asks to review/search past sessions in this project):
1. Run `./aim sessions` from the project root and present the project session table clearly.
2. If the Operator asks about a specific topic, decision, or past conversation, run `./aim search-sessions "<query>"` and/or inspect the matching `<project>/joshua_os/archive/history/*_<session_id>.md` file to answer with exact session citations and clickable `file://` links.
