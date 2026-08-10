---
name: jpipe-survey
description: "Surveys jPipe justification models (.jd) by what their elements mean, not how their labels read. Finds one claim written two ways; a leaf covering two things where splitting one out would match another model's; a bare leaf some model here would prove with refine; one claim written as a check in one model and a fact in another; and labels that disagree about when their artifact exists. Never searches the tree, so a git-ignored or run-produced file is never called missing. Scope is one .jd plus everything it loads, one model in it with -m, or the repository with --global. Reports every candidate ranked by impact with a confidence and blast radius, asks nothing up front, and edits nothing until you approve a fix list. Use when asked about duplicated or shareable evidence, reuse across models, merge hazards, consolidating an assurance case, or whether a leaf should be a refine. NOT for judging one model's argument on its own, which is jpipe-review's; NOT for writing a model from scratch; NOT for syntax errors."
argument-hint: "<path/to/model.jd> [-m <model>] [--global]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# jPipe Survey

One model at a time hides the duplication. This reads the whole scope at once, and compares meanings.

## Usage

```
jpipe-survey <path/to/model.jd> [-m <model>] [--global]
```

**Scope** is **exactly one `.jd` plus everything it transitively `load`s**, or every `.jd` in the repository
under `--global`. **No file, or more than one, is an error.** Every rule here compares two elements in
different models, so the scope needs **two or more**: a file that loads nothing is a scope of one, and
`--global` is the invocation for a corpus not rooted in a single model.

**`-m <model>` narrows the scope to one model in that file plus the models it is built from**, following
`assemble`, `refine` and `implements` sources transitively. Pass it when a file declares more than one root:
a `load` makes a name available without making it part of your argument. → `references/scope.md`

**References**: read on demand, not up front:

| Read | When |
|---|---|
| `references/semantics.md`, then `references/artifacts.md` | Steps 3 and 4. **The method**, read before comparing anything |
| `references/scope.md` | Step 1, and Step 6 if `-m` was passed |
| `references/rules.md` | any time you cite a rule id (Steps 4 to 7) |
| `references/lifecycle.md` | Step 4, for `JD-N`, and before writing a word about a file |
| `references/prove.md`, then `references/topology.md` | Step 4, for `JD-P` and `JD-T` |
| `references/language.md` | whenever a fix touches a label that may unify, or adds a `refine` |
| `references/report-format.md` | Step 6 |

## When to invoke

Auditing a corpus for duplicated or shareable evidence, consolidating one that grew a model at a time,
checking merge hazards before composing, asking whether a leaf should refine against a model that exists.

### Do NOT invoke for

- **Whether one model is a good argument** (abstraction, atomicity, grounding) is `jpipe-review`'s, which
  examines elements rather than comparing them: do not restate its findings here. Nor is writing a model
  from scratch, the **step library** (`steps/`, `@jpipe_link`), the compiler's source, or rendering.

## Guardrails

- **One scope, and it is what Step 1 resolved**: the file's closure, one model's closure under `-m`, or the
  repository under `--global`. Never compare outside it, and never widen it to make a finding possible.
  Nothing is modified before the author approves a numbered fix list.
- **Never search the tree for an artifact a label names.** Not to confirm a finding, not to raise
  confidence, not once. A case may be discharged at design time or from CI, so an absent file may be
  git-ignored or may not exist until a run makes it. `Glob` is for enumerating `.jd` under `--global` and
  `Grep` for the label harvest; neither is ever pointed at an artifact. → `references/lifecycle.md` §2
- **Compare subject and assertion, never the label.** String similarity and meaning come apart in both
  directions (`artifacts.md` §3), so ranking by wording gets both cases backwards.
- **A wrong merge is worse than a missed one**: it collapses a distinction the author drew on purpose, and
  applied, it silently changes what the case claims. So **nothing is asked before the report**, and instead
  every candidate carries its confidence and the reading behind it; on low confidence, propose no edit.
- **No version-control actions, ever.** Do not stage, commit, push, branch, merge, tag, or open a pull
  request. Report; the author integrates.
- **Write the report for the engineer who built the system.** No rule id standing in for an explanation, no
  severity words, no compiler vocabulary: *unify* names a pass they never invoke, and *comb-shaped* and
  *lifecycle* are ours rather than theirs. → `references/report-format.md`
- **Never report what one model shows.** A fused leaf with no partner, a check that cannot fail, a leaf
  naming nothing: `jpipe-review`'s. Every rule here next to one of its rules is separated by a hard
  condition (`rules.md`).
- **Every label you propose is short**: under 10 words for a fact, under 15 for a check. A label is shared
  only when two files match it **exactly**, so a long canonical wording never gets typed twice.
