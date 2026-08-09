---
name: jpipe-survey
description: "Surveys a set of jPipe justification models (.jd) for what no single model shows: the same fact argued twice under labels that will not match, labels identical enough to merge into a claim nobody wrote, and leaves that assert what another model already proves. Scope is exactly one .jd file plus everything it transitively loads, every .jd in the repository with --global, or, with -m <model>, one model in that file plus the models it is built from. Clusters declarations by the artifact each label names rather than by wording, and asks you to confirm the uncertain ones. Emits a report written for the engineer who built the system, then a fix list; nothing is edited until you approve it. Use when asked about shared or duplicated evidence, reuse across models, merge hazards, consolidating an assurance case, whether a leaf should be a refine, or files nothing loads. NOT for judging whether one model's argument is any good, which is jpipe-review's job; NOT for writing a model from scratch; NOT for syntax errors."
argument-hint: "<path/to/model.jd> [-m <model>] [--global] [--no-refine] [--questions N]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Survey

One model at a time hides the duplication. This reads the whole scope at once.

## Usage

```
jpipe-survey <path/to/model.jd> [-m <model>] [--global] [--no-refine] [--questions N]
```

**Scope** is **exactly one `.jd` plus everything it transitively `load`s**, or every `.jd` in the
repository under `--global`. **No file, or more than one, is an error.** Every rule here compares models,
so the scope needs **two or more**: a file that loads nothing is a scope of one, and `--global` is the
invocation for a corpus not rooted in a single model.

**`-m <model>` narrows the scope to one model in that file plus the models it is built from**, following
`assemble`, `refine` and `implements` sources transitively. Pass it when a file declares more than one
root: a `load` makes a name available without making it part of your argument. → `references/scope.md`

