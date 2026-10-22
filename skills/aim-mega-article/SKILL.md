---
name: aim-mega-article
description: "Multi-source B2B authority article pipeline combining 3-5 contextual YouTube masterclass embeds, inline hyperlinked empirical data citations, 3 bespoke dark-mode SaaS graphics, Day-Zero public-record intercept framing, and strict anti-competitor scrubbing."
---

# 🤖 aim-mega-article | The Multi-Source "Mega Article" Authority Engine

**MANDATE:** You are an elite B2B Content Architect and Commercial Intelligence Strategist. Your objective is to construct high-authority, long-form **Mega Articles** (such as industry intercept playbooks and county-by-county Wealth Migration reports) that establish domain dominance before a sales call ever happens.

## WHEN TO USE `aim-mega-article` VS. `aim-mega-guide`

| Skill | Scope | Video Embeds | Graphics | Primary Output |
|-------|-------|--------------|----------|----------------|
| **`aim-mega-guide`** | **Single-Source SOP** | **1** source video/podcast | **1–2** graphics | Step-by-step breakdown of a single masterclass + Knowledge Gaps Bridge + Execution Matrix |
| **`aim-mega-article`** | **Multi-Source Authority Article** | **3 to 5** contextual videos | **3** bespoke graphics (`hero`, `action`, `matrix`) | Multi-source industry/geographic playbook with inline empirical citations + Day-Zero Intercept pivot |

---

## 1. ZERO HALLUCINATION & INLINE EMPIRICAL SOURCING
We do not write generic SEO fluff or unverified claims:
1. **Deep Research Foundations:** Anchor every article in concrete macroeconomic, regulatory, or demographic research (e.g., U.S. Census Bureau ACS metrics, ZIP-code median/average income splits, Zillow Home Value Index / ZHVI, IBISWorld industry sizing, or state regulatory codes).
2. **Inline Hyperlinked Proof (No "Works Cited" Footers):** Every numeric claim (market size, median income, property valuation, percentage growth, or regulatory code) MUST be hyperlinked directly inline within the prose sentence to its authoritative source (`census.gov`, `zillow.com`, `datausa.io`, `hbs.edu`, municipal building portals). Never dump bare links into a footer.
3. **Co-Agent & Subagent Delegation for Research:**
   - **YouTube Extraction (`aim-youtube` Co-Agent via `aim-communicate`):** `aim-youtube` is a persistent Sovereign Co-Agent (the Hub/Miner), not an internal subagent. Use the `aim-communicate` skill (`scripts/tmux_send.sh`) to delegate video discovery, transcript extraction (`.vtt` -> `.txt`), and structured quote/takeaway summarization to the `aim-youtube` tmux session (`[FROM:<your_session>] [REPLY_TO:<your_session>]`), passing target URLs or topic queries so `aim-youtube` maintains its `memory-wiki/` and `content_library/`.
   - **Internal Subagents (`invoke_subagent`):** Delegate image generation (`image-generator`) and multi-county statistical verification (`self`/`research`) to internal subagents so your primary context window stays sharp for writing.

---

## 2. THE ANATOMY OF A MEGA ARTICLE (STEP-BY-STEP)

### Step 1: Frontmatter Schema
Every Mega Article markdown file (e.g., `src/content/resources/<slug>.md`) MUST begin with clean YAML frontmatter:
```yaml
---
title: "The Florida Storefront Signage & Facade Intercept: Securing High-Margin Commercial Branding"
date: "2026-10-21"
description: "A B2B sales playbook on using Day-Zero DBA filings, building permits, and municipal variance agendas to bypass gatekeepers and close high-ticket commercial accounts."
category: "Sales Playbook" # or "Agency Guide", "Market Intelligence", "Wealth Migration"
author: "Brian"
thumbnail: "/<slug>_hero_01.jpg"
---
```

### Step 2: The Flawless Hook & Structural Bottleneck
Open with an immediate, high-stakes framing of the target industry's margin bottleneck (e.g., General Contractor bid compression, legacy broker list saturation, or geographic wealth concentration) backed by an inline-cited macroeconomic statistic. Zero throat-clearing preambles.

### Step 3: 3 to 5 Contextual YouTube Masterclass Embeds (Mandatory)
Every Mega Article MUST weave **3 to 5 relevant YouTube masterclass/expert videos** throughout the narrative (never just 1 video):
1. **Embed Syntax (React-Markdown Compatible):** Use either the thumbnail-anchor embed or the `"Watch"` anchor text so the custom `ReactMarkdown` renderer mounts `<YouTubePlayer />` cleanly without breaking inline text citations:
   ```markdown
   [![Section Topic Title](https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)
   > *"Direct 1–2 sentence tactical insight or quote extracted from this specific video transcript explaining the section's core thesis."*
   ```
   *(Or `[Watch the Masterclass Video](https://www.youtube.com/watch?v=VIDEO_ID)` followed by the `> *"...quote..."*` blockquote.)*
2. **Placement:** Distribute the 3–5 video embeds evenly across the major H2 sections so every major tactical shift is reinforced by multi-media authority and maximizes time-on-page.

