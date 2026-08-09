# The survey report

Emit this at Step 5 and stop, unless `--apply` was given.

## Who reads this

**The engineer who built the system.** Not a safety specialist, not an assurance consultant, and not
someone who has read this skill. They know their pipeline, their requirements and their CI. They have
never heard of Toulmin, do not know what a warrant is, and have no idea what `R01` means, and none of
that is a gap in their competence: it is vocabulary internal to this tool.

So the report is written in their terms, about their system. Three things per finding, in this order:

| | |
|---|---|
| **What's wrong** | stated concretely, naming both places and quoting both labels |
| **Why it matters** | the consequence *for them*: work done twice, a check that will not run once, a claim the composed model makes that nobody wrote |
| **Options** | more than one where more than one exists, with the trade-off named. They choose |

A finding that stops after "what's wrong" is a complaint. One that stops after "why" is a lecture. The
options are what makes it useful.

This skill has an extra reason to care. Its findings are all of the form *"these two things you wrote
months apart are really the same thing"*, which reads as an accusation of sloppiness unless the writing
is careful. It is not sloppiness: it is the absence of a mechanism, which is what this skill is.

### Never write these words

| Not this | This |
|---|---|
| "these leaves will not unify" | "worded differently, so the composed model keeps them as two nodes and runs the check twice" |
| "accidental unification" | "when these are composed, the two become one node, and the merged node says something neither file says" |
| "duplicate-fact-not-unified" | "both of these are about `data/train.csv`" |
| "extract a shared leg" | "this whole argument is written out twice; move it to one file and point both at it" |
| "should be a refine" | "r22 already argues this. This file could use that argument instead of asserting it" |
| "orphan model" | "nothing in the corpus loads this file" |
| "UNSOUND", "STRUCTURE", "REUSE", "CONVENTION" | the section headings below, which say what they mean |
| "authority: house" | "a convention rather than a defect: take it or leave it" |
| "`R01` at r13.jd:11" *as the explanation* | say what is wrong; the id goes at the end, for reference |

Two words are worth keeping, because they are the reader's own domain rather than ours: **`assemble`**
and **`refine`** are jPipe keywords they write, so use them. *"Unify"* is not: it names a compiler pass
they never invoke, so say what it does instead.

Rule ids still appear, once, at the end of each finding. They stay because people cite them in review
threads and script against them, but they are a reference number, never an argument.

---

## Rules for every finding

1. **Point at both places.** `file:line` and the element id on each side, with both labels quoted
   verbatim. A cross-model finding a reader cannot see both halves of is a claim they must take on
   trust, which is the one thing an assurance case is against.
2. **Name the shared artifact.** Not "these look similar": the thing itself, `data/train.csv`. If you
   cannot name one artifact both leaves denote, this is an open question, not a finding.
