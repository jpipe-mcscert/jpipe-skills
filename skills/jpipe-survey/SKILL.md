---
name: jpipe-survey
description: "Surveys a corpus of jPipe justification models (.jd) for what no single file shows: the same fact argued twice under labels that will not unify, labels identical enough to merge into a claim nobody wrote, and leaves that assert what another model already proves. Harvests every .jd's element declarations in one pass, clusters them by the artifact each label names rather than by wording, and asks you to confirm the uncertain clusters. Emits a report with file:line, rule ids and a decision log; edits are applied only after you approve them. Use when asked about shared or duplicated evidence, reuse across models, unification hazards, consolidating an assurance case, whether a leaf should be a refine, or orphan models and entry points in a justifications/ directory. NOT for judging whether one model's argument is any good (its abstraction, atomicity, or whether its artifacts exist), which is jpipe-review's job; NOT for writing a model from scratch; NOT for syntax errors, which are jpipe diagnostic's."
argument-hint: "[justifications/ | glob | .] [--no-refine] [--questions N] [--apply]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Survey

One model at a time hides the duplication. This reads the whole corpus at once.

## Usage

```
jpipe-survey <target> [--no-refine] [--questions N] [--apply]
```

**Target**: a directory (recurse `*.jd`), a glob, or nothing (the repository root). Needs **two or
more** models: with one, say so and stop, because every rule here compares models.

