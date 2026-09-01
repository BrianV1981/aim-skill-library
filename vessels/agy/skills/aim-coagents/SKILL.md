---
name: aim-coagents
description: >
  AGY Override: Spawning and instructing Linux-based CLI coagents via WSL tmux.
  Enforces strict directory sandboxing and injects the Path 2a bridging instruction.
---

# `aim-coagents` (AGY Windows 11 Override)

> **MANDATE:** You are the Windows 11 Orchestrator. When you need to delegate a task to a specialized Linux coagent (Grok, OpenCode, Codex), you must spawn them in a strict sandboxed directory via WSL and bind them to the Shared Scratchpad protocol.

## 1. Directory Sandboxing
Agents must **never** be spawned arbitrarily or in the root `C:\`. They must be isolated in dedicated project workspaces based on their role.

The standard hierarchy is:
`C:\Users\kingb\aim-agents\<workspace-name>\`

Before spawning an agent:
1. Ensure the target directory exists.
2. Initialize it via `init-workspace.ps1` if required, or simply create the directory if it's a blank sandbox.

## 2. Spawning the Coagent via WSL
Because you run natively in Windows, you must bridge the OS gap by utilizing the Windows Subsystem for Linux (WSL). You will spawn the coagent inside a detached `tmux` session so the Operator can attach and monitor it later if needed.

**Syntax Template:**
```powershell
wsl tmux new-session -d -s <session-name> "cd /mnt/c/Users/kingb/aim-agents/<workspace-name> && <cli_command> --task '<your-instructions>'"
```

## 3. The Path 2a Bridging Instruction (CRITICAL)
Linux CLI coagents do not have access to your native Antigravity message API. If you do not explicitly teach them how to reply, they will print their answer to their terminal buffer and you will never receive it cleanly.

You MUST append the following directive to the end of your `<your-instructions>` payload:

> **"CRITICAL: When you have finished your task, you must use your write_to_file tool to output your final report to aim-communicate.md in the root of your workspace, and then halt. Do not wait for a reply."**

**Example Execution:**
```powershell
# 1. Define the parameters
$sessionName = "grok-worker-1"
$wslPath = "/mnt/c/Users/kingb/aim-agents/frontend-refactor"
$instruction = "Analyze the React components and identify duplicate logic. CRITICAL: When you have finished your task, you must use your write_to_file tool to output your final report to aim-communicate.md in the root of your workspace, and then halt. Do not wait for a reply."

# 2. Spawn the agent
wsl tmux new-session -d -s $sessionName "cd $wslPath && aim-grok --task '$instruction'"
```

## 4. Handoff
Once spawned, do NOT wait synchronously. Utilize the `aim-communicate` skill to schedule a background cron job that polls `aim-communicate.md` for their response.
