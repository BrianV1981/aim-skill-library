---
name: aim-coagents
description: >
  AGY Override: Spawning and instructing Linux-based CLI coagents via WSL tmux
  and coordinating replies via A-Mail (`aim-mail` / `amail`).
---

# `aim-coagents` (AGY Windows 11 Override)

> **MANDATE:** You are the Windows 11 Orchestrator. When delegating a task to a specialized Linux coagent (Grok, OpenCode, Codex), spawn it in an isolated workspace via WSL `tmux` and route dispatches and completion reports exclusively through **A-Mail** (`amail` / `aim-mail`).

## 1. Directory Sandboxing
Agents must **never** be spawned arbitrarily or in the root `C:\`. Isolate them in dedicated project workspaces based on their role:

`%USERPROFILE%\aim-agents\<workspace-name>\` (or `$HOME/aim-agents/<workspace-name>/` inside WSL2)

Before spawning an agent:
1. Ensure the target directory exists.
2. Initialize it via `init-workspace.ps1` if required, or create the directory if it is a clean sandbox.

## 2. Spawning the Coagent via WSL & Registering in A-Mail
Bridge Windows and WSL by launching the coagent inside a detached `tmux` session and registering its logical ID in the shared A-Mail (`AIM_MAILBOX_DIR`) address book:

```powershell
wsl tmux new-session -d -s <session-name> "cd ~/aim-agents/<workspace-name> && <cli_command>"
amail register <session-name> --driver tmux --tmux-session <session-name> --cwd "~/aim-agents/<workspace-name>"
```

## 3. A-Mail Reply Instruction (CRITICAL)
Instruct spawned coagents to return their bounded (`max_hops=1`) completion report to your logical orchestrator ID via A-Mail (`amail` / `aim-mail`) rather than writing ad-hoc scratchpad files:

```powershell
$sessionName = "grok-worker-1"
$wslPath = "~/aim-agents/frontend-refactor"
wsl tmux new-session -d -s $sessionName "cd $wslPath && grok"
amail register $sessionName --driver tmux --tmux-session $sessionName --cwd $wslPath

# Dispatch via shared Maildir (or run `wsl amail send ... --wake` to trigger the WSL tmux driver):
wsl amail send `
  --from joshua-win11 `
  --to $sessionName `
  --reply-to joshua-win11 `
  --subject "Frontend Refactor Audit" `
  --body "Analyze React components for duplicate logic and reply via amail ending with DO NOT reply." `
  --operator-approved `
  --wake
```

## 4. Zero-Token Waiting & Inbox Verification
Once dispatched, use `amail wait joshua-win11 --thread-id <thread_id> --timeout 120 --json` (or allow the live Antigravity Desktop Sidecar `watch` loop to deliver the coagent's reply automatically to your session).