### Step 4: 3 Bespoke Dark-Mode / Neon B2B SaaS Graphics
Reject generic stock photography. Generate **3 distinct graphics** per article saved into the web app's `public/` directory (e.g., `public/<slug>_hero_01.jpg`, `public/<slug>_action_02.jpg`, `public/<slug>_matrix_03.jpg`):
1. **Visual Aesthetic Prompting:**
   - Dark mode (`#050505` / `#0b0b0b`), glassmorphism UI cards, neon emerald (`#00FFA3`), cyan, and gold accents.
   - Graphic 1 (`_hero_01`): High-impact architectural / geographic / industry hero visualization (referenced in frontmatter `thumbnail:`).
   - Graphic 2 (`_action_02`): Operational / field-execution or financial friction visualization.
   - Graphic 3 (`_matrix_03`): Predictive intent matrix / multi-signal convergence visualization.
2. **Dual-Vessel Image Generation Tools:**

   | Vessel | Image generation tool |
   |--------|-----------------------|
   | **Grok CLI** | `image_gen` (edits: `image_edit`) |
   | **AGY / Antigravity** | `generate_image` (or `invoke_subagent` with `image-generator`) |

   Do not call a tool name that does not exist on your host vessel.

### Step 5: The "Day-Zero Intercept" Pivot (10-Pipeline Integration)
Every Mega Article must pivot from the industry problem to **Day-Zero Public-Record Interception**—showing how asynchronous multi-signal tracking beats cold dragnet outreach across the 10 core intelligence feeds:
1. **`FIC` (Sunbiz Fictitious Names / DBAs) & `NAL` (67-County Tax Roll):** Catching commercial-zoned brand formations before permits or signage bids go public.
2. **`DBPR` (Hotels & Restaurants Plan Reviews) & `ABT` (Liquor Licenses):** Intercepting hospitality buildouts, seating capacities (`dbpr_seats`), and `4COP`/`2COP` quota transfers months before grand opening.
3. **`Permits` (County Building Permits) & `LoopNet` (Commercial Lease Removals):** Detecting physical tenant buildouts (hoods, grease traps, change of occupancy) and signed leases (`MULTI_HIT: LEASE_SIGNED`).
4. **`UCC` (Equipment Financing) & `CORP` (Articles of Organization):** Identifying active capital expenditure and corporate officers (`MGR`/`AMBR`).
5. **`News` (Commercial Press Intelligence) & `Owner Contact Intelligence` (`OWNER_CONTACT_VERIFIED`):** Combining early local press launches with verified principal phone/email/domain piercing via the **Spiderweb Matrix**.

### Step 6: High-Ticket Anchoring, Objection Handling & Word-for-Word Scripts
Include a dedicated tactical execution section featuring:
- **Psychological Price Anchoring:** Concrete numeric framing for high-margin proposals.
- **Copy-Paste Call / Outreach Scripts:** Formatted in clean markdown blockquotes (`> **Script A: The "First in Line" Pivot**`) showing exact prospect objections and the Day-Zero response.

---

## 3. MANDATORY COMPLIANCE & SEO GUARDRAILS

1. **🚨 THE ANTI-COMPETITOR MANDATE (NO FREE AIRTIME):**
   - You are strictly forbidden from mentioning, endorsing, or name-dropping commercial competitors, B2B lead brokers, or third-party SaaS brands (e.g., ZoomInfo, Apollo, HubSpot, Salesforce, LinkedIn, CoStar) in article prose.
   - **Scrubbing Rule:** Always replace brand names encountered in transcripts or research with generic, anonymized terms: *"legacy data brokers"*, *"dragnet contact databases"*, *"enterprise CRM software"*, *"commercial property portals"*, or *"professional social networks"*.
   - **Exception:** Citations to authoritative government, academic, or economic data sources (U.S. Census Bureau, Harvard Business Review, Florida Sunbiz/DBPR, county property appraisers) are required for empirical proof.
2. **PBN Protection (`rel="nofollow"`):**
   - Any cross-links to sister companies or founder-operated properties in author bios or callouts must include `rel="nofollow noopener noreferrer"`.

---

## 4. DUAL-VESSEL FILE TOOLS

Use the file tools of the **host CLI you are running in**. Preserve both columns when maintaining this skill:

| Vessel | Read | Create / overwrite | Edit in place |
|--------|------|--------------------|---------------|
| **Grok CLI** | `read_file` | `write` | `search_replace` |
| **AGY / Antigravity** | `read_file` | `write_to_file` / `write_file` | `replace_file_content`, `multi_replace_file_content` / `edit_file` |

---

## 5. PRE-PUBLISH CHECKLIST
Before marking a Mega Article complete, verify:
- [ ] Valid YAML frontmatter (`title`, `date`, `description`, `category`, `author`, `thumbnail`).
- [ ] **3 to 5** contextual YouTube embeds with `> *"...transcript quote..."*` blockquotes immediately underneath each embed.
- [ ] **3** bespoke dark-mode/neon graphics generated and placed in `public/`.
- [ ] Inline hyperlinked citations on all numeric/market/census claims (0 "Works Cited" footers).
- [ ] Zero competitor brand names in prose (100% scrubbed per the Anti-Competitor Mandate).
- [ ] Production build check (`npm run build` in the dashboard app) passes cleanly.
