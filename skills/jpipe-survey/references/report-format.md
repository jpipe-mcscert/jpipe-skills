# The survey report

The report **is** the product. A fixed shape means two surveys of the same corpus are diffable, and it
enforces discipline: there is a slot for the rule id, its description, the locations on both sides, and
the blast radius, so omitting one is visibly wrong rather than merely unmentioned.

Emit this at Step 5 and stop, unless `--apply` was given.

---

## Rules for every finding

1. **An id, its description, both locations, both quotes.** `[JD-XNN name]`, the rule's **Description**
   from `rules.md`, and `file:line:col` for *every* element involved. A cross-model finding names at
   least two places, and a reader who cannot see both cannot check you.
2. **Name the shared artifact.** Not "these look similar": the thing itself, `data/train.csv`. If you
   cannot name one artifact both leaves denote, this is an open question.
3. **Cite the answer that confirmed it.** Where a finding rests on an interview answer, say so
   (*"confirmed in answer to question 1"*). It tells the reader the identity claim came from the author,
   not from you.
4. **Say what should replace it**, in full, for both sides. A merge proposal that quotes only the new
   wording leaves the reader diffing in their head.
5. **State the blast radius**, and for anything that unifies, say so explicitly: aligning labels creates
   a unified group and renumbers every later `unified_N`.
6. **Name the authority when it is not `language`.** `house` findings are proposals the author declines
   freely.
7. **Never report a bare count.** "12 possible duplicates" is noise.
8. **Never report what one model shows.** Abstraction, atomicity, whether the artifacts exist: that is
   `jpipe-review`'s work, and duplicating it here trains authors to run one skill instead of both.

## Tone

Surveying someone's corpus means telling them their arguments overlap, which reads as an accusation of
sloppiness if phrased carelessly. Two habits:

- **Duplication is normal.** Two authors writing two goals months apart *will* word the same fact
  differently. That is not carelessness, it is the absence of a mechanism, which is what this skill is.
- **Say what the sharing buys.** "The check runs once and supports both goals" is a reason. "These are
  duplicates" is a complaint.

---

## Template

```markdown
# jPipe survey: <target>

jpipe <version> · <N> models · <M> elements surveyed · <K> clusters examined
**<a> UNSOUND · <b> STRUCTURE · <c> REUSE · <d> CONVENTION**
Questions asked: <n>, answered: <m>, declined: <d>

## 🔴 UNSOUND (<a>)
<R03: labels that will merge into a claim nobody wrote>

## 🟠 STRUCTURE (<b>)
<F01: leaves asserting what the corpus proves>

## 🔵 REUSE (<c>)
<R01, R02, R04: opportunities, always declinable>

## 🟡 CONVENTION (<d>)
<F02-F04: placement, orphans, entry points. Irrelevant if the project states its own conventions>

<each finding:>
**<n> · `[JD-XNN name]` · <file>:<line>:<col> ⇄ <file>:<line>:<col>**
*<the rule's Description, verbatim from rules.md>*
Shared artifact: `<the thing>`<, confirmed in answer to question N>.
  <model> `<id>`  "<label>"
  <model> `<id>`  "<label>"
→ <the proposed wording or structure, in full>
Authority: <house>            <omitted when the authority is language>
Blast radius: <edits, and whether a unified group is created or destroyed>

## Corpus map

| File | Model | Root? | Composed by | Elements | 🔴 | 🟠 | 🔵 | 🟡 |
|---|---|---|---|--:|--:|--:|--:|--:|

## Decisions
<every question, its answer, and what followed. Declined clusters belong here, not in Open questions>

## Suggested fix order
<dependency order, not importance order; see rules.md>

## Open questions
<unanswered clusters and unasked ones, both labels quoted. Not findings.>

## Not reviewed
<passes not run; unasked clusters; what a survey cannot see>
```

The **Decisions**, **Open questions** and **Not reviewed** sections are not optional padding. Decisions
is what stops a second run re-asking; the other two are where the survey states its own limits.

---

## Worked example

