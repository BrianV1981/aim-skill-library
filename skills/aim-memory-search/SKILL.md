---
name: aim-memory-search
description: >
  Search A.I.M. Engram / hybrid memory via the vessel ./aim CLI. Use for project
  history and factual recall. Slash: /aim-memory-search.
---

# aim-memory-search

From the **vessel project root** (where `./aim` works):

```bash
./aim map
./aim search "<query>"
./aim search "<query>" --top-k 10
./aim search "<snippet>" --full
./aim wiki search "<query>"   # if wiki is enabled on this vessel
```

## Rules

1. Prefer `./aim map` before open-ended exploration.  
2. If nothing is found, **say so** — do not invent memory hits.  
3. Cite query + result source when using facts from search.