3. **Say the answer came from them.** Where a finding rests on an interview answer, say so (*"you
   confirmed these are the same file"*). It tells the reader the identity claim is theirs, not a guess
   of yours, which is exactly the distinction that makes the finding safe to act on.
4. **Give the wording for both sides**, in full. A merge proposal that quotes only the new label leaves
   the reader diffing in their head.
5. **Every label you propose is short**: under 10 words for a fact, under 15 for a check. This matters
   more here than anywhere else, because a label is only shared when two files match it **exactly**. A
   long canonical wording is one nobody types twice, so it is a merge that quietly does not happen.
6. **Say what the edit costs**, and where labels are aligned say the specific thing: this creates a
   shared node, and the ids of later shared nodes shift, which matters if anything outside the models
   refers to them.
7. **Never report a bare count.** "12 possible duplicates" is not actionable.
8. **Never report what one model shows.** Whether a leaf asserts a verdict, whether it fuses two facts,
   whether the artifacts exist: that is `jpipe-review`'s work, per model. Duplicating it here teaches
   people to run one skill instead of both.

## Tone

- **Duplication is normal, and say so.** Two engineers writing two goals months apart *will* word the
  same fact differently. Nobody did anything wrong.
- **Say what the sharing buys**, not that the duplication exists. *"The check runs once and covers both
  requirements"* is a reason. *"These are duplicates"* is a complaint.
- **No scores or grades.** Counts of findings, yes. A letter for their corpus, no.

---

## Template

```markdown
# Survey: <target>

<N> models · <M> elements · <a> serious, <b> worth fixing, <c> opportunities, <d> suggestions
Asked you <q> questions; <answered> answered, <declined> declined.
<what was and was not looked at, in one line>

## 🔴 Composing these models makes a claim nobody wrote (<a>)
<R03>

## 🟠 An argument the corpus already contains is being asserted instead (<b>)
<F01>

## 🔵 The same work is being done twice (<c>)
<R01, R02, R04: opportunities, always declinable>

## 🟡 Suggestions (<d>)
<F02-F04: placement, files nothing loads, competing entry points>

<each finding, in every section:>
### <n>. <the problem in one plain sentence>

`<file>:<line>` `<id>` · "<label>"
`<file>:<line>` `<id>` · "<label>"

**What's wrong.** <the defect, concretely, naming the artifact both sides denote>

**Why it matters.** <the consequence: work done twice, a check that will not run once, a claim the
composed model makes that neither file says>

**Options.**
  **a.** <the first option, with the exact wording for both sides>
  **b.** <the second, with its trade-off named>
  <which you would pick, and why, in one clause>

Cost: <what moves, including whether a shared node is created or destroyed>  ·  Reference: `[JD-XNN]`

## The corpus

| File | Model | Root? | Composed by | Elements | 🔴 | 🟠 | 🔵 | 🟡 |
|---|---|---|---|--:|--:|--:|--:|--:|

## What you told me
<every question, your answer, and what followed. Declined clusters belong here, not in Open questions>

## What to do first
<dependency order, in plain words: what unblocks what>

## Open questions
<unanswered clusters and unasked ones, both labels quoted. Not findings.>

## Not looked at
<what this survey did not cover, so a clean report is not mistaken for a broad one>
```

**What you told me** is not optional, and it is the section that makes a second run cheap: it records
every answer, including the noes, so nobody is asked the same thing twice.

---

## Worked example

```markdown
# Survey: justifications/

6 models · 47 elements · 1 serious, 1 worth fixing, 1 opportunity, 1 suggestion
Asked you 3 questions; 2 answered, 1 declined.
Read every .jd under justifications/ and compared them. Did not judge any model on its own.

## 🔴 Composing these models makes a claim nobody wrote (1)

### 1. Two different files are both called "The reported metrics"

`g2_fates.jd:14` `e_metrics` · "The reported metrics"
`g6_efficiency.jd:9` `e_metrics` · "The reported metrics"

**What's wrong.** These labels are identical, character for character, but they are about different
files. The strategies above them say which: g2 compares per-group selection rates, so it means
`model/v2/metrics.json`; g6 compares wall-clock duration, so it means the CI timing report.

**Why it matters.** When these models are composed with `assemble`, anything with the same label
becomes a single node. So the composed case will show one box, feeding both the fairness leg and the
efficiency leg, claiming one file grounds both. Neither of your files says that. Whoever reads the
composed diagram sees an argument nobody wrote, and it looks tidier than the truth.

**Options.**
  **a.** Give each its own name, which is worth doing anyway since neither currently says which file
     it means:
     `g2_fates.jd` `e_metrics`      → "The fairness metrics in model/v2/metrics.json"
     `g6_efficiency.jd` `e_metrics` → "The CI timing report for the release run"
  **b.** Leave the labels and list the ids in `unifyExclude` when you compose. This stops the merge
     without fixing the ambiguity, so the next person to read either file still cannot tell which
     file it means.
  (a). (b) suppresses the symptom, and you would be carrying that config forever.

This one is not a matter of taste: the merge is what the compiler does, so there is nothing here to
agree or disagree with.

Cost: two labels. Removes a shared node, so the ids of later shared nodes shift down
  ·  Reference: `[JD-R03]`

## 🟠 An argument the corpus already contains is being asserted instead (1)

### 2. r20 states something r22 already proves

`requirements/r20.jd:11` `e_grid` · "The identity grid is the full 27-cell one (R22)"
`requirements/r22.jd:4` `c` · "The identity grid is the full 27-cell one (R22)"

**What's wrong.** r20 takes this as a given. r22 is a whole argument that establishes it, with its own
evidence, and it concludes the same sentence.

**Why it matters.** Right now the two are only connected by the `(R22)` you typed in the label. If
r22's argument ever stops holding, r20 carries on asserting its conclusion as a fact, and nothing
links the two so nothing tells you. You also cannot see the connection in either diagram.

**Options.**
  **a.** Point r20 at r22's argument with `refine`, so r22's whole tree is grafted where the leaf is.
     Conventionally this lives in r20's own file, under the same name, so nothing that uses r20 has
     to change:
     ```
     load "r22.jd"
     justification r20_base { ... evidence e_grid is "... (R22)" ... }
     justification r20 is refine(r20_base, r22) { hook: "e_grid" }
     ```
  **b.** Leave it as a leaf and treat the `(R22)` tag as the link. Cheaper, and the link stays
     invisible to both the compiler and the diagram.
  (a). It is the reason `refine` exists, and it is one file's change.

Cost: r20.jd only. Everything that composes `r20` picks up the fuller argument with no change.
  Structural, so recompile and re-render  ·  Reference: `[JD-F01]`

## 🔵 The same work is being done twice (1)

### 3. r13 and r20 are both about data/train.csv, worded differently

`requirements/r13.jd:11` `e_train` · "The committed training split"
`requirements/r20.jd:9` `e_data` · "The train.csv split as committed"

**What's wrong.** Both are `data/train.csv`, which you confirmed when I asked. The wordings differ, so
nothing connects them.

**Why it matters.** Sharing in jPipe happens by exact label match, so as written these stay two
separate boxes when the models are composed. Whatever checks that the training split is what it should
be runs twice, and if you ever automate it, you will wire it up twice and can update one and forget
the other. Matched, it runs once and covers both requirements.

**Options.**
  **a.** Put both on one wording. Neither of the current two names the file, so this is a good moment
     to fix that as well:
     `r13.jd` `e_train` → "The committed data/train.csv and its header row"
     `r20.jd` `e_data`  → "The committed data/train.csv and its header row"
  **b.** Leave them. The cost is one duplicated check, which is small today and grows with each
     requirement that touches the training data.
  (a), and note the two strategies stay exactly as they are: r13 checks the column set, r20 checks a
  checksum. Sharing the fact is not sharing the check, and those are genuinely different questions.

Cost: two labels, no ids change. Creates a shared node, so the ids of later shared nodes shift
  ·  Reference: `[JD-R01]`

## 🟡 Suggestions (1)

### 4. Nothing in the corpus loads g5_draft.jd

`g5_draft.jd:6` · model `draft_safety`

**What's wrong.** Searched all six models for `load "g5_draft.jd"`, for `draft_safety` as an
`assemble` source, and for it as a `refine` base or refiner. Nothing references it.

**Why it matters.** Probably nothing, but it is worth a look: either it is a draft you can delete, or
its consumer was renamed and something you meant to be in the case is silently outside it. Those two
have very different consequences and the corpus cannot tell them apart.

**Options.**
  **a.** Delete it if it is a leftover.
  **b.** Wire it in if it was meant to be part of the case.
  **c.** Leave it and note in its header that it is a separate entry point on purpose.
  I cannot tell which, and a model composed by a script outside `justifications/` would look exactly
  like this from here.

Cost: nothing, this needs a decision rather than an edit  ·  Reference: `[JD-F03]`

## The corpus

| File | Model | Root? | Composed by | Elements | 🔴 | 🟠 | 🔵 | 🟡 |
|---|---|---|---|--:|--:|--:|--:|--:|
| g1_top.jd | top | **yes** | (root) | 6 | 0 | 0 | 0 | 0 |
| g2_fates.jd | fairness | no | g1_top | 8 | 1 | 0 | 0 | 0 |
| g6_efficiency.jd | efficiency | no | g1_top | 7 | 1 | 0 | 0 | 0 |
| requirements/r13.jd | r13 | no | g2_fates | 4 | 0 | 0 | 1 | 0 |
| requirements/r20.jd | r20 | no | g2_fates | 5 | 0 | 1 | 1 | 0 |
| g5_draft.jd | draft_safety | no | **nothing** | 6 | 0 | 0 | 0 | 1 |

## What you told me

1. r13 `e_train` and r20 `e_data`, both `data/train.csv`? → **yes**. Became finding 3.
2. g4 `e_report` and g6 `e_timing`, both the benchmark record? → **no**, different things. Dropped,
   and I will not ask again on this corpus.
3. r9 `e_env` and r14 `e_deps`, both the `Pipfile`? → *not answered*. See open questions.

## What to do first

1. **Finding 1.** The composed case currently claims something neither file says, so nothing built
   from these models is trustworthy until it is settled.
2. **Finding 3**, the two labels. Re-render afterwards: matching them creates a shared node.
3. **Finding 2**, the refine. Structural, one file, recompile after.
4. **Finding 4.** Needs a decision from you, not an edit.

## Open questions

**`requirements/r9.jd:12` and `requirements/r14.jd:15`**: r9 `e_env` is "The committed Pipfile and the
pipeline source files" and r14 `e_deps` is "The dependency manifest as committed". These may both be
the `Pipfile`, but r9's label names two things at once, so there is no single thing to match against.
Run `jpipe-review` on r9 first: it will flag that leaf as covering two facts, and once it is split
this becomes answerable.

**Four more pairs I did not ask about**, the budget being 7 questions and these ranking below it:
r3 `e_split` and r18 `e_data`; g3 `e_log` and g4 `e_log`; r7 `e_model` and r11 `e_fitted`; r22
`e_grid` and r24 `e_matrix`. Both labels for each are quoted above. Answer any of them unprompted and
a re-run will act on it.

## Not looked at

- **Whether any single model is a good argument.** This survey only compared models with each other.
  Whether a leaf states a verdict where it should name a fact, or names a file that does not exist,
  is `jpipe-review`'s job, one model at a time. A clean survey and a clean review are different
  claims, and a corpus wants both.
- **Anything outside `justifications/`.** A model composed by a script elsewhere, or a step library
  referring to shared-node ids, would not show up here. Finding 4 is stated with that limit.
- **Whether any of this compiles.** Nothing was built, because nothing was edited. `jpipe diagnostic`
  and your editor are the authority there.
```
