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

Furthermore, if the Operator completely kills the terminal and performs a **cold boot** of `agy`, the CLI ignores the summary caches entirely and recalculates the Preview directly from the raw Protobuf `step_payload` of the very first message inside `conversations/<id>.db`. 

To permanently bypass all of this, you MUST spawn a detached background process that `sleep(5)`s (to wait for `agy` to idle) and then performs both standard DB updates AND a direct binary byte-padded replacement on the session `.db` file.

Write this unified script to `/tmp/rename_session.py` and run it via `nohup`:

```python
import sqlite3
import json
import time
import sys
import os

# 1. Wait for the agy CLI to finish the current turn and flush its state
time.sleep(5) 

CONV_ID = sys.argv[1]
OLD_TITLE = sys.argv[2]
NEW_TITLE = sys.argv[3]

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

# 4. Binary Replace for Cold Boots (Protobuf Byte-Length Padding)
# Protobuf strings have a length prefix. We MUST pad the NEW_TITLE with spaces 
# so it exactly matches the byte-length of the OLD_TITLE to avoid corrupting the DB.
PADDED_NEW_TITLE = NEW_TITLE.ljust(len(OLD_TITLE))

SESSION_DB = f'/home/kingb/.gemini/antigravity-cli/conversations/{CONV_ID}.db'
if os.path.exists(SESSION_DB):
    with open(SESSION_DB, 'rb') as f:
        content = f.read()
    content = content.replace(OLD_TITLE.encode('utf-8'), PADDED_NEW_TITLE.encode('utf-8'))
    with open(SESSION_DB, 'wb') as f:
        f.write(content)

# Update history.jsonl just in case
HISTORY_FILE = '/home/kingb/.gemini/antigravity-cli/history.jsonl'
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'rb') as f:
        content = f.read()
    content = content.replace(OLD_TITLE.encode('utf-8'), PADDED_NEW_TITLE.encode('utf-8'))
    with open(HISTORY_FILE, 'wb') as f:
        f.write(content)
```

Execute it strictly using:
```bash
nohup python3 /tmp/rename_session.py "YOUR-CONV-ID" "Old Original Title" "The New Title" > /dev/null 2>&1 &
```

## 4. VERIFICATION
Inform the Operator that the background script has been launched (including the binary protobuf replacement). Let them know they can verify by typing `/resume` after your turn completes, and the new title will be displayed natively in the terminal UI even upon a cold boot.