```markdown
# jPipe survey: justifications/

jpipe 2.3.1 · 6 models · 47 elements surveyed · 9 clusters examined
**1 UNSOUND · 1 STRUCTURE · 1 REUSE · 1 CONVENTION**
Questions asked: 3, answered: 2, declined: 1

## 🔴 UNSOUND (1)

**U1 · `[JD-R03 accidental-unification]` · g2_fates.jd:14:19 ⇄ g6_efficiency.jd:9:19**
*Identical labels name different things, and will silently merge.*
Both leaves are labelled *"The reported metrics"*, byte for byte, but denote different artifacts:
  g2_fates      `e_metrics` → `model/v2/metrics.json`, the fairness figures (per `s_flip`)
  g6_efficiency `e_metrics` → the CI timing report (per `s_runtime`)
→ Under `assemble` these merge into one `unified_N`, and the composed model then claims one artifact
  grounds both legs, which neither file says. Disambiguate both:
  g2_fates      → "The reported fairness metrics in model/v2/metrics.json"
  g6_efficiency → "The CI timing report for the release run"
Authority: language. This is what the compiler will do, not a matter of taste.
Blast radius: two labels; **removes** a unified group, so later `unified_N` ids shift down.

## 🟠 STRUCTURE (1)

**F1 · `[JD-F01 should-be-refine]` · requirements/r20.jd:11:19 · `evidence e_grid`**
*A leaf asserts what another model in the corpus proves.*
Leaf: *"The identity grid is the full 27-cell one (R22)"*.
Proved by: `requirements/r22.jd:4` `conclusion c`, *"The identity grid is the full 27-cell one (R22)"*.
→ The corpus contains the argument and r20 declines to use it. Refine against it, storing the refine
  in the requirement file under the reused name:
    load "r22.jd"
    justification r20_base { … evidence e_grid is "… (R22)" … }
    justification r20 is refine(r20_base, r22) { hook: "e_grid" }
Authority: house.
Blast radius: r20.jd only. Every branch that assembles `r20` picks up the refined form with no change.
  Structural: recompile and re-render.

## 🔵 REUSE (1)

**R1 · `[JD-R01 duplicate-fact-not-unified]` · requirements/r13.jd:11:19 ⇄ requirements/r20.jd:9:19**
*Two leaves name the same artifact but will not unify.*
Shared artifact: `data/train.csv`, confirmed in answer to question 1.
  r13 `e_train`  "The committed training split"
  r20 `e_data`   "The train.csv split as committed"
→ Align both on "The committed data/train.csv split and its header row". `assemble` then unifies them,
  so the fact is stated once and the check runs once for both goals. The two strategies stay as they
  are: r13 confronts a column set, r20 confronts a checksum, and sharing a fact is not sharing a check.
Authority: house.
Blast radius: two label edits, no id changes, **but this creates a unified group**, so every later
  `unified_N` shifts. Re-render the composed model after applying.

## 🟡 CONVENTION (1)

**C1 · `[JD-F03 orphan-model]` · g5_draft.jd:6 · model `draft_safety`**
*Nothing in the corpus loads, assembles, or refines this model.*
Searched all 6 models for `load "g5_draft.jd"`, for `draft_safety` as an `assemble` source, and for it
as a `refine` base or refiner. No consumer.
→ A draft, a stale consumer, or an undocumented second entry point. Reported as a question: the corpus
  cannot tell which, and a model composed by a script outside `justifications/` would look identical.
Authority: house.

## Corpus map

| File | Model | Root? | Composed by | Elements | 🔴 | 🟠 | 🔵 | 🟡 |
|---|---|---|---|--:|--:|--:|--:|--:|
| g1_top.jd | top | **yes** | (root) | 6 | 0 | 0 | 0 | 0 |
| g2_fates.jd | fairness | no | g1_top | 8 | 1 | 0 | 0 | 0 |
| g6_efficiency.jd | efficiency | no | g1_top | 7 | 1 | 0 | 0 | 0 |
| requirements/r13.jd | r13 | no | g2_fates | 4 | 0 | 0 | 1 | 0 |
| requirements/r20.jd | r20 | no | g2_fates | 5 | 0 | 1 | 1 | 0 |
| g5_draft.jd | draft_safety | no | **nothing** | 6 | 0 | 0 | 0 | 1 |

## Decisions

1. `data/train.csv` shared by r13 `e_train` and r20 `e_data` → **yes**. Became R1.
2. g4 `e_report` vs g6 `e_timing`, possibly one benchmark record → **no**, different artifacts.
   Not reported, and not re-asked on a later run over this corpus.
3. r9 `e_env` and r14 `e_deps`, possibly both the `Pipfile` → *unanswered*. See O1.

## Suggested fix order

1. **U1**, accidental-unification. The composed model already claims something nobody wrote, so
   nothing else here is trustworthy until it is settled.
2. **R1**, the label alignment. Creates a unified group; re-render before judging anything downstream.
3. **F1**, the refinement. Structural, one file, recompile after.
4. **C1**, the orphan. Needs a decision from a person, not an edit.

## Open questions

**O1 · requirements/r9.jd:12 ⇄ requirements/r14.jd:15**: r9 `e_env` *"The committed Pipfile and the
pipeline source files"* and r14 `e_deps` *"The dependency manifest as committed"*. These may both be
the `Pipfile`, but r9's leaf names two artifacts at once, so there is no single artifact to match
against. `jpipe-review` would flag that leaf as non-atomic; split it first, then this becomes answerable.

**O2 · 4 further clusters not asked about**, the question budget being 7 and these ranking below it:
r3 `e_split` ⇄ r18 `e_data`; g3 `e_log` ⇄ g4 `e_log`; r7 `e_model` ⇄ r11 `e_fitted`;
r22 `e_grid` ⇄ r24 `e_matrix`. Both labels for each are in the survey table above; answer any of them
unprompted and a re-run will act on it.

## Not reviewed

- **What one model shows.** Abstraction, atomicity, and whether the named artifacts exist in the tree
  are `jpipe-review`'s work, per model. A clean survey says nothing about whether any of these models
  is a good argument on its own.
- **Anything outside `justifications/`.** A model composed by a script elsewhere, or a step library
  referencing `unified_N` ids, would not appear here. F03 above is stated with that limit.
- **Whether any of this compiles.** No file was built: `jpipe diagnostic` and the editor own that, and
  a declaration clusters whether or not its file parses. Nothing was compiled because nothing was edited.
- `--no-refine` was not passed; both passes ran on all 6 models.
```