- **Never mint a retired id** (`rules.md` lists the twelve and translates them), nor open `steps/`.

## Workflow

### Step 1. Inventory

Follow `load` from the named `.jd` until nothing new appears, treating a cycle as already-visited; under
`--global`, `Glob` every `*.jd` in the repository instead. Record per file the models it declares, what it
`load`s, and what each model is built from (`assemble` / `refine` sources, an `implements` template).

**That graph is what the scope resolves against**, and `references/scope.md` is the whole of how: every
model in the file closure, or under `-m` only the named model and what it is built from. Its §4 holds the
ways this stops instead of guessing; a scope of one model is not one of them, but say so and say the way on.

**Do not compile anything.** An element is comparable whether or not its file parses, so a scope caught
mid-edit is still worth surveying. Compilation belongs at Step 7, where it verifies work this skill did.

### Step 2. Harvest, without opening files

One `grep -rEn` over the scope's files for element declarations **and** the `justification` / `template`
headers above them, so every element carries the model it belongs to and not only its `file:line`
(`semantics.md` §2 has the pattern). Attribution is what enforces the boundary under `-m`, where one file can
hold a model in the closure and a model outside it. **Pass the files explicitly**, never a directory.
Everything downstream runs on this table, at a cost that does not scale with file size.

### Step 3. Read every element as a proposition

Split each label into **subject** and **assertion**, for all four kinds rather than leaves alone. For
`evidence` the subject is the artifact and `artifacts.md` §1 is the extraction; also record which of its six
kinds the label implies, since that is a claim about **when** the thing exists. Then bucket by subject.

Open a full file only where a candidate needs the surrounding argument to judge. Count the single-element
buckets: they were never compared, and the report says how many. → `references/semantics.md` §1, §2, §3b

### Step 4. Classify the pairs

Within each bucket apply the five tests **in order**, stopping at the first that fires: fused, mislevelled,
same, establishes, untimed. The order is load-bearing, since a fused label cannot be merged and a kind
mismatch changes what a match means. Give every candidate a confidence and the reason for it.

Then the two passes needing the graph rather than a bucket: `JD-N`'s check across each composed model's
leaves, and `JD-T`, which does not run under `-m`. → `semantics.md` §3-§4, then the three family files

### Step 5. Rank

Order by **impact**: models touched, duplicated checks removed, depth added. Confidence breaks ties, and
severity does not enter it, since a lone 🔴 is often a two-label edit while a 🟠 restructuring three goals is
the real work. Per candidate, settle the blast radius: files, whether a shared node appears or disappears and
so whether later `unified_N` ids shift, and what recompiles.

### Step 6. Report

Emit the report in exactly the shape of `references/report-format.md`, and read it first: the reader is **the
engineer who built the system**, and every finding owes them *what is wrong*, *why it matters to them*, *the
options*, then confidence and impact. Lead with **Worth your time, in order**; keep **Worth a look** for
low-confidence candidates and **Not looked at** for the limits, the single-element buckets, the models `-m`
excluded and the unsearched tree among them.

### Step 7. Apply and verify

Present a numbered fix list in the report's voice: which finding it closes, the exact before and after text
for **every** file it touches, what it costs, and what it depends on. Order by dependency, not impact
(`rules.md`), and never propose an `L01`, which is handed to `jpipe-review`. Ask in prose which numbers to
apply, and record every choice, the declines included, under **What you decided**.

`Edit` only the approved items. Then the one step that compiles: per touched file,
`jpipe --headless diagnostic -i <file>`, capturing stdout, stderr and the exit code **separately**, since a
failed `load` reports entirely on stderr with stdout completely empty. Then `jpipe process` to prove it still
renders, on the model `-m` named, or the scope's root, or each affected root under `--global`. If `jpipe` is
not on PATH, say so and stop **before editing**: these edits span files, and one you cannot verify is worse
than a finding you merely reported. A file that did not build before your edit still must build after it.

Any applied merge or split creates or destroys a shared node, renumbering every later `unified_N`, possibly
including ids referenced from a step library this skill does not read. Say which changed, then close with the
delta: findings closed, remaining, newly introduced.

## Output contract

The report is the product, written for the engineer who built the system, and it opens with the findings
ranked by what they are worth. Every finding gives them a `file:line` and a quoted label on **each** side,
what is wrong, why it matters, the options, the confidence and its reason, what the edit touches, and last of
all the rule id, as a reference number.

One verdict, over a scope the report names: which models were compared, and under `-m` which were not.
**CLEAN** means these models say different things and merge nothing they should not. It says nothing about
whether any one of them argues well, whether the files compile, or whether anything they name exists.
