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

## 3. THE EXECUTION PROTOCOL
To successfully change your session title, you must execute the following two steps sequentially:

### Step 1: Update the SQLite Database
Use python to connect to `conversation_summaries.db` and execute an `UPDATE` statement targeting your specific Conversation ID (which you can find in your system prompt context).

```python
import sqlite3

# Your specific Conversation ID from your context
CONV_ID = "YOUR-CONVERSATION-ID-HERE"
NEW_TITLE = "The New Session Title"

conn = sqlite3.connect('/home/kingb/.gemini/antigravity-cli/conversation_summaries.db')
conn.execute(f'UPDATE conversation_summaries SET title="{NEW_TITLE}" WHERE conversation_id="{CONV_ID}"')
conn.commit()
conn.close()
```

### Step 2: Update the JSON Cache
To ensure the change reflects immediately in the CLI UI without a cache refresh, you must also patch the metadata JSON file. Update both the `Title` and `Preview` fields for your session ID.

```python
import json

CACHE_FILE = '/home/kingb/.gemini/antigravity-cli/cache/conversation_metadata.json'
CONV_ID = "YOUR-CONVERSATION-ID-HERE"
NEW_TITLE = "The New Session Title"

with open(CACHE_FILE, 'r') as f:
    data = json.load(f)

if 'conversations' in data and CONV_ID in data['conversations']:
    data['conversations'][CONV_ID]['summary']['Title'] = NEW_TITLE
    data['conversations'][CONV_ID]['summary']['Preview'] = NEW_TITLE
    
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
```

## 4. VERIFICATION
Once both scripts have executed successfully, inform the Operator that the session title has been permanently changed. When they exit and type `/resume`, the new title will be displayed natively in the terminal UI.
