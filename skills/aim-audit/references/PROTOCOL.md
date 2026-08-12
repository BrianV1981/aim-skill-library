# Protocol: Evolving Audit

| Field | Value |
|-------|--------|
| **Status** | Canonical SOP for skill `aim-audit` |
| **Home** | `aim-skill-library/skills/aim-audit/references/PROTOCOL.md` |
| **Analog** | `aim-handoff` — **update in place**, do not decapitate |
| **Persona / blueprint** | aim-coagents `aim-auditor` |
| **Supersedes** | Ad-hoc `AUDIT_<TARGET>_<DATE>.md` + `_REAUDIT` + `_AUDIT3` novel-per-pass |

This is the house auditing system. The skill `SKILL.md` is the checklist. **This file is the rubric.** Do not paste it into every vessel `AGENTS.md`.

---

## 0. The idea (yes, you understand it correctly)

Same rule as `aim-handoff`:

> **UPDATE, do not decapitate.** If the living audit exists, **amend it**. Preserve identity and closed history; rewrite the verdict and open queue; do not spawn a sibling novel.

| Object | First write | Every later pass |
|--------|-------------|------------------|
| **Handoff** | ~200-line `HANDOFF.md` | Same file. Finished work → §0. Mission/next → rewritten. |
| **Audit** | Baseline `AUDIT_<SLUG>.md` (long, once) | **Same file.** Closed findings → §0. Smoke matrix + open findings + verdict **updated**. Pass log **appended** (one row). |

**Wrong:** `AUDIT_AIM_JOSHUA_2026-08-12.md` then `…_REAUDIT_…` then `…_AUDIT3_…` (three full reports, same product, one day).

**Right:** `artifacts/AUDIT_AIM_JOSHUA.md` created at `ccd0d5b2`, then edited at `281579f8`, then edited at `f063ce3d`. History lives in **§10 Pass log** + **§0 Closed findings**, not in new filenames.

A re-audit is a **git commit against the audit document**, not a new literary work.

---

## 1. What this audit is (and is not)

These are **product-truth audits**, not PR reviews and not AppSec pentests.

**Is:** Does this A.I.M. (or Operator-named) product do what README / issues / HANDOFF / SOURCE claim, *on this host*, with evidence? Docs honesty, CLI happy paths, GitOps path math, process integrity (empty `Closes #N`), packaging/legal hygiene, secrets.

**Is not:** Maintainability judo (`code-review`). Session self-check (`check-work`). Semgrep/CodeQL trophy hunt (optional **Appendix S** only). Marketplace “/100 security posture” checklists.

OSS skills (Trail of Bits, Anthropic security-review, generic scored greps) are **modules**, never the spine. Steal: false-positive refute, differential review, spec-vs-code, open-source hygiene. Do not replace this protocol with them.

---

## 2. One living document per target

### 2.1 Canonical path

```text
artifacts/AUDIT_<SLUG>.md
```

| Rule | Example |
|------|---------|
| Slug = stable product id, `A-Z0-9_`, no date | `AIM_JOSHUA`, `AIM_CONNECT`, `AGENT_REACH` |
| No `_REAUDIT`, `_AUDIT3`, `_2026-08-12` in the **canonical** name | — |
| Dated files are **legacy** or **snapshots**, not the working copy | see §2.3 |

Header of the living file always shows **current** SHA, grade, mode, and last-updated. Prior SHAs belong in the pass log, not in the filename.

### 2.2 Optional findings sidecar (same slug)

If the findings table gets large, also keep:

```text
artifacts/AUDIT_<SLUG>.findings.yaml
```

Markdown tables in the living doc remain the Operator-facing source. The YAML is for join/diff across passes. **Do not** let them diverge — update both in the same pass, or skip YAML until the skill exists.

### 2.3 When a new file is allowed