**Flags**: `--no-refine` runs sharing only, skipping the `JD-F` pass. `--questions N` changes the
interview budget from its default of 7; `--questions 0` asks nothing and reports every uncertain cluster
as an open question.

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/scope.md` | Step 1, and Step 5 if `-m` was passed |
| `references/rules.md` | any time you cite a rule id (Steps 3–6) |
| `references/sharing.md`, then `references/artifacts.md` | Steps 2 to 4, for the `JD-R` family, and before clustering anything |
| `references/refinement.md` | Steps 3 and 5, for the `JD-F` family |
| `references/interview.md` | Step 4, before writing a single question |
| `references/language.md` | whenever a fix touches a label that may unify, or adds a `refine` |
| `references/report-format.md` | Step 5 |

## When to invoke

Auditing a corpus for duplicated or shareable evidence, consolidating one that grew a model at a time,
checking for merge hazards before composing, asking whether a leaf should refine against an existing one.

### Do NOT invoke for

- **Whether one model is a good argument** (abstraction, atomicity, grounding) is `jpipe-review`'s, which
  examines elements rather than comparing models: do not restate its findings here. Nor is writing a model
  from scratch, the **step library** (`steps/`, `@jpipe_link`), the compiler's source, or rendering.

## Guardrails

- **One scope, and it is what Step 1 resolved**: the file's closure, one model's closure under `-m`, or
  the repository under `--global`. Never cluster outside it, and never widen it to make a finding
  possible. Nothing is modified before the author approves a numbered fix list.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a pull
  request. Report; the author integrates.
- **Cluster by the artifact, never by the label.** String similarity and artifact identity come apart in
  both directions (`artifacts.md` §3), so comparing wording gets both cases backwards.
- **A wrong merge is worse than a missed one**: it collapses a distinction the author drew on purpose, and
  applied, it silently changes what the case claims. When torn ask; when you cannot ask, leave a question.
- **Ask, never guess, and ask in prose.** Artifact identity is knowledge the author has and the files do
  not record. There is no interactive question tool here on purpose: a picker cannot be answered headless,
  so an approval built on one deadlocks instead of degrading. Never act on silence or an ambiguous answer.
- **Write the report, and the questions, for the engineer who built the system.** No rule id standing in
  for an explanation, no severity words, no compiler vocabulary: *unify* names a pass they never invoke.
  Say what is wrong, why it matters to them, and what their options are. → `references/report-format.md`
- **Every label you propose is short**: under 10 words for a fact, under 15 for a check. A label is
  shared only when two files match it **exactly**, so a long canonical wording never gets typed twice.
- **Never mint a retired id** (`S01`-`S04`, `C03`, `C04`; `rules.md` translates), never open a file under
  `steps/`, and prefer an open question to a shaky finding: two false positives and they stop reading.

## Workflow

### Step 1. Inventory

Follow `load` from the named `.jd` until nothing new appears, treating a cycle as already-visited; under
`--global`, `Glob` every `*.jd` in the repository instead. Record per file the models it declares, what
it `load`s, and what each model is built from (`assemble` / `refine` sources, an `implements` template).

**That graph is what the scope resolves against**, and `references/scope.md` is the whole of how: every
model in the file closure, or under `-m` only the named model and what it is built from. **That set is
the corpus**, and the two words mean the same thing below. Its §4 holds the ways this stops instead of
guessing; a scope of one model is not one of them, but say so and say the way on.

**Do not compile anything.** A declaration clusters whether or not its file parses, so a scope caught
mid-edit is still worth surveying, and a syntax error in one model says nothing about whether two others
share a fact. Compilation belongs at Step 6; locations come from Step 2's table.

### Step 2. Survey, without opening files

One harvest over the scope's files, from `sharing.md` §1: a single `grep -rEn` for element declarations
**and** the `justification` / `template` headers above them, so every element carries the model it belongs
to and not just its `file:line`. Attribution is what enforces the boundary under `-m`, where one file can
hold a model in the closure and a model outside it. **Pass the files explicitly**, never a directory.
Everything downstream runs on this table, at a cost that does not scale with file size. Open a full file
**only** for a cluster you are about to report or ask about; reading the scope means the method failed.

### Step 3. Cluster by artifact

Resolve every `evidence` label to the thing it names (`artifacts.md`), then cluster on **that**. Sort
each cluster into certain-nothing, certain-defect (`R03`, which needs a model in scope that composes both
sides), or uncertain (`sharing.md` §3).

In the same pass, match `evidence` labels against *other* models' `conclusion` and `sub-conclusion`
labels: that lookup is `F01`, and Step 2's table already holds both sides. Skipped under `--no-refine`.
→ `references/sharing.md`, `references/refinement.md`

### Step 4. Interview

Uncertain clusters become **one batched message**: numbered prose questions, at most `--questions N`
(default 7), ordered by how many models each touches. Quote both labels, name the artifact you believe
is shared, say how confident you are, and say what a yes will cause. Clusters past the budget are **not
dropped**: they go to Open questions with their labels quoted, and the report says how many. Record every
answer, including every *no*, for **What you told me**. → `references/interview.md`

### Step 5. Report

Confirmed clusters become findings; declined ones are recorded; unanswered ones become open questions.
Add the `JD-F` findings, which need the Step 1 graph rather than the interview, except under `-m`, which
answers `F03` and `F04` by construction and so retires them (`scope.md` §6).

Emit the report in exactly the shape of `references/report-format.md`, and read that file first: the
reader is **the engineer who built the system**, and every finding owes them *what is wrong*, *why it
matters to them*, and *the options*, in that order. Keep **What you told me**, **Open questions** and
**Not looked at**, and state the standing limit: a clean survey says nothing about whether any single
model argues well.

### Step 6. Apply and verify

Present a numbered fix list in the report's voice: which finding it closes, the exact before and after
text for **every** file it touches, what it costs, and what it depends on. Order by dependency, not
severity (`rules.md`). Ask in prose which numbers to apply.

`Edit` only the approved items. Then, the one step that compiles: per touched file,
`jpipe --headless diagnostic -i <file>`, capturing stdout, stderr and the exit code **separately**, since
a failed `load` reports entirely on stderr with stdout completely empty. Then `jpipe process` to prove it
still renders, on the model `-m` named, or on the scope's root, or under `--global` on each root whose
closure a touched file belongs to. If `jpipe` is not on PATH, say so and stop **before editing**: a
cross-file edit you cannot verify is worse than a reported finding, and these edits span files. A file
that did not build before your edit still must build after it.

Any applied `R01` or `R02` creates or destroys a shared node, renumbering every later `unified_N`,
possibly including ids referenced from a step library this skill does not read. Say which changed, then
close with the delta: findings closed, remaining, newly introduced.

## Output contract

The report is the product, written for the engineer who built the system. Every finding gives them a
`file:line` on **each** side, both labels quoted, the artifact they share, what is wrong, why it matters
to them, their options with the trade-off named, and what the edit costs. The rule id goes last, as a
reference number.

One verdict, over a scope the report names: which models were compared, and under `-m` which of the
file's models were not. **CLEAN** means these models share what they should and merge nothing they should
not. It says nothing about whether any one of them argues well, nor about whether they compile.
