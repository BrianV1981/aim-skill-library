---
name: aim-wiki
description: >
  Persistent memory wiki on A.I.M. vessels: search, process ingest, bootstrap.
  Slash: /aim-wiki.
---

# aim-wiki

From the vessel project root:

```bash
./aim wiki search "<query>"
./aim wiki process      # compile ingest → pages
./aim wiki bootstrap    # seed docs / history when supported
```

## Typical workflow

1. Drop notes into the wiki ingest directory (often under `aim-agy_os/memory-wiki/_ingest/` — confirm on this vessel).  
2. Run `./aim wiki process`.  
3. Read `index.md` and `pages/` under the wiki root.  

Optional agent mode (if supported):

```bash
AIM_WIKI_MODE=agent ./aim wiki process
```

If a command is missing on this vessel, say so — do not invent wiki state.
