---
name: aim-rename-session
description: Protocol for renaming the active Antigravity CLI (agy) session title from within the agent loop using SQLite manipulation.
---

# `aim-rename-session`

> **MANDATE:** You are an autonomous agent operating within the Antigravity CLI (`agy`) harness. The Operator has requested to change the display name/title of your current session. Because `agy` currently lacks a native `/rename` slash command, you must manually manipulate the OS memory stack to fulfill the request.

## 1. THE PROBLEM
When the Operator executes `/resume` in the Antigravity CLI, it lists all recent sessions by their Title (or a fallback Preview). Since agents cannot directly command the CLI host process to rename the active session, you must bypass the CLI and update the database where the session metadata is stored.

## 2. THE DATABASES
The Antigravity OS stores session metadata in two specific locations:
1. **The SQLite Master Registry:** `~/.gemini/antigravity-cli/conversation_summaries.db`
2. **The JSON Cache (Preview Display):** `~/.gemini/antigravity-cli/cache/conversation_metadata.json`

## 3. THE EXECUTION PROTOCOL (THE BACKGROUND HACK)
**CRITICAL:** Because you are actively running inside the `agy` loop, the CLI host process will flush its in-memory state to the SQLite DB and JSON cache the exact microsecond your turn ends. If you manually run a Python script to update the DB during your turn, it will be instantly overwritten by the CLI flushing its own (stale) memory.

To bypass this, you MUST spawn a detached background process that `sleep(5)`s. This gives your turn time to finish and the `agy` process time to go idle. Once idle, your background script will surgically update the database behind `agy`'s back.

Write this unified script to `/tmp/rename_session.py` and run it via `nohup`:

```python
import sqlite3
import json
import time
import sys

# 1. Wait for the agy CLI to finish the current turn and flush its state
time.sleep(5) 

CONV_ID = sys.argv[1]
NEW_TITLE = sys.argv[2]

# 2. Update SQLite
conn = sqlite3.connect('/home/kingb/.gemini/antigravity-cli/conversation_summaries.db')
conn.execute(f'UPDATE conversation_summaries SET title="{NEW_TITLE}", preview="{NEW_TITLE}" WHERE conversation_id="{CONV_ID}"')
conn.commit()
conn.close()

# 3. Update JSON cache
CACHE_FILE = '/home/kingb/.gemini/antigravity-cli/cache/conversation_metadata.json'
try:
    with open(CACHE_FILE, 'r') as f:
        data = json.load(f)

    if 'conversations' in data and CONV_ID in data['conversations']:
        data['conversations'][CONV_ID]['summary']['Title'] = NEW_TITLE
        data['conversations'][CONV_ID]['summary']['Preview'] = NEW_TITLE
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
except Exception:
    pass
```

Execute it strictly using:
```bash
nohup python3 /tmp/rename_session.py "YOUR-CONV-ID" "The New Title" > /dev/null 2>&1 &
```

## 4. VERIFICATION
Inform the Operator that the background script has been launched. Let them know they can verify by typing `/resume` after your turn completes, and the new title will be displayed natively in the terminal UI.
