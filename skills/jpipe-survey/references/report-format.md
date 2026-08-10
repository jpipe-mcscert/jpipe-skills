# The survey report

Emit this at Step 6. The fix list at Step 7 follows it, and edits wait for approval.

## Who reads this

**The engineer who built the system.** Not a safety specialist, not an assurance consultant, and not
someone who has read this skill. They know their pipeline, their requirements and their CI. They have never
heard of Toulmin, do not know what a warrant is, and have no idea what `M01` means, and none of that is a
gap in their competence: it is vocabulary internal to this tool.

So the report is written in their terms, about their system. **Nothing is asked before it.** Every candidate
appears here, ranked, carrying how sure the skill is and what acting on it would cost, and the reader
decides. That puts a heavier duty on the writing than a question would: a reader who cannot tell a solid
finding from a speculative one has been handed a list of guesses.

Four things per finding, in this order:

| | |
|---|---|
| **What's wrong** | stated concretely, naming every place and quoting every label |
| **Why it matters** | the consequence *for them*: work done twice, an argument that cannot fail informatively, a claim the composed model makes that nobody wrote |
| **Options** | more than one where more than one exists, with the trade-off named. They choose |
| **Confidence and impact** | how sure you are and why, then what the edit touches |

A finding that stops after "what's wrong" is a complaint. One that stops after "why" is a lecture. The
options are what makes it useful, and the confidence is what makes it safe to act on.

This skill has an extra reason to care. Its findings are all of the form *"these two things you wrote months
apart are really the same thing"*, which reads as an accusation of sloppiness unless the writing is careful.
It is not sloppiness: it is the absence of a mechanism, which is what this skill is.

### Never write these words

| Not this | This |
|---|---|
| "these leaves will not unify" | "worded differently, so the composed model keeps them as two boxes and runs the check twice" |
| "accidental unification" | "composed, these two become one box, and that box says something neither file says" |
| "same-proposition" | "both of these are about the test suite" |
| "fused leaf", "non-atomic" | "this leaf covers two separate things" |
| "split the leaf to enable sharing" | "if the tests were their own leaf, it would be the same leaf r14 already has" |
| "comb-shaped" | "six bare leaves under one check, so a failure cannot say which one gave way" |
| "assertion with proof available" | "r22 already argues this. This file could use that argument instead of taking it as given" |
| "mislevelled", "wrong rung" | "one of these two is written as a check and the other as a fact" |
| "groundability", "lifecycle" | "when this is supposed to exist" |
| "orphan model" | "nothing here loads this file" |
| "UNSOUND", "STRUCTURE", "REUSE", "CONVENTION" | the section headings below, which say what they mean |
| "authority: house" | "a convention rather than a defect: take it or leave it" |
| "`M01` at r13.jd:11" *as the explanation* | say what is wrong; the id goes at the end, for reference |

Three words are worth keeping, because they are the reader's own domain rather than ours: **`assemble`**,
**`refine`** and **`load`** are jPipe keywords they write, so use them. *"Unify"* is not: it names a compiler
pass they never invoke, so say what it does instead.

Rule ids still appear, once, at the end of each finding. They stay because people cite them in review
threads and script against them, but they are a reference number, never an argument.

---

## Rules for every finding

1. **Point at every place.** `file:line` and the element id on each side, with every label quoted verbatim.
   A cross-model finding a reader cannot see both halves of is a claim they must take on trust, which is the
   one thing an assurance case is against.
2. **State the reading, and own it.** *"I read both of these as the test suite"*, not *"these are the test
   suite"*. The identity claim is yours; saying so is what lets them overrule you in four seconds.
3. **Confidence is a sentence, not a word.** *"Confidence: medium, both are about the trained model but
   neither label says which file"* tells them where to look. Bare "medium" tells them nothing.
4. **Never propose an edit on low confidence.** Report the candidate, name what would settle it, and stop.
   A fix applied on a guess is the worst thing this skill can produce.
5. **Give the wording for every side**, in full. A merge proposal that quotes only the new label leaves the
   reader diffing in their head.
6. **Impact is the blast radius**, in their terms: which files change, whether a shared node is created or
   destroyed and therefore whether later shared-node ids shift, and whether anything composing these models
   has to change.
