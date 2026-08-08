# Grounding: does the repository contain what the evidence names?

**Authority: `argument`.** An evidence leaf claims a fact exists. If nothing in the tree corresponds
to it, the argument rests on nothing, no matter how well-formed the model is.

Read this at Step 4. Skip the pass entirely under `--no-grounding`, or when the models are not inside
a project tree (a standalone `.jd` has nothing to ground against, and that is not a defect).

---

## The discipline, first

This pass is the one most likely to produce garbage, so the rule comes before the method:

> **A grounding finding must name what was searched for and where it was searched.**
> If you cannot state the search you ran, you do not have a finding. You have an open question.

A reviewer that cries wolf on a correct model is worse than no reviewer. Authors stop reading after
the second false positive, and the real findings go down with them. When torn, choose the open
question: it costs the author ten seconds and costs you nothing.

Three hard limits:

- **Never report against a file you declined to open.** The step library (`steps/`, any
  `@jpipe_link` module) is out of scope; its absence or contents can never be a finding.
- **Never report outside the repository root.** Evidence may legitimately name a thing that lives
  elsewhere: a hosted dashboard, a standards document, a third-party dataset. Absence from *this*
  tree says nothing about it.
- **Never report on a leaf you flagged `A05` (non-atomic).** Split it first; then ground the parts.
  A fused leaf has no single artifact to look for.

---

## Method

### 1. Extract the artifact

Read the label and ask what thing it names. Labels are prose written for a human, so the artifact is
usually a noun phrase with a possessive or a qualifier:

| Label | Artifact |
|---|---|
| "The committed Pipfile and its `[packages]` dependency table" | `Pipfile`, section `[packages]` |
| "The committed pipeline source: the `src/` package and the `run_v*.py` entry points" | `src/`, `run_v*.py` |
| "The committed train, test and counterfactual CSV splits and their header rows" | `data/*.csv` (three of them) |
| "The CI run record for the release commit and its coverage job log" | a CI artifact, **likely not in the tree** |
| "The fitted classifier" | a *produced* thing, not a committed one |

### 2. Classify what kind of thing it is

This decides the search, and it decides what absence means.

- **Committed path**: a file or directory expected in the tree. `Glob` for it.
- **Path with an internal section**: a file plus a named part (`[packages]`, a heading, a symbol).
  `Glob` for the file, then `Grep` inside it for the section.
- **Named symbol**: a function, class, or config key. `Grep` the tree.
- **Produced artifact**: something a run creates (`model/metrics.json`, a fitted pipeline). It may
  be git-ignored and legitimately absent from a clean checkout. Ground against **what produces it**,
  and if that is ambiguous, it is an open question, not a finding.
- **External**: a hosted record, a published standard, a third-party dataset. **Out of reach.** Not
  a finding in either direction.

### 3. Search, and record the searches

Run the searches. Keep the exact patterns, because they go in the report. A finding that says "not
found" without saying what was looked for is unactionable and unverifiable.

### 4. Classify the outcome

| Outcome | Meaning | Report as |
|---|---|---|
| **found** | a clear correspondence | nothing; silence is the success case |
| **absent** | a concrete token was searched for and nothing plausible exists | `G01 artifact-absent` |
| **stale** | nothing matches, but a near-match exists under a different name | `G02 artifact-stale` |
| **uncertain** | the label does not resolve to a searchable token, or too many candidates match | an **open question** |
| **unnameable** | the leaf names no inspectable thing at all | `G03 no-artifact-named` |
| **mismatched** | the artifact exists, but the strategy's check cannot be performed against it | `G04 check-not-performable` |

`G02` is the highest-value finding in this pass. A renamed file leaves an argument that still
compiles, still renders, and is quietly false: exactly the failure an assurance case exists to
prevent.

---

## Worked examples

### found: say nothing

```text
r9.jd:12  evidence e_pipfile is "The committed Pipfile and its [packages] dependency table"

  Glob  Pipfile              → Pipfile
  Grep  "\[packages\]"       → Pipfile:14
  → found. No finding.
```

### G02 stale: the valuable one

```text
r3.jd:9   evidence e_split is "The committed data/dev.csv split and its header row"

  Glob  data/dev.csv         → (none)
  Glob  **/dev.csv           → (none)
  Glob  data/*.csv           → data/train.csv, data/test.csv, data/counterfactual.csv
  → G02. Three splits exist; none is named dev. Likely a rename the label missed.
     Report the candidates; do not guess which was meant.
```

### open question: not a finding

```text
r7.jd:11  evidence e_model is "The fitted classifier"

  Produced artifact, not committed. Glob model/ → (git-ignored, empty in a clean checkout)
  Produced by: run_v2.py → ModelStore().load(...)
  → The producer exists, so the fact is reachable. NOT G01.
     Open question: "e_model names a produced artifact rather than a committed one.
     Grounding it depends on a run having happened. Intentional?"
```

### G03: nothing inspectable at all

```text
r11.jd:8  evidence e_qual is "The approach is methodologically sound"

  No artifact, no path, no symbol. Nothing to search for.
  → G03. Nobody, human or machine, can check this leaf.
     Usually co-occurs with A01 or A06; fix the abstraction first and this often resolves itself.
```

### G04: right artifact, wrong check

```text
r14.jd:12 evidence e_cfg    is "The committed pipeline configuration file"
r14.jd:10 strategy s_thresh is "Confront the measured accuracy with the 0.8 threshold"

  Glob config.yaml → config.yaml    (the artifact is there)
  Grep accuracy    → no match in config.yaml
  → G04. The warrant checks a measurement; the ground offers a configuration.
     The leg needs the metrics artifact, or the warrant needs to be about configuration.
```

---

## Report shape

Every grounding finding carries the searches. Minimum:

```text
**U1 · `[JD-G02 artifact-stale]` · requirements/r3.jd:9:19 · `evidence e_split`**
Leaf names *"the data/dev.csv split"*.
Searched: `data/dev.csv`, `**/dev.csv`. No match.
Nearest: `data/train.csv`, `data/test.csv`, `data/counterfactual.csv`.
→ Likely a stale label from a rename. Confirm which split is meant; the fix is label-only.
```

Severity: `G01`, `G02` and `G04` are 🔴 **UNSOUND**: the argument rests on something that is not
there, or is not what the check needs. `G03` is 🟠 **ABSTRACTION**, because the real problem is that
the leaf was never a fact.
