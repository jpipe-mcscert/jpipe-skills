---
name: jpipe-review
description: "Reviews the argument in an existing jPipe justification model (.jd), one model at a time. Checks abstraction (evidence supplies a datum, strategy licenses the inference, conclusion asserts the claim, i.e. Toulmin's grounds/warrant/claim), atomicity (one leaf, one fact), grounding (the artifacts the evidence names actually exist in the repository), and the house style. Reads only the model it was given and the files it loads; never surveys other models. Emits a findings report with file:line and rule ids; edits are applied only after you approve them. Syntax and unresolved-symbol errors are left to `jpipe diagnostic` and the VS Code extension. Use when asked to review, audit, critique, sanity-check, or improve a .jd file, a justifications/ directory, or an assurance case. NOT for writing a new model from scratch, NOT for cross-model reuse or corpus-wide analysis, NOT for reviewing the jpipe-runner step library that implements the checks, NOT for reviewing the jPipe compiler's own source."
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
| `references/rules.md` | any time you cite a rule id (Steps 3–6) |
| `references/abstraction.md` | Step 3, and Step 7 when writing a replacement label |
| `references/grounding.md`, then `references/artifacts.md` | Step 4 |
| `references/conventions.md` | Step 5 |
| `references/language.md` | whenever a fix adds, moves, or re-ids an element, or touches a label that may unify |
| `references/report-format.md` | Step 6 |

## When to invoke

Reviewing, auditing, or improving an existing `.jd`; onboarding an inherited assurance case; a
pre-merge check over a `justifications/` directory.

### Do NOT invoke for

- Writing a new model from scratch.
- **Cross-model questions**: is this fact argued twice elsewhere, will these two labels unify, does
  anything load this model. All of them need a corpus, and this skill does not have one.
- Reviewing the **step library** that implements the checks (`steps/`, `@jpipe_link` modules).
- Reviewing the jPipe compiler's own source.
- Rendering a diagram. That is one command: `jpipe process -m <model> -i <f> -f SVG -o <out>.svg`.

## Guardrails

- **One model at a time.** Exactly one model is under review; the files it `load`s are dependencies
  the compiler needs, not subjects. Never read, `grep`, quote, or propose an edit to any other `.jd`,
  and never widen the target set. A finding that needs a second model to state is not one this skill
  can make. Given a directory, review each file on its own terms; do not correlate across them.
- **Read-only through Step 6.** Nothing is modified before the author approves a numbered fix list.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a
  pull request. Report; the author integrates.
- **Never re-report what the compiler already said.** Diagnostics are a gate, not findings.
- **Never open a file under `steps/`** or any `@jpipe_link` binding module. Out of scope, and its
  contents can never be a finding.
- **Never silently re-id or renumber.** `assemble` unification is positional; a one-line label edit
  can shift every downstream `unified_N`.
- **Name the authority on every finding** that is not `language`. Toulmin (`argument`) and house
  practice (`house`) are proposals the author may decline.
- **Prefer an open question to a shaky finding.** Two false positives and the author stops reading.

## Workflow

### Step 1. Scope

Resolve the target list, and then treat it as closed: those models, and no others, are what this
review is about. Run `jpipe --version` and record it for the report header; if `jpipe` is not on PATH,
say so and stop, because the compile gate is not optional. Per target, note the files it `load`s: read
so the target compiles, never reviewed, never the site of a finding. Note the repository root (Step 4).

For more than 8 files, plan to batch Steps 3–5 and emit **one** consolidated report, still one
verdict per model.

### Step 2. Compile gate

Per file: `jpipe --headless diagnostic -i <file>`, capturing stdout, stderr, and the exit code
separately.

A file passes only if the exit code is `0` **and** stderr is empty. A failed `load` is fatal and
reports **entirely on stderr, leaving stdout completely empty**, not even a Diagnostics header. A
gate that reads stdout alone will call a broken file clean.

On failure: record *that* the file does not build, keep the compiler's raw output verbatim for the
report's **Not reviewed** section, and skip Steps 3–5 for that file. Do not explain, rank, or
catalogue the diagnostics.

On success: keep the `=== Symbol Table ===` block. It maps every element id to `line:col`, and it is
where the locations in your findings come from.

### Step 3. Abstraction & atomicity *(within each model)*

Assign every element its Toulmin role and check it against its jPipe kind. Classify each `evidence`
leaf as a datum, a claim in a grounds slot, or two facts fused; check each `strategy` licenses an
inference; check each `sub-conclusion` states what its leg establishes.

Resolve fused leaves **first**: a fused leaf has no single artifact, so it also has nothing for Step 4
to search for.

Classify each file 🟢/🟡/🟠/⚪. → `references/abstraction.md`

### Step 4. Grounding *(evidence → repository)*

For each atomic evidence leaf, extract the artifact it names, decide what kind of thing it is, and
search: `Glob` for paths, `Grep` for sections and symbols. **Record the exact searches**, because a
grounding finding must state what was looked for and where, or it is an open question instead.

Skipped under `--no-grounding`, and when the models are not inside a project tree.
→ `references/grounding.md`

### Step 5. House style *(within this file)*

First check whether the project states its own conventions (`CLAUDE.md`, `justifications/README.md`,
a contributing guide). If it does, that document wins and this pass defers to it.

Otherwise: refine placement, conclusions at goal level, provenance headers, and leaves carrying a
requirement tag that suggests a refine. Every check here is decided from this file alone. If a
convention would need a second model to check, it is not in this pass.
→ `references/conventions.md`

### Step 6. Report

Emit the report in exactly the shape of `references/report-format.md`, including the **Open
questions** and **Not reviewed** sections, which are where the review states its own limits. Name
single-model scope among them, so no CLEAN verdict reads as a claim about the corpus.

**Stop here** unless `--apply` was given.

### Step 7. Propose and get approval

Present a numbered fix list. Each entry: the finding id **with its rule description**, the exact
before and after text, the blast radius, and any fix it depends on. Order by dependency, not severity:
atomicity splits before what depends on them, label rewords before structural changes.

Ask in prose which numbers to apply. Never act on silence or an ambiguous answer, and never widen
beyond what was approved. Every edit lands in the file under review; a fix that would require
touching another model is out of scope, so report it and leave it.

### Step 8. Apply and re-verify

`Edit` only the approved items. Then re-run the Step 2 gate on every touched file (all must pass)
and `jpipe process -m <model> -i <file> -f SVG -o <tmp>` to prove the model still renders.

If any applied fix could create, destroy, or rename a unified group, say so and name the hazard. The
composed model that would renumber is a file this skill does not read, so the re-render is the
author's to run, not yours to report on.

Close with the delta: findings closed, findings remaining, anything newly introduced.

## Output contract

The report is the product. Every finding carries a rule id **and that rule's description quoted from
`rules.md`**, a `file:line:col`, the label quoted, the proposed replacement, and a blast-radius line:
a bare `JD-A01` is a lookup key, not a finding.

Verdicts, **per model**: **CLEAN** · **FINDINGS** · **BLOCKED** (did not compile). CLEAN means the
model holds on its own terms, and nothing about how it sits with any other.