7. **Every label you propose is short**: under 10 words for a fact, under 15 for a check. This matters more
   here than anywhere else, because a label is shared only when two files match it **exactly**, so a long
   canonical wording is one nobody types twice and a merge that quietly never happens.
8. **Never report a bare count.** "12 possible duplicates" is not actionable.
9. **Never report what one model shows.** Whether a leaf asserts a verdict, whether a check is
   unfalsifiable, whether the artifacts exist: that is `jpipe-review`'s work, per model. Duplicating it here
   teaches people to run one skill instead of both.
10. **Never claim a file is missing.** Nothing was searched for. Absence is not this skill's business and
    saying otherwise would be wrong as often as not (`lifecycle.md` §2).

## Tone

- **Duplication is normal, and say so.** Two engineers writing two goals months apart *will* word the same
  fact differently. Nobody did anything wrong.
- **Say what the sharing buys**, not that the duplication exists. *"The check runs once and covers both
  requirements"* is a reason. *"These are duplicates"* is a complaint.
- **No scores or grades.** Counts of findings, yes. A letter for their corpus, no.

---

## Template

```markdown
# Survey: <scope>

<models> models · <elements> elements · <serious> serious, <shallow> worth deepening,
  <reuse> opportunities, <suggestions> suggestions
<which models were compared, named; under -m, which of the file's models were not>
<how many subject buckets held one element and were therefore never compared>

## Worth your time, in order

<one line per finding, highest impact first, confidence breaking ties. This is the section
 the report is read for, so it comes before any finding and repeats nothing:>
1. #<n>  <what it buys, in the reader's terms>   <confidence>
2. ...

## 🔴 Composing these models makes a claim nobody wrote (<serious>)
<M03>

## 🟠 The argument is shallower than the corpus can support (<shallow>)
<P01, L01, N01, N02>

## 🔵 The same work is being done twice (<reuse>)
<D01, D02, M01, M02: opportunities, always declinable>

## 🟡 Suggestions (<suggestions>)
<P02, N03, T01, T02>

<each finding, in every section:>
### <n>. <the problem in one plain sentence>

`<file>:<line>` `<id>` · "<label>"
`<file>:<line>` `<id>` · "<label>"

**What's wrong.** <the defect, concretely, naming what the two elements have in common>

**Why it matters.** <the consequence: work done twice, a failure that cannot be localised, a claim
the composed model makes that neither file says>

**Options.**
  **a.** <the first option, with the exact wording for every side>
  **b.** <the second, with its trade-off named>
  <which you would pick, and why, in one clause>

Confidence: <level, and the reason in the same breath>
Impact: <files touched · whether a shared node appears or disappears · what recompiles>
  ·  Reference: `[JD-XNN]`

## The corpus

| File | Model | Root? | Composed by | Elements | 🔴 | 🟠 | 🔵 | 🟡 |
|---|---|---|---|--:|--:|--:|--:|--:|

## What you decided
<filled in at Step 7: which numbered fixes were applied, which were declined, and why. A declined
 item is a real result and must not be re-proposed on a later run over this scope>

## Worth a look, nothing proposed
<low-confidence candidates, both labels quoted, and what would settle each one. Not findings>

## Not looked at
<what this survey did not cover, so a clean report is not mistaken for a broad one>
```

**`Worth your time, in order` is not optional**, and it is the only section most readers will finish. Rank
by what the corpus gains: models touched, duplicated checks removed, depth added. Confidence breaks ties.
Do **not** rank by severity, because the one 🔴 in a corpus is often a two-label edit while the 🟠 that
restructures three goals is the day's real work.

**Name the scope as models, not as one file.** A verdict covers whatever was compared, and a file name does
not say what that was: `goals.jd` may hold two arguments. Under `-m` this is load-bearing rather than tidy,
since the honest summary is *one of your arguments*, so say which models were in and list the file's others
under **Not looked at** by name, along with `T01` and `T02`, which `-m` retires (`scope.md` §6).

---

## Worked example

