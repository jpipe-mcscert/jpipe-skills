# The findings report

The report **is** the product. A fixed shape means two reviews of the same corpus are diffable, and
it enforces discipline: there is a slot for the rule id, the location, and the blast radius on every
finding, so omitting one is visibly wrong rather than merely unmentioned.

Emit this at Step 7 and stop, unless `--apply` was given.

---

## Rules for every finding

1. **An id, a location, a quote.** `[JD-XNN name]`, `file:line:col` from the compile gate's Symbol
   Table, and the element's label quoted verbatim. A finding the author has to go hunting for is
   half a finding.
2. **Say what should replace it.** Not "this is wrong" — the actual proposed wording. For a
   three-part rewrite, give all three parts.
3. **State the blast radius.** Label-only? New ids? Does it create or destroy a unified group? This
   is the line that tells the author whether the fix is two minutes or an afternoon.
4. **Name the authority when it is not `language`.** A finding backed by Toulmin or by house practice
   is a proposal. Say so, and the author can disagree without arguing with a tool.
5. **Never report a bare count.** "12 possible duplicates" is noise. A finding the author cannot act
   on without redoing your analysis should be an open question or nothing.

## Tone

Reviewing someone's assurance case is reviewing their reasoning, which lands harder than reviewing
their code. Two habits keep it useful:

- **Describe the defect, not the author.** *"This leaf asserts the verdict"* — not *"you forgot"*.
- **When the pattern came from the official docs, say so.** `jpipe-compiler/docs/design/language.md`
  and the release example both use `evidence e is "The test suite passes"`, which is `A01`. An author
  who followed the tutorial did the reasonable thing. Explain the rule; do not imply carelessness.

---

## Template

```markdown
# jPipe review — <target>

jpipe <version> · <N> files · <M> nodes · **<a> UNSOUND · <b> ABSTRACTION · <c> REUSE · <d> CONVENTION**
Compile gate: <p> pass, <q> skipped · Passes run: abstraction, grounding, reuse, conventions
<omit-note if any pass was skipped and why>

## 🔴 UNSOUND (<a>)
<findings — the argument does not hold>

## 🟠 ABSTRACTION (<b>)
<findings — elements at the wrong rung>

## 🔵 REUSE (<c>)
<opportunities — always declinable>

## 🟡 CONVENTION (<d>)
<corpus fit — declinable, and irrelevant if the project states its own conventions>

## Per-file verdict

| File | Model | Nodes | 🔴 | 🟠 | 🔵 | 🟡 | Class |
|---|---|--:|--:|--:|--:|--:|---|

## Suggested fix order
<dependency order, not importance order — see rules.md>

## Open questions
<judgement calls, uncertain groundings, unclustered near-matches. Not findings.>

## Not reviewed
<skipped files and why; passes not run>
```

The **Open questions** and **Not reviewed** sections are not optional padding. They are where the
review states its own limits, and a report without them implies a completeness it does not have.

---

## Worked example

