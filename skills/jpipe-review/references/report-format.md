# The findings report

The report **is** the product. A fixed shape means two reviews of the same target are diffable, and
it enforces discipline: there is a slot for the rule id, the location, and the blast radius on every
finding, so omitting one is visibly wrong rather than merely unmentioned.

Emit this at Step 5 and stop, unless `--apply` was given.

---

## Rules for every finding

1. **An id, its description, a location, a quote.** `[JD-XNN name]` followed by the rule's
   **Description** from `rules.md`, then `file:line` as you read it (plus the column of the label's
   opening quote when you can point at it), and the element's label quoted verbatim. A finding the
   author has to go hunting for is half a finding.

   Never make the id carry the meaning. `[JD-A01 claim-as-evidence]` alone is a lookup key, and an
   author reading their first review has no table to look it up in. Spell the rule out:

   ```text
   **A2 · `[JD-A01 claim-as-evidence]` · requirements/r3.jd:14:19 · `evidence e_schema`**
   *A leaf asserts a verdict where it should name an artifact.*
   ```

   The description says what the rule is; the lines under it say why this element trips it. Both, every
   time, including in the fix list at Step 6 and in the one-line summaries.
2. **Say what should replace it.** Not "this is wrong", but the actual proposed wording. For a
   three-part rewrite, give all three parts.
3. **State the blast radius.** Label-only? New ids? Does it create or destroy a unified group? This
   is the line that tells the author whether the fix is two minutes or an afternoon.
4. **Name the authority when it is not `language`.** A finding backed by Toulmin or by house practice
   is a proposal. Say so, and the author can disagree without arguing with a tool.
5. **Never report a bare count.** "3 questionable leaves" is noise. A finding the author cannot act
   on without redoing your analysis should be an open question or nothing.
6. **Stay inside the file.** Every location, quote, and proposed edit belongs to the model under
   review. A finding is never stated in terms of a second `.jd`, because this review never read one.

## Tone

Reviewing someone's assurance case is reviewing their reasoning, which lands harder than reviewing
their code. Two habits keep it useful:

- **Describe the defect, not the author.** *"This leaf asserts the verdict"*, not *"you forgot"*.
- **When the pattern came from the official docs, say so.** `jpipe-compiler/docs/design/language.md`
  and the release example both use `evidence e is "The test suite passes"`, which is `A01`. An author
  who followed the tutorial did the reasonable thing. Explain the rule; do not imply carelessness.

---

## Template

```markdown
# jPipe review: <target>

jpipe <version> · <N> models reviewed independently · <M> nodes · **<a> UNSOUND · <b> ABSTRACTION · <c> CONVENTION**
Passes run: abstraction, grounding, conventions
<omit-note if any pass was skipped and why>

## 🔴 UNSOUND (<a>)
<findings: the argument does not hold>

## 🟠 ABSTRACTION (<b>)
<findings: elements at the wrong rung>

## 🟡 CONVENTION (<c>)
<house style: declinable, and irrelevant if the project states its own conventions>

<each finding, in every section:>
**<n> · `[JD-XNN name]` · <file>:<line>:<col> · `<kind> <element-id>`**
*<the rule's Description, verbatim from rules.md>*
<what is wrong here, quoting the label>
→ <the proposed replacement, in full>
Authority: <argument | house>            <omitted when the authority is language>
Blast radius: <labels only | new ids | unification impact>

## Per-file verdict

| File | Model | Nodes | 🔴 | 🟠 | 🟡 | Class |
|---|---|--:|--:|--:|--:|---|

## Suggested fix order
<dependency order, not importance order; see rules.md>

## Open questions
<judgement calls, uncertain groundings, requirement tags that may want a refine. Not findings.>

## Not reviewed
<skipped files and why; passes not run; the single-model scope limit>
```

The **Open questions** and **Not reviewed** sections are not optional padding. They are where the
review states its own limits, and a report without them implies a completeness it does not have.

---

## Worked example

