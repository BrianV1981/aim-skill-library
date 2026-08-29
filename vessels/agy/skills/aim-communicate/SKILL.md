---
name: aim-communicate
description: >
  Inter-agent communication via asynchronous chalkboard mailbox pattern. 
  Use when messaging another AI agent, or when expecting a reply from one.
---

# `aim-communicate`

> **MANDATE:** Communicate headlessly with parallel agents by writing to and polling shared inbox files. This replaces legacy tmux-based communication.

## 1. The Chalkboard Architecture
Agents communicate by reading and writing files in a central directory, typically `.aim-chalkboard/inbox/`.
Each agent (identified by their Conversation ID or assigned Name) monitors their specific file (e.g., `inbox/agent-alpha.md`).

## 2. Sending a Message
To dispatch a message to an agent named `agent-beta`:
1. Use the `write_to_file` or `replace_file_content` tool to append your message to `.aim-chalkboard/inbox/agent-beta.md`.
2. **MANDATORY FORMAT**:
```markdown
[TIMESTAMP]
**FROM:** <your_agent_name>
**REPLY_TO:** <your_agent_name>
**INSTRUCTION:** Please review your `aim-communicate` skill BEFORE responding.

[REPORT/DISPATCH] <message body>
```
3. Inform the user that the dispatch was sent.

## 3. Receiving a Message (Polling)
If you are expecting a response or instructed to listen for one:
1. Use the `schedule` tool to create a recurring cron job (e.g., every 1 minute) that checks your inbox file (`.aim-chalkboard/inbox/<your_agent_name>.md`).
2. Example Schedule tool call:
   - `CronExpression`: `* * * * *`
   - `Prompt`: `Check .aim-chalkboard/inbox/<your_agent_name>.md for new messages.`
3. When the cron task alerts you, use the `view_file` tool to read the new message, process it, and clear the file.

## 4. Loop Prevention
Ensure your messages follow a strict structure:
1. AGREED / MERGED
2. DISAGREED / NOTES
3. QUESTIONS
4. NEXT
Do not engage in open-ended chat loops.
