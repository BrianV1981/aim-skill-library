---
name: aim-google
description: Fast, script-friendly CLI for interacting with Google Workspace (Gmail, Calendar, Drive, Docs, etc.)
---

# aim-google (Google in your terminal)

> **Dependency:** This skill acts as an agentic bridge to the [BrianV1981/aim-google](https://github.com/BrianV1981/aim-google) CLI. The CLI must be installed on the host system (or within WSL) for this skill to function.

`aim-google` is a powerful, script-friendly CLI tool that provides direct access to the Operator's Google Cloud services. 

As a Windows Antigravity agent, you must know that this tool is installed **inside the WSL (Ubuntu) environment**. You cannot run it natively in PowerShell.

## Core Directives for Agents

1. **WSL Execution & Authentication:** The CLI requires a secure keyring password to unlock the OAuth tokens. **Do not ask the user for this password.** It is stored in the WSL environment. You must dynamically extract it and inject it into your WSL execution string like this:
   ```bash
   # 1. Extract the password dynamically
   PASSWORD=$(wsl bash -c "grep 'AIM_GOOGLE_KEYRING_PASSWORD' ~/.bashrc | cut -d'\"' -f2")
   
   # 2. Run the command inside WSL
   wsl bash -c "AIM_GOOGLE_KEYRING_PASSWORD='$PASSWORD' ~/go/bin/aim-google --no-input --json <service> <action>"
   ```
2. **JSON Output is Mandatory:** When executing commands to read data, you MUST use the `--json` global flag. This ensures the output is machine-readable and easily parseable by you.
3. **Exploration over Hallucination:** `aim-google` has a massive surface area. Do not guess command syntax. Use `aim-google --help` to discover available services (e.g., `gmail`, `calendar`, `drive`).
4. **No Interactive Prompts:** If you are running a destructive or complex command in the background, append `--force` or `--no-input` to prevent the CLI from hanging on a `y/n` prompt.

## Common Examples

**Checking Email (Gmail):**
```bash
wsl bash -c "AIM_GOOGLE_KEYRING_PASSWORD='\$PASSWORD' ~/go/bin/aim-google --no-input --json gmail search 'is:unread' --max 10"
```

## Troubleshooting
If a command fails with an `invalid_grant` error, it means the Google OAuth token has expired. You must instruct the user to run the authentication command manually in their WSL terminal so they can click the browser link:
`AIM_GOOGLE_KEYRING_PASSWORD="<password>" ~/go/bin/aim-google auth add brianv1981@gmail.com`