**Flags**: `--no-refine` runs sharing only, skipping the `JD-F` pass. `--questions N` changes the
interview budget from its default of 7; `--questions 0` asks nothing and reports every uncertain
cluster as an open question. `--apply` continues into the fix loop.

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/rules.md` | any time you cite a rule id (Steps 4–7) |
| `references/artifacts.md` | Step 4, before clustering anything |
| `references/sharing.md` | Steps 4 and 5, for the `JD-R` family |
| `references/refinement.md` | Steps 4 and 6, for the `JD-F` family |
| `references/interview.md` | Step 5, before writing a single question |
| `references/language.md` | whenever a fix touches a label that may unify, or adds a `refine` |
| `references/report-format.md` | Step 6 |

## When to invoke

Auditing a `justifications/` directory for duplicated or shareable evidence; consolidating a corpus
that grew a model at a time; checking a corpus for unification hazards before composing it; asking
whether a leaf should refine against an argument that already exists.

### Do NOT invoke for

- **Whether one model is a good argument.** Abstraction, atomicity, grounding: `jpipe-review`, which
  reads one model properly rather than glancing at many. Do not restate its findings here.
- Writing a new model from scratch.
- Reviewing the **step library** (`steps/`, `@jpipe_link` modules) or the jPipe compiler's source.
- Rendering a diagram: `jpipe process -m <model> -i <f> -f SVG -o <out>.svg`.

## Guardrails

- **Read-only through Step 6.** Nothing is modified before the author approves a numbered fix list.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a pull
  request. Report; the author integrates.
- **Cluster by the artifact, never by the label.** String similarity and artifact identity come apart
  in both directions (`artifacts.md` §3). A method that compares wording gets both cases backwards.
- **A wrong merge is worse than a missed one.** It collapses a distinction the author drew on purpose,
  and if applied it silently changes what the case claims. When torn, ask; when you cannot ask, leave
  an open question.
- **Ask, never guess, and ask in prose.** Artifact identity is knowledge the author has and the corpus
  does not record. There is no interactive question tool here on purpose: a picker cannot be answered
  headless, and an approval step built on one deadlocks instead of degrading.
- **Never act on silence** or on an ambiguous answer, and never widen beyond what was approved.
- **Never mint a retired id.** The `S01`-`S04`, `C03` and `C04` ids are burned; `rules.md` has the
  translation table.
- **Never open a file under `steps/`** or any `@jpipe_link` module. Out of scope, and its contents can
  never be a finding.
- **Prefer an open question to a shaky finding.** Two false positives and the author stops reading.

## Workflow

### Step 1. Inventory

`Glob` every `*.jd` under the target. For each, record the model names it declares, the files it
`load`s, and whether it is an operator result (`is assemble(...)` / `is refine(...)`) and over which
sources. That graph is what Step 6 needs for `F03` and `F04`, and it is cheap to build now.

Run `jpipe --version` and record it for the report header; if `jpipe` is not on PATH, say so and stop,
because the compile gate is not optional. Note the repository root.

Fewer than two models: stop and say why.

### Step 2. Compile gate

Per file: `jpipe --headless diagnostic -i <file>`, capturing stdout, stderr and the exit code
separately.

A file passes only if the exit code is `0` **and** stderr is empty. A failed `load` is fatal and reports
**entirely on stderr, leaving stdout completely empty**, not even a Diagnostics header. A gate that
reads stdout alone will call a broken file clean.

A file that does not build is excluded from every cluster and listed under **Not reviewed**, verbatim.
Never re-explain the compiler's diagnostics. Do not stop the survey: the rest of the corpus is still
worth surveying, and say in the report which models were missing from it.

### Step 3. Survey, without opening files

One harvest over the whole corpus, from `sharing.md` §1: a single `grep -rEn` for
`<kind> <id> is "<label>"`, yielding `file:line: kind id is "label"` for every element. Cost does not
scale with file size, and everything downstream runs on this table.

Open a full file **only** for a cluster you are about to ask about or report. If you find yourself
reading the corpus, the method has already failed.

### Step 4. Cluster by artifact

Resolve every `evidence` label to the thing it names (`artifacts.md`), then cluster on **that**. Sort
each cluster into certain-nothing, certain-defect (`R03`), or uncertain (`sharing.md` §3).

In the same pass, match `evidence` labels against the `conclusion` and `sub-conclusion` labels of
*other* models: that lookup is `F01`, and the table from Step 3 already holds both sides. Skipped under
`--no-refine`. → `references/sharing.md`, `references/refinement.md`

### Step 5. Interview

Uncertain clusters become **one batched message**: numbered prose questions, at most `--questions N`
(default 7), ordered by how many models each touches. Quote both labels in full, name the artifact you
believe is shared, say how confident you are, and say what a yes will cause.

Clusters past the budget are **not dropped**: they go to Open questions with their labels quoted, and
the report says how many. Record every answer, including every *no*, for the report's Decisions section.
→ `references/interview.md`

### Step 6. Report

Confirmed clusters become findings; declined ones become Decisions entries; unanswered ones become open
questions. Add the `JD-F` findings, which need the Step 1 graph rather than the interview.

Emit the report in exactly the shape of `references/report-format.md`, including **Decisions**, **Open
questions** and **Not reviewed**. State the standing limit: a clean survey says nothing about whether
any single model is a good argument.

**Stop here** unless `--apply` was given.

### Step 7. Apply and re-verify

Present a numbered fix list, each entry with its rule description, the exact before and after text for
**every** file it touches, the blast radius, and any fix it depends on. Order by dependency, not
severity (`rules.md`). Ask in prose which numbers to apply.

`Edit` only the approved items. Then re-run the Step 2 gate on every touched file, and
`jpipe process -m <model> -i <file> -f SVG -o <tmp>` on the composed model if the target has one.

Any applied `R01` or `R02` **creates or destroys a unified group**, which renumbers every later
`unified_N`, possibly including ids referenced from a step library this skill does not read. Say which
groups changed. Close with the delta: findings closed, findings remaining, anything newly introduced.

## Output contract

The report is the product. Every finding carries a rule id **and that rule's description quoted from
`rules.md`**, a `file:line:col` for every element involved, the named shared artifact, both labels
quoted, the proposed replacement, and a blast-radius line.

Verdicts, for the corpus: **CLEAN** · **FINDINGS** · **PARTIAL** (one or more files did not compile).
CLEAN means these models share what they should and merge nothing they should not. It says nothing
about whether any one of them argues well.
