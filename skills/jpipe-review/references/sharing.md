# Sharing: the same fact, argued twice

**Authority: `house`, except `S03` which is `language`.** Findings in this pass are opportunities the
author may decline — with one exception that is a genuine defect.

Read this at Step 6. The pass needs a corpus: skip it for a single-file target unless `--corpus <dir>`
is given.

---

## Why this matters in jPipe specifically

In most argumentation notations, "these two arguments rest on the same fact" is an observation with
no mechanical consequence. In jPipe it has one.

After any operator runs, the compiler merges result elements with **byte-identical labels** into a
single `unified_N` node (`language.md` §7). So two goals that ground on the same artifact, worded
identically, become one node: the fact is stated once, the check runs once, and the diagram shows the
sharing. Worded differently — by one article, one trailing period — they stay two nodes, and the same
work is done twice.

Sharing is therefore not a style preference here. It is a thing the corpus either achieves or misses,
and the difference is invisible in any single file.

---

## Method

### 1. Survey labels without opening files

Never read the corpus to find duplicates — harvest the declarations and cluster those. One pass:

```bash
grep -rEn '^[[:space:]]*(evidence|sub-conclusion|strategy|conclusion)[[:space:]]+[A-Za-z_][A-Za-z0-9_:]*[[:space:]]+is[[:space:]]+' <corpus> --include='*.jd'
```

That yields `file:line: kind id is "label"` for every element in the corpus at a cost that does not
scale with file size. Everything in this pass runs on that table. Open full files **only** for
clusters you are about to report.

### 2. Cluster by the artifact, not by the string

This is the whole discipline. String similarity is a trap in both directions:

- *"the training split"* and *"the training configuration"* share four of five words and denote
  entirely different things.
- *"The committed Pipfile and its `[packages]` dependency table"* and *"the dependency manifest as
  committed"* share almost nothing and denote the same file.

So resolve each label to the artifact it names — the same extraction as `grounding.md` §1 — and
cluster on **that**. Where grounding asks *does this exist?*, sharing asks *have I seen this one
before?*, and the answer comes from the same noun phrase.

### 3. Judge each cluster

| Cluster | Verdict | Rule |
|---|---|---|
| Same artifact, **different labels** | will **not** unify; should | `S01` |
| Same artifact, same `fact → check → verdict` leg, in ≥2 models | extract into a shared model | `S02` |
| **Identical labels**, different artifacts | will unify; must not | `S03` — 🔴 a defect |
| Two warrants running the same check on the same datum | one of them is redundant | `S04` |
| Same words, different artifacts, different labels | nothing. Move on | — |

---

## The discipline

> **An `S01` or `S02` finding must name the shared artifact explicitly and quote both labels in full.**
> If you cannot name one artifact that both leaves denote, it is an open question.

The failure mode here is the mirror of grounding's: proposing to merge two things that merely sound
alike. A wrong merge is worse than a missed one — it collapses a real distinction the author drew on
purpose, and if applied it silently changes what the argument claims.

Two further limits:

- **Never propose a merge across a leaf flagged `A05` (non-atomic).** Split it first. A fused leaf has
  no single artifact to cluster on, which is precisely why atomicity findings are ordered before
  reuse findings.
- **Every reuse finding carries its unification consequence.** Aligning two labels *creates* a
  unified group and renumbers every later `unified_N`. The `.jd` diff is one line; the effect reaches
  bindings this skill does not read.

---

## S01 — same artifact, drifted labels

The common case, and the cheapest to fix.

```text
r13.jd:11  evidence e_train is "The committed training split"
r20.jd:9   evidence e_data  is "The train.csv split as committed"
```

Both denote `data/train.csv`. As written they are two nodes; the check runs twice.

The fix is to align the labels on one wording. Prefer the one that is more specific about the
artifact, since that is also the better ground — here, neither is great, and the alignment is a good
moment to improve both:

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

Now an `assemble` over both unifies the two leaves into one `unified_N`.

Note what did **not** change: the two strategies. Sharing a fact does not mean sharing the check —
the same artifact legitimately grounds different arguments. Only align the leaves.

## S02 — extract a shared leg

When the whole `fact → check → verdict` triple repeats across models, aligning labels is not enough:
you would be maintaining three copies of the same reasoning.

Extract it into its own requirement model and have the others `refine` at their leaf, following
`conventions.md` §C02 — `rNN_base` plus the refine exported under the reused name, stored in the
requirement file.

Prefer `S01` when only the ground repeats. Reach for `S02` when the warrant repeats too.

## S03 — accidental unification 🔴

The inverse, and the only defect in this file. Two elements in different models carry **identical
labels** but denote different things. Under `assemble` they merge into one node — and the merged node
claims something neither author wrote.

```text
g2_fates.jd:14      evidence e_metrics is "The reported metrics"      → model/v2/metrics.json
g6_efficiency.jd:9  evidence e_metrics is "The reported metrics"      → the CI timing report
```

The tell is a label generic enough that two authors could arrive at it independently: *"the reported
metrics"*, *"the test results"*, *"the configuration"*. Specific labels do not collide by accident.

The fix is to disambiguate the labels — which is the same fix as `A01`/`G03` would prescribe, since
a label too generic to identify its artifact was never a good ground. Alternatively `unifyExclude`
exempts specific ids, but treat that as a workaround: it suppresses the symptom and leaves two
elements claiming to be the same fact.

Report `S03` as 🔴 **UNSOUND**. Unlike everything else here it is not declinable, because the composed
model already asserts something nobody intended.

## S04 — redundant check

Two warrants perform the same check on the same datum in different words. Less common than `S01` and
usually a consequence of it — once the leaves unify, two identical strategies hanging off one node
are visible. Worth mentioning, rarely worth a structural change.

---

## Report shape

```text
**R1 · `[JD-S01 duplicate-fact-not-unified]` · r13.jd:11:19 ⇄ r20.jd:9:19**
Shared artifact: `data/train.csv`.
  r13 `e_train` — "The committed training split"
  r20 `e_data`  — "The train.csv split as committed"
→ Align both on "The committed data/train.csv split and its header row". `assemble` will then
  unify them into one node, and the check runs once for both goals.
Blast radius: two label edits, no id changes — **but this creates a new unified group**, so every
  later `unified_N` shifts. Re-render the composed model after applying.
```

Severity: `S01`, `S02`, `S04` are 🔵 **REUSE** — opportunities, always declinable. `S03` is 🔴
**UNSOUND**.

Never report a bare count ("12 possible duplicates"). A reuse finding the author cannot act on
without redoing your analysis is noise. If a cluster is too uncertain to write up properly, it goes
in Open questions with the labels quoted, or it goes nowhere.
