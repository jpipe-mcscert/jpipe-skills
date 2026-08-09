---
name: jpipe-review
description: "Reviews the argument in an existing jPipe justification model (.jd), one model at a time. Checks abstraction (evidence supplies a datum, strategy licenses the inference, conclusion asserts the claim, i.e. Toulmin's grounds/warrant/claim), atomicity (one leaf, one fact), grounding (the artifacts the evidence names actually exist in the repository), and the house style. Emits a findings report with file:line and rule ids; edits are applied only after you approve them. Syntax and unresolved-symbol errors are left to `jpipe diagnostic` and the VS Code extension. Use when asked to review, audit, critique, sanity-check, or improve a .jd file, a justifications/ directory, or an assurance case. NOT for writing a new model from scratch, NOT for cross-model reuse or corpus-wide analysis, which is jpipe-survey's job, NOT for reviewing the jpipe-runner step library that implements the checks, NOT for reviewing the jPipe compiler's own source."
argument-hint: "[path/to/model.jd | justifications/ | glob] [--no-grounding] [--apply]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Review

Syntax is the compiler's job. This reviews whether the argument *means* anything.

## Usage

```
jpipe-review <target> [--no-grounding] [--apply]
```

**Target**: a `.jd` file, a directory (recurse `*.jd`), a glob, or nothing (the changed `.jd` files).
A directory target is **N independent reviews**, not one review of a corpus. **Flags**:
`--no-grounding` skips the repository-artifact pass. `--apply` continues into the fix loop.

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/rules.md` | any time you cite a rule id (Steps 2–5) |
| `references/abstraction.md` | Step 2, and Step 6 when writing a replacement label |
| `references/grounding.md`, then `references/artifacts.md` | Step 3 |
| `references/conventions.md` | Step 4 |
| `references/language.md` | whenever a fix adds, moves, or re-ids an element, or touches a label that may unify |
| `references/report-format.md` | Step 5 |

## When to invoke

Reviewing, auditing, or improving an existing `.jd`; onboarding an inherited assurance case; a
pre-merge check over a `justifications/` directory.

### Do NOT invoke for

- Writing a new model from scratch, or reviewing the **step library** (`steps/`, `@jpipe_link`
  modules) or the jPipe compiler's own source.
- **Cross-model questions**: is this fact argued twice elsewhere, will these two labels unify, does
  anything load this model. Those need a corpus, so they are `jpipe-survey`'s.
- Rendering a diagram. That is one command: `jpipe process -m <model> -i <f> -f SVG -o <out>.svg`.

## Guardrails

- **One model at a time.** Exactly one model is under review; the files it `load`s are dependencies
  the compiler needs, not subjects. Never read, `grep`, quote, or propose an edit to any other `.jd`,
  and never widen the target set. A finding that needs a second model to state is not one this skill
  can make. Given a directory, review each file on its own terms; do not correlate across them.
- **Read-only through Step 5.** Nothing is modified before the author approves a numbered fix list.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a
  pull request. Report; the author integrates.
- **Never re-report what the compiler already said**, and never open a file under `steps/` or any
  `@jpipe_link` module: out of scope, and its contents can never be a finding.
- **Never silently re-id or renumber.** `assemble` unification is positional; a one-line label edit
  can shift every downstream `unified_N`.
- **Write the report for the engineer who built the system.** No Toulmin vocabulary, no severity
  words, no rule id standing in for an explanation. Say what is wrong, why it matters to them, and
  what their options are. → `references/report-format.md`
- **Every label you propose is short**: under 10 words for a fact, under 15 for a check. Labels are
  diagram node text, and unification is exact string equality. → `references/abstraction.md` §3b
- **Prefer an open question to a shaky finding.** Two false positives and the author stops reading.

## Workflow

### Step 1. Scope

Resolve the target list, and then treat it as closed: those models, and no others, are what this
review is about. Per target, note the files it `load`s: read for context, never reviewed, never the
site of a finding. Note the repository root (Step 3).

**Do not compile anything yet.** An argument's shape is legible long before it parses, the author
already knows whether the file builds, and compilation belongs at Step 7 where it verifies work this
skill did. Locations therefore come from the file as read: `file:line`.

For more than 8 files, plan to batch Steps 2–4 and emit **one** consolidated report, still one
verdict per model.

### Step 2. Roles and atomicity *(within each model)*

Assign every element its role and check it against its jPipe kind. Classify each `evidence` leaf as a
fact, a verdict in a fact's place, or two facts fused; check each `strategy` licenses one inference and
performs **one** check; check each `sub-conclusion` states what its leg establishes.

**Count the jobs per element, and where there are two, decompose.** One leg per fact and per check is
the recommendation this skill leads with, not a fallback: a split argument reports *which* half failed.
Do the fused elements first, since the legs they produce are what later findings are written against,
and a fused leaf gives Step 3 nothing to search for.

Classify each file 🟢/🟡/🟠/⚪. → `references/abstraction.md`

### Step 3. Grounding *(evidence → repository)*

For each atomic evidence leaf, extract the artifact it names, decide what kind of thing it is, and
search: `Glob` for paths, `Grep` for sections and symbols. **Record the exact searches**, because a
grounding finding must state what was looked for and where, or it is an open question instead.

Skipped under `--no-grounding`, and when the models are not inside a project tree.
→ `references/grounding.md`

### Step 4. House style *(within this file)*

First check whether the project states its own conventions (`CLAUDE.md`, `justifications/README.md`,
a contributing guide). If it does, that document wins and this pass defers to it. Otherwise: refine
placement, conclusions at goal level, provenance headers, and leaves carrying a requirement tag that
suggests a refine. Every check is decided from this file alone; one needing a second model is not in
this pass. → `references/conventions.md`

### Step 5. Report

Emit the report in exactly the shape of `references/report-format.md`. Read that file before writing
a word of it: the reader is **the engineer who built the system**, not a safety specialist, and every
finding owes them three things in order, *what is wrong*, *why it matters to them*, and *the options*.

Nothing internal to this skill appears there: no Toulmin vocabulary, no severity words, no rule id
doing an explanation's work. Ids appear once per finding, at the end, as a reference number.

Keep **Open questions** and **Not looked at**: they state the review's own limits, and single-model
scope is one, so no clean report reads as a claim about the corpus.

**Stop here** unless `--apply` was given.

### Step 6. Propose and get approval

Present a numbered fix list in the report's voice, not the catalogue's. Each entry: which finding it
closes, the exact before and after text, what it costs, and any fix it depends on. Order by dependency,
not severity (`rules.md`): decompositions first, then rewords, then structure.

Ask in prose which numbers to apply. Never act on silence or an ambiguous answer, and never widen beyond
what was approved. Every edit lands in the file under review; a fix needing another model is out of
scope, so report it and leave it.

### Step 7. Apply and verify

The one step that compiles. `Edit` only the approved items, then per touched file:
`jpipe --headless diagnostic -i <file>`, capturing stdout, stderr and the exit code **separately**. A
file passes only if the exit code is `0` **and** stderr is empty: a failed `load` reports entirely on
stderr, leaving stdout completely empty, so a check reading stdout alone calls a broken file clean.
Then `jpipe process -m <model> -i <file> -f SVG -o <tmp>` to prove it still renders.

If `jpipe` is not on PATH, say so and stop **before editing**: an unverifiable edit to an assurance
case is worse than a reported finding. Everything through Step 6 runs without the compiler.

A file that did not build before your edit still must build after it; if it did not compile going in,
say so rather than claiming the edit broke it. If any applied fix could create, destroy or rename a
unified group, name the hazard: the composed model that would renumber is one this skill does not read,
so that re-render is the author's to run. Close with the delta: findings closed, findings remaining,
anything newly introduced.

## Output contract

The report is the product, and it is written for the engineer who built the system. Every finding
gives them a `file:line`, the label quoted, what is wrong, why it matters to them, their options with
the trade-off named, and what the edit costs. The rule id goes last, as a reference number.

Verdicts, **per model**: **CLEAN** · **FINDINGS**. CLEAN means the model holds on its own terms, says
nothing about how it sits with any other, and says nothing about whether the file compiles.