```markdown
# Survey: justifications/

7 models · 52 elements · 1 serious, 2 worth deepening, 2 opportunities, 1 suggestion
Compared every .jd under justifications/. Did not judge any model on its own.
9 subjects appeared in only one element and were never compared against anything.

## Worth your time, in order

1. #4  the test suite becomes one leaf instead of three, and its check runs once   high
2. #2  r22's argument goes under a leaf that four goals take on faith              medium
3. #1  stops the composed case claiming one file grounds two unrelated legs        high
4. #3  says when half the release case's files are supposed to exist               high
5. #5  one of these two has a check written where a fact belongs                   medium
6. #6  nothing loads draft_fairness.jd                                             high

## 🔴 Composing these models makes a claim nobody wrote (1)

### 1. Two different files are both called "The reported metrics"

`g2_fates.jd:14` `e_metrics` · "The reported metrics"
`g6_efficiency.jd:9` `e_metrics` · "The reported metrics"

**What's wrong.** These labels are identical, character for character, and they are about different files.
The checks above them say which: g2 compares per-group selection rates, so it means the fairness metrics;
g6 compares wall-clock duration, so it means the CI timing record.

**Why it matters.** `release.jd` assembles both. Anything with the same label becomes a single box when
that happens, so the composed case shows one file feeding both the fairness leg and the efficiency leg,
claiming it grounds both. Neither of your files says that. Whoever reads the composed diagram sees an
argument nobody wrote, and it looks tidier than the truth.

**Options.**
  **a.** Give each its own name, worth doing anyway since neither says which file it means:
     `g2_fates.jd` `e_metrics`      → "The fairness metrics for the release run"
     `g6_efficiency.jd` `e_metrics` → "The CI timing record for the release run"
  **b.** Leave the labels and list the ids in `unifyExclude` when you compose. Stops the merge without
     fixing the ambiguity, so the next reader still cannot tell which file either means.
  (a). (b) suppresses the symptom and you carry that config forever.

This one is not a matter of taste: the merge is what the compiler does when it composes them, so there is
nothing here to agree or disagree with.

Confidence: high, the checks above each leaf name different comparisons
Impact: 2 files, labels only. Removes a shared node, so later shared-node ids shift down
  ·  Reference: `[JD-M03]`

## 🟠 The argument is shallower than the corpus can support (2)

### 2. r22 already argues what four goals take on faith

`requirements/r20.jd:11` `e_grid` · "The identity grid is the full 27-cell one (R22)"
`requirements/r22.jd:4` `c` · "The identity grid is the full 27-cell one (R22)"

**What's wrong.** r20 takes this as given. r22 is a whole argument that establishes it, with its own
evidence, and it concludes the same sentence.

**Why it matters.** The two are connected by the `(R22)` you typed in a label and by nothing else. If r22's
argument stops holding, r20 carries on asserting its conclusion as a fact and nothing tells you. Four goals
assemble r20, so all four inherit the assumption, and the connection is invisible in every one of their
diagrams.

**Options.**
  **a.** Graft r22 under the leaf with `refine`. Conventionally this lives in r20's own file under the
     same name, so nothing composing r20 has to change:
       load "r22.jd"
       justification r20_base { ... evidence e_grid is "... (R22)" ... }
       justification r20 is refine(r20_base, r22) { hook: "e_grid" }
  **b.** Leave the leaf and treat the tag as the link, which keeps it invisible to the compiler and to
     every diagram.
  (a). It is the reason `refine` exists, and it is one file's change.

Confidence: medium-to-high. The tag matches and the two labels are the same sentence
Impact: r20.jd only. Structural, so recompile and re-render. All four goals composing r20 pick up the
  fuller argument with no change of their own  ·  Reference: `[JD-P01]`

### 3. Nothing says when half of the release case's files exist

`quality.jd:9` `e_specs` · "The committed SPECS section 4"
`performance.jd:8` `e_timings` · "The recorded per-stage durations"
`performance.jd:12` `e_metrics` · "The reported metrics"

**What's wrong.** `release.jd` assembles `quality` with `performance`, and those rest on two different
kinds of thing. SPECS is in the repository and always will be. The durations only exist once the pipeline
has run. "The reported metrics" could be either and I could not tell.

**Why it matters.** There is no moment when you can check all of this at once. At design time the timing
leaves have nothing behind them, which looks like a broken case and is not. From CI they are fine, and
nothing records that this was the intent, so the next person hits the same confusion. To be clear, this is
not a missing file and I have not gone looking for one: some of these are supposed to be absent until a run
makes them.

**Options.**
  **a.** Put the moment into the two labels that lack it:
     `performance.jd` `e_timings` → "The per-stage durations from the release run"
     `performance.jd` `e_metrics` → "The metrics.json written by the release run"
  **b.** Split the case by moment: what holds before the pipeline runs, what holds after, composed above.
     More work, and a green result then means one specific thing.
  (a) now, and (b) when the case next grows a goal.

Confidence: high for two of the three; `e_metrics` is the one I could not place
Impact: 1 file, labels only. No shared node moves  ·  Reference: `[JD-N01]`

## 🔵 The same work is being done twice (2)

### 4. "The source and test code" hides a leaf r14 already has

`g3_quality.jd:12` `e_code` · "The source and test code are available"
`requirements/r14.jd:9` `e_tests` · "The committed tests/ directory"

**What's wrong.** g3's leaf covers two separate things at once. Half of it, the tests, is the same thing
r14 already has as a leaf of its own.

**Why it matters.** As written, nothing can connect them: g3's leaf is unique because no other model needs
exactly that pair, so it can never be shared with anything. Split it and the test half is a leaf four other
requirements could rest on too. The check over the source tree and the check over the test tree are also
different checks, and right now one strategy claims to do both, so a failure cannot say which.

**Options.**
  **a.** Split g3's leaf into two legs, and put the test half on r14's wording:
     `g3_quality.jd` `e_src`   → "The committed source tree"
     `g3_quality.jd` `e_tests` → "The committed tests/ directory"
     Each then needs its own check; the strategy above says why the two are jointly enough.
  **b.** Split it and leave both wordings alone, which fixes the check and buys no sharing.
  (a). The split is worth doing on its own, and the alignment is free once you are editing the line.

Confidence: high. Two things needing two different checks, and r14's leaf is one of them verbatim
Impact: g3_quality.jd, plus one new leg. Creates a shared node, so later shared-node ids shift
  ·  Reference: `[JD-D01]`

## 🟡 Suggestions (1)

### 6. Nothing in the corpus loads draft_fairness.jd
...

## The corpus

| File | Model | Root? | Composed by | Elements | 🔴 | 🟠 | 🔵 | 🟡 |
|---|---|---|---|--:|--:|--:|--:|--:|
| release.jd | release | yes | nothing | 2 | 0 | 0 | 0 | 0 |
| g2_fates.jd | fairness | no | release | 8 | 1 | 0 | 0 | 0 |
| ... | | | | | | | | |

## What you decided
<empty until Step 7>

## Worth a look, nothing proposed

- `r3.jd:8` `e_env` "The environment is reproducible" and `r11.jd:14` `e_deps` "The dependency manifest
  as committed". Both are about the dependency environment, but r3's label does not name a thing, so I
  could not tell whether it means the Pipfile or the lockfile. If it means the Pipfile, this is the same
  leaf as r11's and worth aligning. One word from you settles it.

## Not looked at

- **Whether any single model is a good argument.** This survey only compared models with each other.
  Whether a leaf states a verdict where it should name a fact, whether a check can fail, whether a label
  names a file that exists: all `jpipe-review`'s, which examines elements rather than comparing models. A
  clean survey and a clean review are different claims, and a corpus wants both.
- **Whether any of these files exist.** Nothing was searched for in the tree. A case may be discharged
  from CI where half its evidence is output rather than input, so absence proves nothing from here.
- **9 subjects that appeared only once.** Nothing to compare them against, and a label using a different
  word for the same thing lands outside its bucket, so the pass is not exhaustive.
- **Anything outside `justifications/`.** A model composed by a script, or a step library referring to
  shared-node ids, would not show up here.
- **Whether any of this compiles.** Nothing was built, because nothing was edited. `jpipe diagnostic` and
  your editor are the authority there.
```
