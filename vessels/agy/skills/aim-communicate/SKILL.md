---
name: aim-communicate
description: >
  AGY Override: Inter-agent communication via the Shared Scratchpad (Path 2a). 
  Use when reading responses from Linux tmux coagents or writing messages to them via file synchronization. 
  Replaces legacy tmux send-keys protocols.
---

# `aim-communicate` (AGY Windows 11 Override)

> **MANDATE:** You are the Windows 11 Orchestrator. When communicating with Linux-based CLI coagents (Grok, OpenCode, Codex) running in WSL/tmux, you MUST use the file system as your API bridge. 

## 1. The Shared Scratchpad (Path 2a)
Windows and WSL share the exact same local file system. Rather than injecting keystrokes into a Linux terminal, you will read and write to a dedicated `aim-communicate.md` file located in the root of the coagent's workspace.

- **Windows Path:** `C:\Users\kingb\aim-agents\<workspace-name>\aim-communicate.md`
- **WSL Equivalent:** `/mnt/c/Users/kingb/aim-agents/<workspace-name>/aim-communicate.md`

## 2. Dispatching a Message
When you need to send follow-up instructions to a running coagent:
1. Use the `write_to_file` or `replace_file_content` tool to append your message to the coagent's `aim-communicate.md` file.
2. Structure your dispatch cleanly so the coagent can parse it.
3. *Note: If the agent is idle, you may need to ping their terminal using WSL to force them to read the file, but prefer instructing them to poll the file automatically upon spawn (see \im-coagents\).*

## 3. Receiving a Message (Polling)
If you are expecting a response from a coagent:
1. Do NOT pause your execution or loop continuously. 
2. Use the `schedule` tool to create a recurring background cron job (e.g., `* * * * *` for every minute) to check the target workspace's `aim-communicate.md` file.
3. Example Schedule:
   - `CronExpression`: `* * * * *`
   - `Prompt`: `Check C:\Users\kingb\aim-agents\<workspace-name>\aim-communicate.md for the coagent's response.`
4. When the cron alerts you, use `view_file` to read the answer. 

## 4. Telemetry and Health Checks (Path 2b)
You may occasionally need to check if a Linux coagent is stuck, crashed, or waiting for a user prompt. 
Use your `run_command` tool to securely scrape their terminal buffer without interfering with their input:

`powershell
wsl tmux capture-pane -t <session-name> -p -J -S -40
`

**WARNING:** Never use terminal scraping to extract the coagent's final data/report. Terminal buffers are brittle, paginated, and polluted with ANSI codes. Rely strictly on `aim-communicate.md` for data handoffs.