```markdown
# jPipe review: justifications/

jpipe 2.3.1 · 5 models reviewed independently · 31 nodes · **1 UNSOUND · 3 ABSTRACTION · 1 CONVENTION**
Passes run: abstraction, grounding, conventions

## 🔴 UNSOUND (1)

**U1 · `[JD-G02 artifact-stale]` · requirements/r3.jd:9:19 · `evidence e_split`**
*The label missed a rename; a near-match exists under another name.*
Leaf names *"The committed data/dev.csv split and its header row"*.
Searched: `data/dev.csv`, `**/dev.csv`. No match.
Nearest: `data/train.csv`, `data/test.csv`, `data/counterfactual.csv`.
→ Three splits exist and none is named `dev`. Likely a rename the label missed. Confirm which
  split R3 is about; the fix is label-only.
Blast radius: one label, no id changes, no unification impact.

## 🟠 ABSTRACTION (3)

**A1 · `[JD-A05 non-atomic-evidence]` · requirements/r9.jd:12:19 · `evidence e_env`**
*One leaf names two independent facts.*
Leaf fuses two independent artifacts: *"The committed Pipfile and the pipeline source files"*.
An allowlist comparison and an import scan share nothing but the word "and", so one warrant
cannot check both and a failure cannot say which half failed.
→ Split into two legs:
  `e_pipfile`: "The committed Pipfile and its [packages] dependency table"
                 checked by "Confront the declared packages with the CPU-only allowlist"
  `e_source`: "The committed pipeline source: the src/ package and the run_v*.py entry points"
                 checked by "Scan the imports of every pipeline source file for a GPU or network module"
Blast radius: +1 evidence, +1 strategy, +1 sub-conclusion, 4 new relations. Structural; recompile
  and re-render after applying.

**A2 · `[JD-A01 claim-as-evidence]` · requirements/r3.jd:14:19 · `evidence e_schema`**
*A leaf asserts a verdict where it should name an artifact.*
*"A schema check over each split passes"* is a Claim in a Grounds slot: it asserts the verdict
this leg exists to reach, so the leg proves itself and cannot fail.
→ Single-leg rewrite; the existing strategy `s` can host the check:
  **grounds** (evidence)  → "The committed train, test and counterfactual CSV splits and their header rows"
  **warrant** (strategy)  → "Confront each split's column set with the schema in SPECS section 2; every split matches"
  **claim**   (conclusion) → unchanged
Authority: argument, not enforced by the compiler. Worth noting that
`jpipe-compiler/docs/design/language.md` uses this exact pattern in its own example.
Blast radius: two labels, no id changes, no unification impact.

**A3 · `[JD-A03 missing-intermediate-claim]` · requirements/r14.jd:9:19 · model `r14`**
*A leg reaches a verdict that nothing writes down.*
Three unrelated leaves (`e_decision`, `e_severe`, `e_cfg`) wire straight into the top strategy `s`.
Each reaches its own verdict; none is written down, so `s` silently combines three judgements and
a failure cannot be localised to a leg.
→ Give each leg a `sub-conclusion` + `strategy`, and let `s` state why the three are jointly
  sufficient.
Blast radius: +3 sub-conclusions, +3 strategies, 9 relations rewired. Structural; apply last and
  re-render.

## 🟡 CONVENTION (1)

**C1 · `[JD-C06 missing-header]` · requirements/r14.jd:1**
*No provenance header tracing the argument to what it serves.*
Nothing in the file traces this argument to the requirement it
serves or the decisions behind it.
→ Worth adding, and it is where the backing for `s_thresh` belongs: the warrant confronts accuracy
  with "the 0.8 threshold" but nothing here says what authorizes 0.8.
Authority: house.

## Per-file verdict

| File | Model | Nodes | 🔴 | 🟠 | 🟡 | Class |
|---|---|--:|--:|--:|--:|---|
| requirements/r9.jd | r9 | 8 | 0 | 1 | 0 | 🟡 single-leg split |
| requirements/r3.jd | r3 | 3 | 1 | 1 | 0 | 🟡 single-leg reword |
| requirements/r14.jd | r14 | 5 | 0 | 1 | 1 | 🟠 multi-leg |
| g2_fates.jd | fates | 8 | 0 | 0 | 0 | 🟢 at abstraction |
| g6_efficiency.jd | efficiency | 7 | 0 | 0 | 0 | 🟢 at abstraction |

## Suggested fix order

1. **U1**, artifact-stale, *the label missed a rename*. The argument rests on a file that is not
   there, so nothing else in r3 is trustworthy until it is settled.
2. **A1**, non-atomic-evidence, *one leaf names two independent facts*. First among the 🟠: the split
   produces the atoms the rest is written against.
3. **A2**, claim-as-evidence, *a leaf asserts a verdict where it should name an artifact*. Label-only
   reword, zero blast radius.
4. **A3** missing-intermediate-claim and **C1** missing-header: structural and documentation.
   Recompile and re-render after A3.

## Open questions

**O1 · requirements/r7.jd:11 · `evidence e_model`**: names *"the fitted classifier"*, a produced
artifact rather than a committed one. `model/` is git-ignored and empty in a clean checkout, but
`run_v2.py` produces it, so the fact is reachable. Not reported as G01. Is grounding on a produced
artifact intentional here?

**O2 · requirements/r32.jd:9**: the leaf reads *"core test modules pass"*, which is the A01 shape.
But R32 is literally about the test suite, so "the suite's last run record" may be the legitimate
fact rather than a verdict in disguise. Judgement call; left alone. ⚪

**O3 · requirements/r14.jd:15 · `evidence e_deps`**: the leaf cites `(R9)`. If a requirement argument
for R9 exists, this is the place to `refine` against it rather than assert it. Does one? Not visible
from inside this file.

## Not reviewed

- **Anything outside these five files.** Each model was reviewed on its own, and no other `.jd` was
  read. So: whether two of these leaves will unify under `assemble`, whether a fact argued here is
  already argued elsewhere, and whether anything loads these models are all unanswered. A 🟢 above
  means the model holds on its own terms, nothing more. `jpipe-survey` answers those.
- **Whether any of this compiles.** No file here was built: `jpipe diagnostic` and the editor are the
  authority on that, and they have already told you. This review is about what the argument means, and
  a model can mean nothing while parsing perfectly. Nothing was compiled because nothing was edited.
- **justifications/steps/**: the Python step library is out of scope for this skill.
- `--no-grounding` was not passed; the grounding pass ran on all 5 models.
```
