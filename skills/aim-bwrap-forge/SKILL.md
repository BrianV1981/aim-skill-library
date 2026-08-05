---
name: aim-bwrap-forge
description: Dynamically spin up isolated bwrap sandbox co-agents.
---

# aim-bwrap-forge

## Overview
This skill grants you the ability to dynamically spawn a `bwrap`-isolated sandbox and dispatch a co-agent into it. This is used when you need to execute untrusted code, isolate a specific task to prevent contamination of the global OS, or handle strict multi-tenant workloads.

## Requirements
- `bwrap` (bubblewrap) must be installed on the host system.
- The `aim-coagents` library should be available to orchestrate the handoff.

## Execution
1. Create a secure directory for the new tenant/sandbox: `mkdir -p ~/.aim/sandboxes/dynamic_sandbox_123`
2. Initialize the bwrap environment pointing to the standard JOSHUA install scripts but confined to the sandbox directory.
3. Spawn a co-agent into the sandbox using `tmux new-session -d -s bwrap_agent "bwrap --unshare-all ... /path/to/aim-joshua/aim"`
4. Communicate with the isolated agent via standard `aim-communicate` sockets or by monitoring its tmux output.

## Tear-down
When the task is complete, the sandboxed agent will commit its final memory state to its local `.git` ledger. You can then retrieve the outputs and safely `rm -rf` the sandbox directory if it is no longer needed.
