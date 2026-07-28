---
name: aim-memory-wiki
description: Interactive active-memory ingestion skill for maintaining a persistent, compounding LLM knowledge base (the Memory Wiki).
---

# `aim-memory-wiki`

> **MANDATE:** You are the active agent in a session, and the user has activated the `aim-memory-wiki` skill. Your objective is to process the recent session context, extract key discoveries, code decisions, and milestones, and incrementally update the persistent knowledge base located in `memory-wiki/`.

## 1. THE CORE PHILOSOPHY
The wiki is a **persistent, compounding artifact** — a structured, interlinked collection of markdown files. It sits between the user and raw data. You do not just index data for retrieval; you read it, extract key information, and *integrate it into the existing wiki* (updating entity pages, revising topic summaries, noting where new data contradicts old claims). 
**The wiki keeps getting richer with every source you add and every session you summarize.**

## 2. BOOTSTRAPPING (IF EMPTY)
If `memory-wiki/` does not exist or is completely empty (no `index.md` or `log.md`), you must scaffold it:
1. Create `memory-wiki/index.md` with a `# Project Wiki Index` header and basic placeholder sections (e.g., `## Core Concepts`, `## Architecture`).
2. Create `memory-wiki/log.md` with a `# Memory Log` header to track chronological ingestion events.
3. Create the `memory-wiki/pages/` directory to house individual detailed markdown files.

## 3. THE THREE LAYERS
1. **Raw Sources:** External files, chat history, or code that you read but do not modify.
2. **The Wiki:** A directory of LLM-generated markdown files (`memory-wiki/`). You own this layer entirely. You create pages, update them, maintain cross-references, and keep everything consistent.
3. **The Schema:** Rules and configurations (like `AGENTS.md`) that guide how you act. 

## 4. YOUR OPERATIONS WHEN TRIGGERED
When the user invokes this skill, you must perform an **Ingest** operation synchronously:

1. **Synthesize Context:** Review what was accomplished, decided, or learned in the recent session. Do NOT copy raw transcripts. Extract the tactical takeaways, architectural changes, or deep insights.
2. **Update the Index (`memory-wiki/index.md`):** This is the content-oriented catalog. If you create a new page or identify a new core concept, add a link and a one-line summary to `index.md`. Organize it by category (entities, concepts, etc.).
3. **Update the Log (`memory-wiki/log.md`):** This is a chronological, append-only record of operations. You MUST append an entry detailing what you ingested.
   - Format: `## [YYYY-MM-DD] ingest | <Title of the update>`
   - Include a brief bulleted summary of what pages were touched.
4. **Update/Create Content Pages:** 
   - Open existing relevant pages (e.g., `memory-wiki/pages/architecture.md`) and integrate the new facts. 
   - If a topic is new and complex, create a new file (e.g., `memory-wiki/pages/new_concept.md`) and interlink it with existing pages using standard Markdown links (`[Concept](concept.md)`).
   - Resolve any contradictory stale claims from older versions.

## 5. LINTING AND CROSS-REFERENCING
Always ensure:
- No orphaned pages exist. If you make a new page, link to it from `index.md` or another relevant page.
- Links are valid relative markdown links.
- Your summaries are precise and dense with signal, free of conversational filler. 

## 6. EXECUTION
Proceed by explicitly generating your proposed memory updates for the user to review, or immediately begin writing to the `memory-wiki/` directory depending on the user's prompt. 
Use your file system editing tools (`replace_file_content`, `write_to_file`, `multi_replace_file_content`) to methodically apply the changes.
