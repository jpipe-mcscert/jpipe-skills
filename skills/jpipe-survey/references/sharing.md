# Sharing: the same fact, argued twice

**Authority: `house`, except `R03` which is `language`.** Findings here are opportunities the author
may decline, with one exception that is a genuine defect.

Read this at Steps 4 and 5.

---

## Why this matters in jPipe specifically

In most argumentation notations, "these two arguments rest on the same fact" is an observation with no
mechanical consequence. In jPipe it has one.

After any operator runs, the compiler merges result elements with **byte-identical labels** into a
single `unified_N` node (`language.md` §7). Two goals that ground on the same artifact, worded
identically, become one node: the fact is stated once, the check runs once, and the diagram shows the
sharing. Worded differently, by one article or one trailing period, they stay two nodes and the same
work is done twice.

Sharing is therefore not a style preference. It is something a corpus either achieves or misses, and
the difference is invisible in any single file, which is why no amount of careful per-model review
finds it.

---

## Method

### 1. Survey labels without opening files

Never read a corpus to find duplicates. Harvest the declarations and cluster those:

```bash
grep -rEn '^[[:space:]]*(evidence|sub-conclusion|strategy|conclusion)[[:space:]]+[A-Za-z_][A-Za-z0-9_:]*[[:space:]]+is[[:space:]]+' <corpus> --include='*.jd'
```

That yields `file:line: kind id is "label"` for every element, at a cost that does not scale with file
size. Everything in this pass runs on that table. Open full files **only** for clusters you are about
to report or ask about.

### 2. Cluster by the artifact, not by the string

→ `artifacts.md`, which is the shared extraction and states the trap in full. The one-line version:
string similarity and artifact identity come apart **in both directions**, so a method that compares
labels gets both cases backwards.

Where grounding asks *does this exist?*, sharing asks *have I seen this one before?*, and the answer
comes from the same noun phrase.

### 3. Sort each cluster by how certain it is

This is what makes the pass usable rather than an interrogation. Three tiers, and only the middle one
costs the author anything:

| Cluster | Certain? | Action |
|---|---|---|
| Byte-identical labels, same artifact | yes | Already unified. Say nothing |
| Byte-identical labels, **different** artifacts | yes | `R03`, 🔴. Report it; do not ask |
| Different labels, **plausibly** one artifact | **no** | Ask. → `interview.md` |
| Different labels, different artifacts | yes | Nothing. Move on |

The third row is the whole reason this skill asks questions. Whether *"the committed training split"*
and *"the train.csv split as committed"* name one file is not visible in the labels, not decidable
from the models, and not something to guess: it is knowledge the author has and the corpus does not
record.

---

## The discipline

> **An `R01` or `R02` finding must name the shared artifact explicitly and quote both labels in full.**
> If you cannot name one artifact that both leaves denote, it is an open question.

The failure mode is proposing to merge two things that merely sound alike. **A wrong merge is worse
than a missed one**, because it collapses a distinction the author drew on purpose, and if applied it
silently changes what the argument claims. A missed merge costs a duplicated check; a wrong one
corrupts the case.

Three further limits:

- **Never propose a merge across a non-atomic leaf.** A leaf naming two independent artifacts has no
  single artifact to cluster on. Say that the leaf should be split first, and that `jpipe-review` is
  what diagnoses it.
- **Every finding carries its unification consequence.** Aligning two labels *creates* a unified group
  and renumbers every later `unified_N`. The `.jd` diff is one line; the effect reaches ids that may
  be referenced from a step library this skill does not read.
- **Never report a bare count.** "12 possible duplicates" is noise. A finding the author cannot act on
  without redoing your analysis goes in Open questions with the labels quoted, or goes nowhere.

---

## R01. Same artifact, drifted labels

The common case, and the cheapest to fix.

```text
r13.jd:11  evidence e_train is "The committed training split"
r20.jd:9   evidence e_data  is "The train.csv split as committed"
```

Both denote `data/train.csv`, **as the author confirmed**. As written they are two nodes; the check
runs twice.

The fix aligns the labels on one wording. Prefer the one more specific about the artifact, since that
is also the better ground. Here neither is great, and the alignment is a good moment to improve both:

```jd
justification r13 {
  conclusion c is "No protected attribute reaches the model (R13)"
  strategy   s is "Confront the training split's column set with the protected-attribute list; the intersection is empty"
  evidence   e_train is "The committed data/train.csv split and its header row"
  s supports c
  e_train supports s
}

justification r20 {
  conclusion c is "The training split is the frozen committed one (R20)"
  strategy   s is "Confront the split's checksum with the one recorded at freeze time; they match"
  evidence   e_train is "The committed data/train.csv split and its header row"
  s supports c
  e_train supports s
}
```

An `assemble` over both now unifies the two leaves into one `unified_N`.

Note what did **not** change: the two strategies. Sharing a fact does not mean sharing the check. The
same artifact legitimately grounds different arguments, and one of these confronts a column set while
the other confronts a checksum. **Align the leaves only.**

## R02. Extract a shared leg

When the whole `fact → check → verdict` triple repeats, aligning labels is not enough: you would be
maintaining three copies of the same reasoning.

Extract it into its own requirement model and have the others `refine` at their leaf, following
`refinement.md` F02: `rNN_base` plus the refine exported under the reused name, in the requirement
file.

Prefer `R01` when only the ground repeats. Reach for `R02` when the warrant repeats too.

## R03. Accidental unification 🔴

The inverse, and the only defect here. Two elements in different models carry **identical labels** but
denote different things. Under `assemble` they merge into one node, and the merged node claims
something neither author wrote.

```text
g2_fates.jd:14      evidence e_metrics is "The reported metrics"   → model/v2/metrics.json
g6_efficiency.jd:9  evidence e_metrics is "The reported metrics"   → the CI timing report
```

The tell is a label generic enough that two authors could arrive at it independently: *"the reported
metrics"*, *"the test results"*, *"the configuration"*. Specific labels do not collide by accident.

The fix is to disambiguate the labels, which is what a good ground needed anyway: a label too generic
to identify its artifact was never doing its job. `unifyExclude` exempts specific ids, but treat it as
a workaround. It suppresses the symptom and leaves two elements still claiming to be the same fact.

**Report `R03` without asking.** It is the one row in this file that is not a matter of opinion: the
composed model already asserts the merge, so there is nothing for the author to decline. Do confirm
the artifacts really differ before reporting, since two identical labels that *do* name the same thing
are correct and unremarkable.

## R04. Redundant check

Two warrants perform the same check on the same datum in different words. Less common than `R01` and
usually a consequence of it: once the leaves unify, two near-identical strategies hanging off one node
become visible. Worth mentioning, rarely worth a structural change.

---

## Report shape

```text
**R1 · `[JD-R01 duplicate-fact-not-unified]` · r13.jd:11:19 ⇄ r20.jd:9:19**
*Two leaves name the same artifact but will not unify.*
Shared artifact: `data/train.csv`, confirmed in answer to question 1.
  r13 `e_train`  "The committed training split"
  r20 `e_data`   "The train.csv split as committed"
→ Align both on "The committed data/train.csv split and its header row". `assemble` will then unify
  them into one node, and the check runs once for both goals.
Authority: house.
Blast radius: two label edits, no id changes, **but this creates a new unified group**, so every later
  `unified_N` shifts. Re-render the composed model after applying.
```

Severity: `R01`, `R02`, `R04` are 🔵 **REUSE**, always declinable. `R03` is 🔴 **UNSOUND**.