```markdown
# jPipe review — justifications/

jpipe 2.3.1 · 4 files · 24 nodes · **2 UNSOUND · 3 ABSTRACTION · 1 REUSE · 1 CONVENTION**
Compile gate: 3 pass, 1 skipped · Passes run: abstraction, grounding, reuse, conventions

## 🔴 UNSOUND (2)

**U1 · `[JD-G02 artifact-stale]` · requirements/r3.jd:9:19 · `evidence e_split`**
Leaf names *"The committed data/dev.csv split and its header row"*.
Searched: `data/dev.csv`, `**/dev.csv` — no match.
Nearest: `data/train.csv`, `data/test.csv`, `data/counterfactual.csv`.
→ Three splits exist and none is named `dev`. Likely a rename the label missed. Confirm which
  split R3 is about; the fix is label-only.
Blast radius: one label, no id changes, no unification impact.

**U2 · `[JD-S03 accidental-unification]` · g2_fates.jd:14:19 ⇄ g6_efficiency.jd:9:19**
Both leaves are labelled *"The reported metrics"*, but they denote different artifacts:
  g2_fates      → `model/v2/metrics.json` (fairness figures, per `s_flip`)
  g6_efficiency → the CI timing report (per `s_runtime`)
→ Under `assemble` these merge into one `unified_N`, and the composed model then claims one
  artifact grounds both legs — which neither file says. Disambiguate both labels.
Authority: language — this is what the compiler will do, not a matter of taste.
Blast radius: two labels; **removes** a unified group, so later `unified_N` ids shift down.

## 🟠 ABSTRACTION (3)

**A1 · `[JD-A05 non-atomic-evidence]` · requirements/r9.jd:12:19 · `evidence e_env`**
Leaf fuses two independent artifacts — *"The committed Pipfile and the pipeline source files"*.
An allowlist comparison and an import scan share nothing but the word "and", so one warrant
cannot check both and a failure cannot say which half failed.
→ Split into two legs:
  `e_pipfile` — "The committed Pipfile and its [packages] dependency table"
                 checked by "Confront the declared packages with the CPU-only allowlist"
  `e_source`  — "The committed pipeline source: the src/ package and the run_v*.py entry points"
                 checked by "Scan the imports of every pipeline source file for a GPU or network module"
Blast radius: +1 evidence, +1 strategy, +1 sub-conclusion, 4 new relations. **Unblocks R1 below** —
  the split `e_pipfile` is the leaf that r14 also grounds on.

**A2 · `[JD-A01 claim-as-evidence]` · requirements/r3.jd:14:19 · `evidence e_schema`**
*"A schema check over each split passes"* is a Claim in a Grounds slot — it asserts the verdict
this leg exists to reach, so the leg proves itself and cannot fail.
→ Single-leg rewrite; the existing strategy `s` can host the check:
  **grounds** (evidence)  → "The committed train, test and counterfactual CSV splits and their header rows"
  **warrant** (strategy)  → "Confront each split's column set with the schema in SPECS section 2; every split matches"
  **claim**   (conclusion) → unchanged
Authority: argument — not enforced by the compiler. Worth noting that
`jpipe-compiler/docs/design/language.md` uses this exact pattern in its own example.
Blast radius: two labels, no id changes, no unification impact.

**A3 · `[JD-A03 missing-intermediate-claim]` · requirements/r14.jd:9:19 · model `r14`**
Three unrelated leaves (`e_decision`, `e_severe`, `e_cfg`) wire straight into the top strategy `s`.
Each reaches its own verdict; none is written down, so `s` silently combines three judgements and
a failure cannot be localised to a leg.
→ Give each leg a `sub-conclusion` + `strategy`, and let `s` state why the three are jointly
  sufficient.
Blast radius: +3 sub-conclusions, +3 strategies, 9 relations rewired. Structural — apply last and
  re-render.

## 🔵 REUSE (1)

**R1 · `[JD-S01 duplicate-fact-not-unified]` · requirements/r9.jd:12:19 ⇄ requirements/r14.jd:15:19**
Shared artifact: `Pipfile`.
  r9  `e_env`     — "The committed Pipfile and the pipeline source files"  *(after the A1 split: `e_pipfile`)*
  r14 `e_deps`    — "The dependency manifest as committed"
→ Both denote the same file. Align r14 on r9's post-split wording — "The committed Pipfile and its
  [packages] dependency table" — and `assemble` will unify them, so the fact is stated once and both
  goals share the node.
Depends on: **A1** (r9's leaf must be split before there is an atom to match).
Authority: house.
Blast radius: one label edit, no id changes — **but it creates a unified group**, so every later
  `unified_N` shifts. Re-render the composed model after applying.

## 🟡 CONVENTION (1)

**C1 · `[JD-C06 missing-header]` · requirements/r14.jd:1**
No `/** */` provenance header. Every other file under `requirements/` opens with one tracing its
argument to REQUIREMENTS.md and the decisions behind it.
→ Worth adding, and it is where the backing for `s_thresh` belongs: the warrant confronts accuracy
  with "the 0.8 threshold" but nothing in the corpus says what authorizes 0.8.
Authority: house.

## Per-file verdict

| File | Model | Nodes | 🔴 | 🟠 | 🔵 | 🟡 | Class |
|---|---|--:|--:|--:|--:|--:|---|
| requirements/r9.jd | r9 | 8 | 0 | 1 | 1 | 0 | 🟡 single-leg split |
| requirements/r3.jd | r3 | 3 | 1 | 1 | 0 | 0 | 🟡 single-leg reword |
| requirements/r14.jd | r14 | 5 | 0 | 1 | 1 | 1 | 🟠 multi-leg |
| g2_fates.jd | fates | 8 | 1 | 0 | 0 | 0 | 🟢 at abstraction |
| g6_efficiency.jd | efficiency | — | — | — | — | — | ⏭ did not compile |

## Suggested fix order

1. **U1, U2** — the argument rests on a missing artifact and asserts an unintended merge. Nothing
   else is trustworthy until these are settled.
2. **A1** — the atomicity split. Before R1, because R1 needs the atom it produces.
3. **A2** — label-only reword, zero blast radius.
4. **R1** — reuse alignment. Re-render afterwards; `unified_N` numbering shifts.
5. **A3, C1** — structural and documentation. Recompile and re-render after A3.

## Open questions

**O1 · requirements/r7.jd:11 · `evidence e_model`** — names *"the fitted classifier"*, a produced
artifact rather than a committed one. `model/` is git-ignored and empty in a clean checkout, but
`run_v2.py` produces it, so the fact is reachable. Not reported as G01. Is grounding on a produced
artifact intentional here?

**O2 · requirements/r32.jd:9** — the leaf reads *"core test modules pass"*, which is the A01 shape.
But R32 is literally about the test suite, so "the suite's last run record" may be the legitimate
fact rather than a verdict in disguise. Judgement call — left alone. ⚪

## Not reviewed

- **g6_efficiency.jd** — does not compile; semantic passes skipped for this file. The compiler and
  the VS Code extension are the authority there. Its raw output:
  <details><summary>jpipe diagnostic</summary>

  ```
  [ERROR] g6_efficiency.jd:22:9: [unresolved-symbol] cannot execute: support('efficiency', 'e_time', 's_run')
  ```
  </details>

- **justifications/steps/** — the Python step library is out of scope for this skill.
- `--no-grounding` was not passed; the grounding pass ran on all 3 compiling files.
```
