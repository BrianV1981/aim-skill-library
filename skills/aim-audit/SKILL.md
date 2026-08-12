---
name: aim-audit
description: >
  Evolving product-truth audit: one living artifacts/AUDIT_<SLUG>.md, update
  in place (aim-handoff rules), never dated _REAUDIT/_AUDIT3 novels. Modes
  baseline|delta|closeout|event. Use for audit, re-audit, /aim-audit, or when
  the Operator asks how a target is doing vs its README.
---

# `aim-audit`

> **MANDATE:** Product-truth, not a new literary work. If the living audit exists, **amend it**.

Pair with persona **`aim-auditor`** (aim-coagents) when you need the hat. This skill is the **procedure**.

Canonical rubric: [`references/PROTOCOL.md`](references/PROTOCOL.md). Read it on **baseline**, **event**, or when grades/IDs are unclear. Do not inline it into `AGENTS.md`.

---

## 1. Law (same spirit as `aim-handoff`)

1. **UPDATE, do not decapitate.** One file: `artifacts/AUDIT_<SLUG>.md` (slug `A-Z0-9_`, no date).
2. **No sibling novels.** `_REAUDIT`, `_AUDIT3`, `_<YYYY-MM-DD>` are legacy snapshots, not the working copy.
3. **No guesses.** Unknown → `UNKNOWN`. Proven → path, SHA, issue #, command, exit code, count.
4. **Target repo stays clean** unless the Operator scoped a fix. You write the audit file on *this* desk.
5. **Default mode is `delta`** when the living file exists.

## 2. Modes

| Mode | When | Write |
|------|------|--------|
| **baseline** | No living file, or Operator says full E2E from zero | Full §0–§10. Invent smoke contract. Mint finding IDs. |
| **delta** | **Default** later pass | Re-run smoke. Update statuses. Rewrite §2 + §9. Append §10 row. Do not rewrite identity/architecture unless they changed. |
| **closeout** | Series should stop | Freeze vs backlog. Event-driven from here. |
| **event** | Scope change or incident | Snapshot first if sharing. May rewrite §1 / §8. |

## 3. Checklist (every pass)

```text
1. Slug + clone + tip SHA.
2. Living file missing → baseline; else delta (unless Operator said closeout/event).
3. Read the living file. Verify §1; do not re-derive from README if it exists.
4. git log <prior_sha>..HEAD — material? empty close?
5. Re-run §8 smoke with timeouts. Fill §3 Last/Now.
6. Open IDs: close / partial / regress. Refute new critical/high.
7. Mint IDs only for new defects (<SLUG>-NNN).
8. Rewrite §2 verdict + §9 queue. Update changed §6 rows. §7 scan.
9. Append §10 row. Bump Pass N. Header SHA/grade/date.
10. Stop. Do not file GH issues on the target unless asked.
```

## 4. Template (roles stay; numbers stay)

```markdown
# Audit: <product>

| Field | Value |
|-------|--------|
| **Repo** | url |
| **Clone** | path |
| **Commit** | `sha` — subject (stamp) |
| **Mode** | baseline \| delta \| closeout \| event |
| **Pass** | N |
| **Overall grade** | letter (was prior) |
| **Auditor** | vessel / persona aim-auditor |
| **Updated** | stamp |

## 0. CLOSED FINDINGS (DO NOT RE-HUNT)
## 1. IDENTITY
## 2. VERDICT
## 3. SMOKE MATRIX
## 4. OPEN FINDINGS
## 5. DELTA THIS PASS
## 6. GRADE ROLLUP
## 7. SECURITY
## 8. ARCHITECTURE / CONTRACT
## 9. NEXT ACTIONS
## 10. PASS LOG
```

Delta: §5 is the only new narrative. §10 appends one row. Move closed IDs to §0.

## 5. Findings

`STATUS`: `open` | `partial` | `closed` | `wontfix` | `regressed`  
`SEV`: `critical` | `high` | `med` | `low`

Close only with this-pass evidence. Empty `Closes #N` (`git show --name-only` blank) is a **process-integrity** finding. Regress → move ID back from §0 to §4; do not mint a new ID.

**Refute** critical/high before filing.

## 6. Grades (short)

| Letter | Meaning |
|--------|---------|
| **F** | Advertised happy path cannot complete |
| **C** | Path works; docs/CI/board lie or tests absent |
| **B** | Daily-driver; residual polish |
| **A** | Public-OSS: tests exercise the path; docs match CLI |

`overall = min(secrets area, worst *advertised* critical path)`. Process theater can cap at **C**. Full rubric: PROTOCOL.

## 7. Smoke (minimum; specialize in §8)

Use timeouts on embed/network paths. Prefer the target’s own `test.sh` / pytest when present.

A.I.M. vessels (adapt names; do not assume a global `aim` alias):

```bash
./aim --help
./aim doctor
./aim map
timeout 25 ./aim search worktree --top-k 1
# promote: print repo_root; test -d "$repo_root/.git"
# LICENSE: gh api repos/<owner>/<repo>/license --jq .license.spdx_id
# secrets heuristic on tracked files only
```

Host CLIs differ; invoke the project wrapper or `joshua_os/.aim_core/aim_cli.py` (legacy nest: `aim-agy_os/`).

## 8. File / edit tools (dual vessel)

When creating or amending the living audit:

| Host | Create / overwrite | Edit in place | Read |
|------|--------------------|---------------|------|
| **Grok** | `write` | `search_replace` | `read_file` |
| **AGY** | `write_to_file` | `replace_file_content` | host read |

## 9. Triggers

`/aim-audit`, audit, re-audit, “how is \<product\>”, living audit, `AUDIT_<SLUG>.md`.

## 10. Relationship

| Piece | Home |
|-------|------|
| Procedure (this) | **aim-skill-library** `skills/aim-audit` |
| Full SOP | `references/PROTOCOL.md` |
| Role hat | aim-coagents `personas/aim-auditor` |
| Lasting peer DNA | aim-coagents `blueprints/aim-auditor` |
| Session baton | `aim-handoff` (different job) |
