---
name: aim-wiki
description: >
  Use the aim-grok persistent memory wiki. Search, process ingest, or bootstrap.
  Slash: /aim-wiki. Triggers: wiki, memory-wiki, project lore.
---

# aim-wiki (aim-grok)

```bash
cd /path/to/your/vessel   # or your clone path
./aim wiki search "<query>"
./aim wiki process          # compile _ingest/ → pages/ (deterministic)
./aim wiki bootstrap        # seed docs + session history into wiki
```

## Workflow
1. Drop notes into `aim-agy_os/memory-wiki/_ingest/`
2. Run `./aim wiki process`
3. Read `aim-agy_os/memory-wiki/index.md` and `pages/`
4. After `./aim pulse`, summarizer can feed the wiki deterministically

Agent mode (optional): `AIM_WIKI_MODE=agent AIM_WIKI_AGENT=grok ./aim wiki process`
