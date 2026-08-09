---
name: jpipe-survey
description: "Surveys a set of jPipe justification models (.jd) for what no single model shows: the same fact argued twice under labels that will not match, labels identical enough to merge into a claim nobody wrote, and leaves that assert what another model already proves. Scope is exactly one .jd file plus everything it transitively loads, or every .jd in the repository with --global. Harvests every declaration in one pass, clusters them by the artifact each label names rather than by wording, and asks you to confirm the uncertain clusters before reporting them. Emits a report written for the engineer who built the system, then a fix list; nothing is edited until you approve it. Use when asked about shared or duplicated evidence, reuse across models, merge hazards, consolidating an assurance case, whether a leaf should be a refine, or files nothing loads. NOT for judging whether one model's argument is any good, which is jpipe-review's job; NOT for writing a model from scratch; NOT for syntax errors."
argument-hint: "<path/to/model.jd> [--global] [--no-refine] [--questions N]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Survey

One model at a time hides the duplication. This reads the whole scope at once.

## Usage

```
jpipe-survey <path/to/model.jd> [--global] [--no-refine] [--questions N]
```

**Scope** is **exactly one `.jd` plus everything it transitively `load`s**, or every `.jd` in the
repository under `--global`. **No file, or more than one, is an error.** Every rule here compares models,
so the scope needs **two or more**: a file that loads nothing is a scope of one, and `--global` is the
invocation for a corpus not rooted in a single model.

**Flags**: `--no-refine` runs sharing only, skipping the `JD-F` pass. `--questions N` changes the
interview budget from its default of 7; `--questions 0` asks nothing and reports every uncertain cluster
as an open question.

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/rules.md` | any time you cite a rule id (Steps 3–6) |
| `references/artifacts.md` | Step 3, before clustering anything |
| `references/sharing.md` | Steps 3 and 4, for the `JD-R` family |
| `references/refinement.md` | Steps 3 and 5, for the `JD-F` family |
| `references/interview.md` | Step 4, before writing a single question |
| `references/language.md` | whenever a fix touches a label that may unify, or adds a `refine` |
| `references/report-format.md` | Step 5 |

## When to invoke

Auditing a corpus for duplicated or shareable evidence; consolidating one that grew a model at a time;
checking for merge hazards before composing; asking whether a leaf should refine against an argument
that already exists.

### Do NOT invoke for

- **Whether one model is a good argument.** Abstraction, atomicity, grounding: `jpipe-review`, which
  examines elements rather than comparing models. Do not restate its findings here.
- Writing a new model from scratch, reviewing the **step library** (`steps/`, `@jpipe_link` modules) or
  the jPipe compiler's source, or rendering a diagram (`jpipe process -m <model> -i <f> -f SVG`).

## Guardrails

- **One scope, and it is the closure**: the named file and all it transitively `load`s, or every `.jd`
  under `--global`. Never read or cluster outside it, and never widen it to make a finding possible.
  Nothing is modified before the author approves a numbered fix list.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a pull
  request. Report; the author integrates.
- **Cluster by the artifact, never by the label.** String similarity and artifact identity come apart in
  both directions (`artifacts.md` §3), so comparing wording gets both cases backwards.
- **A wrong merge is worse than a missed one**: it collapses a distinction the author drew on purpose, and
  applied, it silently changes what the case claims. When torn, ask; when you cannot ask, leave a
  question.
- **Ask, never guess, and ask in prose.** Artifact identity is knowledge the author has and the files do
  not record. There is no interactive question tool here on purpose: a picker cannot be answered headless,
  and an approval step built on one deadlocks instead of degrading. Never act on silence or on an
  ambiguous answer, and never widen beyond what was approved.
- **Write the report, and the questions, for the engineer who built the system.** No rule id standing in
  for an explanation, no severity words, no compiler vocabulary: *unify* names a pass they never invoke.
  Say what is wrong, why it matters to them, and what their options are. → `references/report-format.md`
- **Every label you propose is short**: under 10 words for a fact, under 15 for a check. It matters most
  here, because a label is shared only when two files match it **exactly**, so a long canonical wording
  is a merge that quietly never happens.
- **Never mint a retired id** (`S01`-`S04`, `C03`, `C04`; `rules.md` translates), never open a file under
  `steps/`, and prefer an open question to a shaky finding: two false positives and the author stops
  reading.

## Workflow

### Step 1. Inventory

Resolve the scope: from the named `.jd`, follow `load` declarations until nothing new appears, treating a
cycle as already-visited; under `--global`, `Glob` every `*.jd` in the repository instead. **That set is
the corpus**, and the two words mean the same thing below. No file or more than one: say which and stop.
A scope of one model: say so and suggest `--global`.

Per file, record the models it declares, what it `load`s, and whether it is an operator result
(`is assemble(...)` / `is refine(...)`) and over which sources. `F03` and `F04` rest on that graph, and
it is complete only for the scope, so say so when reporting them. → `references/refinement.md`

**Do not compile anything.** A declaration clusters whether or not its file parses, so a scope caught
mid-edit is still worth surveying, and a syntax error in one model says nothing about whether two others
share a fact. Compilation belongs at Step 6. Locations come from Step 2's table, which carries a line
number per declaration.

### Step 2. Survey, without opening files

One harvest over the scope, from `sharing.md` §1: a single `grep -rEn` for `<kind> <id> is "<label>"`,
yielding `file:line: kind id is "label"` for every element. **Pass the scope's files explicitly**, never
a directory, so the harvest cannot reach past the boundary Step 1 drew. Cost does not scale with file
size, and everything downstream runs on this table. Open a full file **only** for a cluster you are about
to ask about or report; if you find yourself reading the scope, the method has already failed.

### Step 3. Cluster by artifact

Resolve every `evidence` label to the thing it names (`artifacts.md`), then cluster on **that**. Sort
each cluster into certain-nothing, certain-defect (`R03`), or uncertain (`sharing.md` §3).

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
Add the `JD-F` findings, which need the Step 1 graph rather than the interview.

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
a failed `load` reports entirely on stderr with stdout completely empty. Then `jpipe process` on the
scope's root to prove it still renders, or, under `--global` where there is no single root, on each root
whose closure a touched file belongs to. If `jpipe` is not on PATH, say so and stop **before editing**: a
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

One verdict for the scope, **CLEAN** or **FINDINGS**. CLEAN means these models share what they should
and merge nothing they should not. It says nothing about whether any one of them argues well, nor about
whether they compile.