| Situation | Action |
|-----------|--------|
| First audit of a target | Create `AUDIT_<SLUG>.md` (baseline) |
| Later pass, same product, same scope | **Edit that file** |
| Scope change (new tenant model, new CLI surface, incident) | Edit in **event** mode; may rewrite §1 / §8. Snapshot old file first. |
| Operator asks for a frozen PDF/share | Copy to `artifacts/archive/AUDIT_<SLUG>_<YYYY-MM-DD>_<sha7>.md` then keep editing the canonical file |
| Accidental sibling novels already exist (Joshua #1/#2/#3) | **Collapse** into one living file on the next pass (see §11) |

Do **not** start a new numbered audit file because “this is pass 4.”

---

## 3. Modes

Every pass declares exactly one mode in the header.

| Mode | When | What you write |
|------|------|----------------|
| **`baseline`** | First time, or Operator says “full E2E from zero” | Full template. Invent the smoke contract. Assign finding IDs. Write architecture once. |
| **`delta`** | **Default** for every later pass | Re-run smoke. Update finding statuses. Rewrite verdict + next actions. Append pass-log row. **Do not** rewrite identity/architecture unless they changed. |
| **`closeout`** | Series should stop (Connect #8 instinct) | Freeze vs backlog. Verdict = “event-driven from here.” No new hunt unless scoped. |
| **`event`** | Major scope change or incident | May rewrite §1 / §8. Snapshot first. Treat like a small baseline grafted onto the same file. |

**Default if unspecified: `delta`** whenever `AUDIT_<SLUG>.md` already exists.

Connect’s eight full novels were a missing-mode failure. Joshua #2/#3 wanted to be deltas and still carried the origin story. This protocol makes that a rule violation.

---

## 4. Gold-standard template (numbered sections)

Canonical shape: sections **0–10**. Mission titles may specialize; **numbers and roles stay**.

On **delta** / **closeout**, most sections are *edited in place*, not regenerated. §5 and the pass-log row are the only places that grow freely.

```markdown
# Audit: <product name>

| Field | Value |
|-------|--------|
| **Repo** | <url> |
| **Clone** | <abs path> |
| **Commit** | `<sha>` — *<subject>* (<tz stamp>) |
| **Mode** | baseline \| delta \| closeout \| event |
| **Pass** | N (increment; do not fork a new file) |
| **Overall grade** | <letter> (was <prior>) |
| **Root / engine VERSION** | … |
| **License** | claimed vs repo vs `gh api` |
| **Auditor** | grok-audit vessel |
| **Updated** | <ISO local> |
| **Open GH issues** | count or “none” |

---

## 0. CLOSED FINDINGS (DO NOT RE-HUNT)

| ID | Title | Closed at SHA | One-line evidence |
|----|-------|---------------|-------------------|
| SLUG-001 | … | `abc1234` | … |

*(Consolidate. Point at GH issues / wiki for deep history. Do not re-prove closed items unless the smoke row regresses.)*

---

## 1. IDENTITY

*(1–3 sentences: what the system is. Runtime ASCII **only on baseline or event**. Later passes: edit if the product changed, else leave.)*

---

## 2. VERDICT

*(One blunt paragraph + overall grade + “safe to / do not use X”. Must be current. Rewrite every pass.)*

---

## 3. SMOKE MATRIX

| Probe | Last | **Now** | Notes |
|-------|------|---------|-------|
| `./aim doctor` | PASS | **PASS** | |

*(Same probes every pass. Add a row only when the product grows. Timeouts + exit codes required on FAIL/HANG.)*

---

## 4. OPEN FINDINGS

| ID | Sev | Status | Title | Last evidence |
|----|-----|--------|-------|---------------|
| SLUG-004 | HIGH | open | … | … |

*(Status: `open` \| `partial` \| `regressed`. Detail in subsections only for **changed** items this pass.)*

---

## 5. DELTA THIS PASS

*(SHA range. Commit table: issue #, material?, empirical result. Empty closes called out. On baseline: “n/a — first pass.”)*

---

## 6. GRADE ROLLUP

| Area | Prior | **Now** | Why (≤1 line) |
|------|-------|---------|---------------|
| … | C | **B−** | … |

---

## 7. SECURITY

| Check | Result |
|-------|--------|
| Secret heuristic | Clean / finding ID |
| LICENSE | … |
| Side-effect commands | … |

*(Optional **Appendix S** for Semgrep / Trail of Bits / secret-history — never rewrite §2 from Appendix S alone.)*

---

## 8. ARCHITECTURE / CONTRACT

*(Frozen after baseline. Edit only on event or proven product change. Smoke contract listed here so later vessels re-run the **same** commands.)*

---

## 9. NEXT ACTIONS

1. **SEV — Title.** One line. Link finding ID.
2. …

*(Queue for the *product* owner / next audit. Imperative. Closed items leave this list.)*

---

## 10. PASS LOG

| Pass | Mode | When | SHA | Grade | One-line |
|------|------|------|-----|-------|----------|
| 1 | baseline | 2026-08-12 | `ccd0d5b2` | C+ | First E2E; search hang |
| 2 | delta | 2026-08-12 | `281579f8` | C | Promote regression |
| 3 | delta | 2026-08-12 | `f063ce3d` | B− | Critical list closed |

---

*Method: <commands, timeouts, read-only?>. Auditor does not modify the **target** repo unless Operator scoped a fix.*
```

### Section duties (anti-bloat)

| § | Baseline | Delta | Closeout |
|---|---------|-------|----------|
| 0 | empty or n/a | **Move** newly closed findings here; shrink | Freeze |
| 1 | write | leave unless changed | leave |
| 2 | write | **rewrite** | **rewrite** (stop/event-driven) |
| 3 | invent contract | **re-run + update cells** | re-run once |
| 4 | assign IDs | update status; add only new IDs | open = backlog |
| 5 | n/a | **this is the new prose** | short “why we stop” |
| 6 | write | update changed rows only | final |
| 7 | write | re-scan; one-line unless new hit | freeze |
| 8 | write + freeze | do not rewrite | do not rewrite |
| 9 | write | **replace** with current queue | freeze vs backlog split |
| 10 | first row | **append one row** | append closeout row |

---

## 5. Finding records (stable IDs)

Findings are tickets, not paragraphs. IDs **never change**. Titles may be edited for clarity.

```text
<SLUG>-<NNN>
```

Examples: `JOSH-001`, `CONN-012`, `REACH-003`.

| Field | Values / rule |
|-------|----------------|
| **id** | Assigned at first sighting; monotonic per slug |
| **title** | Imperative or noun phrase, stable enough to grep |
| **severity** | `critical` \| `high` \| `med` \| `low` |
| **status** | `open` \| `partial` \| `closed` \| `wontfix` \| `regressed` |
| **first_seen** | SHA of the pass that created the ID |
| **last_verified** | SHA of this pass |
| **evidence** | Command, exit code, path, timing, `gh` result — not a vibe |

**Close rule:** status → `closed` only with **this-pass evidence** (smoke row or targeted probe). A GitHub “Closes #N” commit that is empty (`git show --name-only` blank) is **not** a close. That is a **process-integrity** finding (new ID or reopen).

**Regress rule:** a previously closed ID that fails smoke again → `regressed`, move **back** from §0 to §4. Do not mint a new ID for the same bug.

**Refute rule (stolen from Trail of Bits `fp-check`):** before raising `critical` / `high`, try to kill it. Hanging Ollama is not an F of the product if fail-fast + lexical fallback works; it is an F if the CLI stalls 75s with no notice. Write the refute attempt in evidence.

Optional YAML shape (sidecar):

```yaml
- id: JOSH-007
  title: cmd_promote repo_root wrong
  severity: critical
  status: closed
  first_seen: ccd0d5b2
  last_verified: f063ce3d
  evidence: "git-common-dir → <clone-root> ; .git True"
```

---

## 6. Grade rubric (so letters mean something)

Letter grades stay — Operators read them. They are **not** an average of twelve vibes.

### 6.1 Area scale

| Grade | Meaning |
|-------|---------|
| **F** | Advertised happy path cannot complete (hang, crash, wrong tree, missing module) |
| **D** | Path sometimes works; packaging/legal or tracked poison (pyc, live DBs) is severe |
| **C** | Path works; docs / CI / issue board **lie** or tests are absent |
| **B** | Daily-driver on this host; residual polish (UX, seed freshness, handbook lag) |
| **A** | Public-OSS bar: tests **exercise the path**, docs match CLI, no process theater |

Modifiers (`+` / `−`) are allowed. Do not invent `A++`.

### 6.2 Overall grade

```text
overall = min(
  security/secrets area,
  worst area that is an *advertised* critical path
)
```

Unadvertised extras (swarm, MCP, bake) can sit at C without capping the overall grade unless the README leads with them.

**Process integrity** can cap overall at **C** if the board is greener than the tree (empty closes as the main motion).

### 6.3 Grade motion

Every delta pass fills **Prior → Now** in §6. Motion needs a why-line. “Docs improved, promote regressed” is a valid **down** grade. Do not inflate because the team was busy.

Across products, grades are only comparable **because this rubric exists**. Joshua B− vs Connect A− vs Agent-Reach A must be defensible against the table above.

---

## 7. Smoke contract

§8 lists the **exact commands** for this target. Later vessels re-run **those**, not a new invented tour.

Minimum fleet contract (A.I.M. vessels) — specialize per product:

```text
./aim --help
./aim doctor
./aim map
timeout 25 ./aim search worktree --top-k 1
# promote path math (print repo_root + test -d "$repo_root/.git")
gh api repos/<owner>/<repo>/license --jq .license.spdx_id
# secrets heuristic (keys / PEM / AKIA) — tracked files only
```

Rules:

- Always use **timeouts** on network/embed paths. Record `rc` and whether stdout was empty.
- Prefer the project’s own `test.sh` / `pytest` when it exists (Agent-Reach model). Absence of tests is a finding, not a skip of the CLI matrix.
- Do not add probes that cannot be re-run next pass.
- Read-only vs the **target** repo. The living audit file in this desk’s `artifacts/` is what you write.

---

## 8. Update rules (anti-bloat) — copy of handoff spirit

1. **One file.** If `artifacts/AUDIT_<SLUG>.md` exists, open it. Do not `write` a sibling.
2. **Move finished work to §0** with one-line evidence. Delete the old §4 essay for that ID.
3. **Rewrite §2 and §9 every pass** for the *current* Operator. More detail on what is still true / still open than on the victory lap.
4. **§5 is the only new narrative.** SHA range, material commits, empty closes, regressions.
5. **§10 appends one row.** Never rewrite old rows except to fix a factual error.
6. **Do not regenerate architecture ASCII** on delta.
7. **Unknown → `UNKNOWN`.** Proven → path, SHA, issue #, command, count, exit code.
8. **No forced docs trees.** Do not invent `docs/audit/` or roadmaps the Operator did not ask for.
9. **Target repo stays clean** unless the Operator scoped a fix. Audits do not drive-by LICENSE files on the product.
10. **Collapse siblings** when you find dated novels for the same slug (see §11) before starting a new pass.

Length budget (guidance, not a hard linter):

| Mode | Target |
|------|--------|
| baseline | As long as needed (Joshua #1 size is OK) |
| delta | **~1–2 pages of new/changed text**; file may stay long because §0/§8/§10 accumulate |
| closeout | Short §2 + freeze/backlog table + pass-log row |

If a delta pass rewrites §1 and §8 without an event, it is doing it wrong.

---

## 9. Pass workflow (agent checklist)

```text
1. Identify slug + clone + tip SHA.
2. If artifacts/AUDIT_<SLUG>.md missing → mode=baseline, create from template.
3. Else mode=delta (unless Operator said closeout/event).
4. Snapshot only if event/closeout-for-share: copy to artifacts/archive/…
5. Read living file. Do not re-derive identity from README if §1 exists — verify it.
6. Git log prior_sha..HEAD. Mark each commit material? / empty close?
7. Re-run §8 smoke contract with timeouts. Fill §3 Last/Now from previous Now.
8. For each open ID: still true? close / partial / regress. Refute new critical/high.
9. Mint IDs only for genuinely new defects.
10. Rewrite §2 verdict + §9 queue. Update §6 changed rows. §7 one-pass scan.
11. Append §10 row. Bump Pass N. Update header SHA/grade/date.
12. Stop. Do not file GH issues on the target unless Operator asked.
```

Inquiry vs directive still applies: if the Operator only asked “what’s the grade?”, answer from the living file and stop. If they asked to audit, execute this checklist.

---

## 10. What we keep from the old novels

These habits were already good. They survive:

- Hostile to claims (README / CHANGELOG / `Closes #N` vs tree vs runtime)
- SHA-pinned header
- Smoke matrix with a prior-pass column
- Process integrity as a first-class area
- Verdicts that can be **withdrawn** (“do not use promote” → withdrawn in §2, ID closed in §0)
- Method footer, read-only default
- Letter grades **inside a series**

These habits die:

- New 250-line file per pass
- Re-explaining the product thesis every time
- Grading twelve areas from scratch when two changed
- Findings without IDs
- Uncalibrated A/B/C across the fleet
- Serial-auditing after closeout with no event

---

## 11. Migrating existing dated reports

On the **next** pass of a target that already has siblings:

1. Choose the **newest** dated report as the text donor.
2. Create (or overwrite) `artifacts/AUDIT_<SLUG>.md` in the gold template.
3. Fold prior reports into **§10 Pass log** (one row each) and **§0 / §4** with minted IDs.
4. Leave the old dated files in place as **legacy snapshots** (do not delete unless Operator asks). Add a one-line pointer at the top of each old file *or* only in the living file’s pass log — prefer **only the living file** points at them, so we do not edit history noisily.
5. All future edits go to the living file.

Joshua (as of 2026-08-12) should collapse like this on next touch:

| Legacy file | Becomes |
|-------------|---------|
| `AUDIT_AIM_JOSHUA_2026-08-12.md` | Pass 1 baseline @ `ccd0d5b2` C+ |
| `AUDIT_AIM_JOSHUA_REAUDIT_2026-08-12.md` | Pass 2 delta @ `281579f8` C |
| `AUDIT_AIM_JOSHUA_AUDIT3_2026-08-12.md` | Pass 3 delta @ `f063ce3d` B− |
| **New canonical** | `artifacts/AUDIT_AIM_JOSHUA.md` |

Do **not** collapse until a real pass (or Operator says “collapse now”). This protocol file does not rewrite product audits by itself.

Connect #1–#8 should become `AUDIT_AIM_CONNECT.md` with pass log 1–8 and a **closeout** row at #8, if/when next touched.

---

## 12. Where this lives (fleet)

| Layer | Repo | Load when |
|-------|------|-----------|
| Always-on pointer | Specialist `AGENTS.md` / blueprint `aim-auditor` | Every turn on an auditor node |
| Checklist | skill `aim-audit` `SKILL.md` | Audit / re-audit / `/aim-audit` |
| This rubric | `references/PROTOCOL.md` | Baseline, event, or when grades/IDs are unclear |
| Wiki | Optional search card that **points here** | `./aim search evolving audit` |

Do not duplicate this SOP into `AGENTS.md` or a wiki page.

---

## 13. Worked miniature (how a delta feels)

Header bump only:

```text
Pass 3 → 4
Mode: delta
Commit: <new sha>
Grade: B− → B− (no advertised-path change)
```

§5 (new):

```text
abc1234  #46 pretty-print search   material yes   PASS compact recitation
```

§4: `JOSH-010` (search JSON dump) → move to §0.

§3: search row notes “human format; --json still works”.

§9: drop that action.

§10: append one row.

**Do not** rewrite “J.O.S.H.U.A. is the intended CLI-agnostic convergence OS…” again.

That is the whole point.

---

*Drafted 2026-08-12 by grok-audit after review of Joshua #1–#3, Connect #8, Agent-Reach, and `aim-handoff`. Empirical over ceremonial. Update this protocol in place the same way.*
