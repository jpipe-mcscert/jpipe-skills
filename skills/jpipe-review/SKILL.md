---
name: jpipe-review
description: "Reviews the argument in an existing jPipe justification model (.jd). Checks abstraction (evidence supplies a datum, strategy licenses the inference, conclusion asserts the claim, i.e. Toulmin's grounds/warrant/claim), atomicity (one leaf, one fact), grounding (the artifacts the evidence names actually exist in the repository), reuse (facts argued twice across models that should share one unified node), and the corpus conventions. Emits a findings report with file:line and rule ids; edits are applied only after you approve them. Syntax and unresolved-symbol errors are left to `jpipe diagnostic` and the VS Code extension. Use when asked to review, audit, critique, sanity-check, or improve a .jd file, a justifications/ directory, or an assurance case. NOT for writing a new model from scratch, NOT for reviewing the jpipe-runner step library that implements the checks, NOT for reviewing the jPipe compiler's own source."
argument-hint: "[path/to/model.jd | justifications/ | glob] [--corpus <dir>] [--no-grounding] [--apply]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Review

Syntax is the compiler's job. This reviews whether the argument *means* anything.

## Usage

```
jpipe-review <target> [--corpus <dir>] [--no-grounding] [--apply]
```

**Target**: a `.jd` file, a directory (recurse `*.jd`), a glob, or nothing (the changed `.jd` files).

**Flags**: `--corpus <dir>` widens the reuse pass when the target is a single file.
`--no-grounding` skips the repository-artifact pass. `--apply` continues into the fix loop.

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/rules.md` | any time you cite a rule id (Steps 3–7) |
| `references/abstraction.md` | Step 3, and Step 8 when writing a replacement label |
| `references/grounding.md` | Step 4 |
| `references/conventions.md` | Step 5 |
| `references/sharing.md` | Step 6 |
| `references/language.md` | whenever a fix adds, moves, or re-ids an element, or touches a label that may unify |
| `references/report-format.md` | Step 7 |

## When to invoke

Reviewing, auditing, or improving an existing `.jd`; onboarding an inherited assurance case; a
pre-merge check over a `justifications/` directory.

### Do NOT invoke for

- Writing a new model from scratch.
- Reviewing the **step library** that implements the checks (`steps/`, `@jpipe_link` modules).
- Reviewing the jPipe compiler's own source.
- Rendering a diagram. That is one command: `jpipe process -m <model> -i <f> -f SVG -o <out>.svg`.

## Guardrails

- **Read-only through Step 7.** Nothing is modified before the author approves a numbered fix list.
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

Resolve the target list. Run `jpipe --version` and record it for the report header; if `jpipe` is not
on PATH, say so and stop, because the compile gate is not optional. Identify the entry-point
model(s) and the `load` graph. Note the repository root (Step 4 needs it) and the corpus root
(Step 6 needs it).

For more than 8 files, plan to batch Steps 3–6 and emit **one** consolidated report.

### Step 2. Compile gate

Per file: `jpipe --headless diagnostic -i <file>`, capturing stdout, stderr, and the exit code
separately.

A file passes only if the exit code is `0` **and** stderr is empty. A failed `load` is fatal and
reports **entirely on stderr, leaving stdout completely empty**, not even a Diagnostics header. A
gate that reads stdout alone will call a broken file clean.

On failure: record *that* the file does not build, keep the compiler's raw output verbatim for the
report's **Not reviewed** section, and skip Steps 3–6 for that file. Do not explain, rank, or
catalogue the diagnostics.

On success: keep the `=== Symbol Table ===` block. It maps every element id to `line:col`, and it is
where the locations in your findings come from.

### Step 3. Abstraction & atomicity *(within each model)*

Assign every element its Toulmin role and check it against its jPipe kind. Classify each `evidence`
leaf as a datum, a claim in a grounds slot, or two facts fused; check each `strategy` licenses an
inference; check each `sub-conclusion` states what its leg establishes.

Resolve fused leaves **first**: atomicity is a precondition for Step 6, and a leaf flagged `A05`
blocks any reuse finding on it.

Classify each file 🟢/🟡/🟠/⚪. → `references/abstraction.md`

### Step 4. Grounding *(evidence → repository)*

For each atomic evidence leaf, extract the artifact it names, decide what kind of thing it is, and
search: `Glob` for paths, `Grep` for sections and symbols. **Record the exact searches**, because a
grounding finding must state what was looked for and where, or it is an open question instead.

Skipped under `--no-grounding`, and when the models are not inside a project tree.
→ `references/grounding.md`

### Step 5. Conventions *(across the corpus)*

First check whether the project states its own conventions (`CLAUDE.md`, `justifications/README.md`,
a contributing guide). If it does, that document wins and this pass defers to it.

Otherwise: leaves that restate another model's conclusion, refine placement, one entry point,
conclusions at goal level, orphan models, provenance headers.
→ `references/conventions.md`

### Step 6. Reuse *(across the corpus)*

Survey before reading. One `grep` harvests every `<kind> <id> is "<label>"` in the corpus with its
file and line; cluster on **the artifact each label names**, never on string similarity. Open full
files only for clusters you are about to report.

Same artifact + drifted labels → they will not unify. Identical labels + different artifacts → they
will, and that is a defect. Same leg repeated → extract it.

Needs a corpus: skip for a single-file target unless `--corpus <dir>` was given.
→ `references/sharing.md`

### Step 7. Report

Emit the report in exactly the shape of `references/report-format.md`, including the **Open
questions** and **Not reviewed** sections, which are where the review states its own limits.

**Stop here** unless `--apply` was given.

### Step 8. Propose and get approval

Present a numbered fix list. Each entry: the finding id, the exact before and after text, the blast
radius, and any fix it depends on. Order by dependency, not by severity: atomicity splits before
reuse alignment, label rewords before structural changes.

Ask in prose which numbers to apply. Never act on silence or an ambiguous answer, and never widen
beyond what was approved.

### Step 9. Apply and re-verify

`Edit` only the approved items. Then re-run the Step 2 gate on every touched file (all must pass)
and `jpipe process -m <model> -i <file> -f SVG -o <tmp>` to prove the model still renders.

If any applied fix created or destroyed a unified group, re-render the composed model and report the
new `unified_N` numbering, so the author knows what shifted.

Close with the delta: findings closed, findings remaining, anything newly introduced.

## Output contract

The report is the product. Every finding carries a rule id, a `file:line:col`, the label quoted, the
proposed replacement, and a blast-radius line. Verdicts: **CLEAN** · **FINDINGS** · **BLOCKED** (one
or more files did not compile).
