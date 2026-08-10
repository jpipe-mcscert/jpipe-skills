---
name: jpipe-review
description: "Reviews the argument in an existing jPipe justification model (.jd). Takes exactly one .jd file as its scope, plus everything it transitively loads, since an argument spread over several files is still one argument; pass -m <model> to narrow that to one model in the file plus the models it is built from. Checks abstraction (each element at its right level), atomicity (one element, one job), grounding (the artifacts the evidence names exist in the repository), and the house style. Emits a findings report written for the engineer who built the system, then a fix list; nothing is edited until you approve it. Syntax errors are left to `jpipe diagnostic`. Use when asked to review, audit, critique or improve a .jd file or an assurance case; pass --global for every .jd in the repository instead. NOT for cross-model reuse, shared evidence or corpus consolidation, which is jpipe-survey's job; NOT for writing a model from scratch; NOT for reviewing the jpipe-runner step library or the jPipe compiler's own source."
argument-hint: "<path/to/model.jd> [-m <model>] [--global] [--no-grounding]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Review

Syntax is the compiler's job. This reviews whether the argument *means* anything.

## Usage

```
jpipe-review <path/to/model.jd> [-m <model>] [--global] [--no-grounding]
```

**Scope** is **exactly one `.jd` plus everything it transitively `load`s**: a model composed from four
requirement files is one argument, not four, so findings may land in any file of that closure. **No
file, or more than one, is an error**: say which and stop rather than guessing at a default.

**Flags**: `-m <model>` narrows the scope to one model in that file plus the models it is built from,
which is what a file declaring more than one root needs: a `load` makes a name available without making
it part of your argument. `--global` widens it to **every** `.jd` in the repository, each element
examined once, and contradicts `-m`. `--no-grounding` skips the repository-artifact pass.

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/scope.md` | Step 1, and Step 5 if `-m` was passed |
| `references/rules.md` | any time you cite a rule id (Steps 2–5) |
| `references/abstraction.md` | Step 2, and Step 6 when writing a replacement label |
| `references/grounding.md`, then `references/artifacts.md` | Step 3 |
| `references/conventions.md` | Step 4 |
| `references/language.md` | whenever a fix adds, moves, or re-ids an element, or touches a label that may unify |
| `references/report-format.md` | Step 5 |

## When to invoke

Reviewing, auditing or improving a `.jd`; onboarding an inherited assurance case; a pre-merge check.

### Do NOT invoke for

- **Cross-model questions**: is this fact argued twice elsewhere, will these two labels merge, does
  anything load this model. Those compare models rather than examine one, so they are `jpipe-survey`'s.
- Writing a model from scratch, the **step library** (`steps/`, `@jpipe_link`), the compiler's own
  source, or rendering a diagram (`jpipe process -m <model> -i <f> -f SVG -o <out>.svg`).

## Guardrails

- **One scope, and it is what Step 1 resolved.** The file's closure, one model's closure under `-m`, or
  the repository under `--global`: everything in it reviewable, nothing outside it readable. Never widen
  it, and never narrow it either, since skipping part of it leaves part of the argument unexamined.
- **Still one argument, not many.** Findings say what is wrong with an element, never how two models
  compare. Seeing two files does not make comparing them this skill's job; that is `jpipe-survey`'s.
- **Read-only until approval.** Nothing is modified before the author approves a numbered fix list.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a
  pull request. Report; the author integrates.
- **Never re-report what the compiler already said**, and never open a file under `steps/` or any
  `@jpipe_link` module: out of scope, and its contents can never be a finding.
- **Write the report for the engineer who built the system.** No Toulmin vocabulary, no severity
  words, no rule id doing an explanation's work. → `references/report-format.md`
- **Never silently re-id or renumber**, and **keep every label you propose short**: under 10 words for a
  fact, under 15 for a check. Labels are diagram node text, and `assemble` unification is exact string
  equality and positional, so a one-line label edit can shift every downstream `unified_N`.
  → `references/abstraction.md` §3b
- **Prefer an open question to a shaky finding.** Two false positives and the author stops reading.

## Workflow

### Step 1. Scope

Resolve the scope, and `references/scope.md` is the whole of how: follow `load` from the named `.jd`
until nothing new appears, treating a cycle as already-visited rather than an error. That set of models
is the review, and all of it is reviewable. `-m` narrows it to the named model and what it is built
from, which is the flag for a file declaring two roots; `--global` widens it to every `.jd` in the
repository, each element examined once, so a requirement file pulled in by three goals is reviewed once
rather than three times. Its §4 holds the ways this stops instead of guessing.

Note the repository root (Step 3). **Do not compile anything yet**: an argument's shape is legible long
before it parses, the author already knows whether the file builds, and compilation belongs at Step 7
where it verifies work this skill did. Locations come from the file as read, `file:line`. For a scope
over 8 files, batch Steps 2 to 4 and emit **one** report, still one verdict per model.

### Step 2. Roles and atomicity *(per element)*

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

Emit the report in exactly the shape of `references/report-format.md`, and read that file first: the
reader is **the engineer who built the system**, and every finding owes them *what is wrong*, *why it
matters to them*, and *the options*, in that order. No Toulmin vocabulary, no severity words, no rule id
doing an explanation's work; ids appear once per finding, at the end, as a reference number.

Keep **Open questions** and **Not looked at**: they state the review's limits, and the scope is one, so
name the models reviewed and, under `-m`, the file's models that were not (`scope.md` §7).

### Step 6. Propose and get approval

Present a numbered fix list in the report's voice, not the catalogue's. Each entry: which finding it
closes, the exact before and after text, what it costs, and any fix it depends on. Order by dependency,
not severity (`rules.md`): decompositions first, then rewords, then structure. Ask in prose which
numbers to apply, never act on silence or an ambiguous answer, and never widen beyond what was approved.
Every edit lands inside the scope; a fix needing a file outside it is reported, not made.

### Step 7. Apply and verify

The one step that compiles. `Edit` only the approved items, then per touched file:
`jpipe --headless diagnostic -i <file>`, capturing stdout, stderr and the exit code **separately**. A
file passes only if the exit code is `0` **and** stderr is empty: a failed `load` reports entirely on
stderr, leaving stdout completely empty, so a check reading stdout alone calls a broken file clean.
Then `jpipe process -m <model> -i <file> -f SVG -o <tmp>` to prove it still renders.

If `jpipe` is not on PATH, say so and stop **before editing**: an unverifiable edit to an assurance case
is worse than a reported finding. Everything through Step 6 runs without the compiler. A file that did
not build before your edit still must build after it; if it did not compile going in, say so rather than
claiming the edit broke it.

If an applied fix creates, destroys or renames a unified group, re-render the composed model and report
the new `unified_N` numbering. That model is usually **in** the scope, being the file that loads the
rest, and under `-m` it is the one you were handed. Close with the delta: closed, remaining, new.

## Output contract

The report is the product, written for the engineer who built the system. Every finding gives them a
`file:line`, the label quoted, what is wrong, why it matters to them, their options with the trade-off
named, and what the edit costs. The rule id goes last, as a reference number.

One verdict, **CLEAN** or **FINDINGS**, over a scope the report names: the models reviewed, per-file
counts beneath, and under `-m` the file's models that were not. CLEAN means this argument holds on its
own terms, and says nothing about models outside the scope, nor about whether the files compile.
