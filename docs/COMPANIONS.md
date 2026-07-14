# Companion packages (not vendored here)

**aim-skill-library** holds **skill playbooks** that fit in a folder. Heavy tools stay in their own repos — **own your stack**, don’t fork the world into one monorepo.

| Companion | What | Install hint |
|-----------|------|----------------|
| **[aim-browser](https://github.com/BrianV1981/aim-browser)** | Headed Chromium CDP + **skill suite** (google-ai, page-fetch, …) | `git clone … && cd aim-browser && npm i && npm run install-skills -- <vessel-skills-dir> --mode symlink` |
| **[aim-google](https://github.com/BrianV1981/aim-google)** | Google Workspace CLI skill | Clone; link `agent-skill/aim-google` into vessel skills |
| **[aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)** | Session → markdown forensics | Clone; follow that repo’s skill install |
| **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** | Co-agent DNA bank | Clone; equip when spawning peers |

Library install (`scripts/install.sh`) never copies these. Link them deliberately after clone.
