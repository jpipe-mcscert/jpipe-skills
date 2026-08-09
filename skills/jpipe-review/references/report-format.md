# The findings report

Emit this at Step 5. The fix list at Step 6 follows it, and edits wait for approval.

## Who reads this

**The engineer who built the system.** Not a safety specialist, not an assurance consultant, and not
someone who has read this skill. They know their pipeline, their data and their CI. They have never
heard of Toulmin, do not know what a warrant is, and have no idea what `A05` means, and none of that is
a gap in their competence: it is vocabulary internal to this tool.

So the report is written in their terms, about their system. Three things per finding, in this order:

| | |
|---|---|
| **What's wrong** | stated concretely, about the element in front of them |
| **Why it matters** | the consequence *for them*: what goes undetected, what a reader is wrongly reassured about, what breaks silently later |
| **Options** | more than one where more than one exists, with the trade-off named. They choose |

A finding that stops after "what's wrong" is a complaint. One that stops after "why" is a lecture. The
options are what makes it useful.

### Never write these words

| Not this | This |
|---|---|
| "a Claim in a Grounds slot" | "this says the check passed, which is what this part is trying to establish" |
| "the warrant does not license the inference" | "nothing here says how the file being present makes the claim true" |
| "non-atomic evidence" | "this names two different things, so one check has to cover both" |
| "wrong level of abstraction", "altitude" | "this belongs one step up: it is a conclusion, not a fact" |
| "UNSOUND", "ABSTRACTION", "CONVENTION" | the section headings below, which say what they mean |
| "authority: argument" | "this is a judgement about the argument, so disagree and it stands" |
| "`A05` at r9.jd:12" *as the explanation* | say what is wrong; the id goes at the end, for reference |

Toulmin, atomicity and the rule ids are how **you** reach a finding. They are not how you report one.

Rule ids still appear, once, at the end of each finding. They stay because people cite them in review
threads and script against them, but they are a reference number, never an argument.

---

## Rules for every finding

1. **Point at one thing.** `file:line`, the element's id, and its label quoted verbatim. A reader who
   has to hunt has been given half a finding.
2. **Say the consequence in terms of the system**, not the notation. *"If the schema drifts tomorrow,
   this still says the check passes"* beats *"the leg cannot fail"*.
3. **Offer options, and name the trade-off.** Usually two: the small edit, and the decomposition that
   costs more nodes and buys a failure you can localise. Say which you would pick and why, in one
   clause, then let them decide.
4. **Where an element does two jobs, lead with decomposition.** Splitting into legs is the
   recommendation, not the fallback (`abstraction.md` §3). Give them the reason that is theirs: a split
   argument tells you *which* half failed, and each half can be checked on its own.
5. **Every label you propose is short.** Under 10 words for a fact, under 15 for a check
   (`abstraction.md` §3b). You are proposing text that has to fit in a diagram box.
6. **Say what the edit costs.** Label-only, new ids, or a re-render. One line, plain: *"two label
   edits, nothing else moves"*.
7. **Never report a bare count.** "3 questionable leaves" is not actionable.
8. **Say plainly when you are unsure.** An open question costs the reader ten seconds. A confident
   wrong finding costs you the next four.
9. **Stay inside the file.** Every location, quote and proposed edit belongs to the model under review.

## Tone

Reviewing an assurance case means reviewing someone's reasoning, which lands harder than reviewing
their code. Three habits:

- **Describe the element, not the author.** *"This leaf asserts the verdict"*, never *"you forgot"*.
- **Assume they had a reason.** The pattern flagged most often, `evidence e is "the tests pass"`, is
  the pattern in jPipe's own worked example. An author who followed the tutorial did the reasonable
  thing, and the finding should say so rather than implying carelessness.
- **No scores or grades.** Counts of findings, yes. A letter grade for their case, no.

---

## Template

```markdown
# Review: <target>

<N> models · <M> elements · <a> serious, <b> worth fixing, <c> suggestions
<which models were reviewed, named; under -m, which of the file's models were not>

## 🔴 The argument does not hold (<a>)
<a reader could take this as assurance and get none>

## 🟠 The argument will not tell you when it breaks (<b>)
<it holds today, and cannot report its own failure>

## 🟡 Suggestions (<c>)
<the argument is fine; these would make it easier to live with>

<each finding, in every section:>
### <n>. <the problem in one plain sentence>

`<file>:<line>` · `<kind> <id>` · "<label quoted verbatim>"

**What's wrong.** <the defect, concretely, in terms of this element>

**Why it matters.** <the consequence for their system: what goes undetected, what a reader is
wrongly reassured about>

**Options.**
  **a.** <the first option, with the labels it would produce>
  **b.** <the second, with its trade-off named>
  <which you would pick, and why, in one clause>

Cost: <what moves: labels only, new ids, or a re-render>  ·  Reference: `[JD-XNN]`

## Per file

| File | Model | Elements | 🔴 | 🟠 | 🟡 |
|---|---|--:|--:|--:|--:|

## What to do first
<dependency order, in plain words: what unblocks what>

## Open questions
<judgement calls, where you could not tell, requirement tags that may want a refine. Not findings.>

## Not looked at
<what this review did not cover, so a clean report is not mistaken for a broad one>
```

**Name the scope as models, not as one file.** A verdict covers whatever was reviewed, and a file name
does not say what that was: `goals.jd` may hold two arguments. Under `-m` this carries weight rather than
tidiness, since the honest summary is *one of your arguments*, so say which models were in and list the
file's others under **Not looked at** by name. → `scope.md` §7

---

## Worked example

```markdown
# Review: justifications/

4 models · 20 elements · 1 serious, 3 worth fixing, 1 suggestion
Read each model on its own, and checked the files their evidence names against the repository.

## 🔴 The argument does not hold (1)

### 1. This argument rests on a file that is not in the repository

`requirements/r3.jd:9` · `evidence e_split` · "The committed data/dev.csv split and its header row"

**What's wrong.** There is no `data/dev.csv`. Searched for that exact path and for `**/dev.csv`; the
splits that do exist are `data/train.csv`, `data/test.csv` and `data/counterfactual.csv`.

**Why it matters.** The model compiles, renders, and looks complete. Anyone reading it concludes R3
has been checked against a dev split, and there is no dev split to check. If this was a rename, the
argument has been quietly false since the rename landed.

**Options.**
  **a.** If R3 is really about one of the three splits that exist, correct the name:
     `evidence e_split` → "The committed data/test.csv and its header row"
  **b.** If a dev split is supposed to exist, this is a finding about the repository rather than the
     model, and the fix is to add the file.
  I cannot tell which from here, and guessing would make the argument confidently wrong instead of
  obviously broken. Worth 30 seconds before anything else on this list.

Cost: one label, nothing else moves  ·  Reference: `[JD-G02]`

## 🟠 The argument will not tell you when it breaks (3)

### 2. One piece of evidence covers two unrelated things

`requirements/r9.jd:12` · `evidence e_env` · "The committed Pipfile and the pipeline source files"

**What's wrong.** These are two different facts checked two different ways: reading the Pipfile's
declared packages, and scanning the source for GPU imports. The strategy above is doing both.

**Why it matters.** There is one pass/fail here for two questions. When it goes red it cannot tell
you whether someone added a GPU package to the Pipfile or imported `torch` in the pipeline, and
those have different fixes. You would go looking by hand, which is the work the case exists to save.

**Options.**
  **a.** Split it into two legs, one per thing, which is what I would do:
     leg 1  fact   "The Pipfile's [packages] table"
            check  "Confront declared packages with the CPU-only allowlist"
            holds  "No GPU package is declared"
     leg 2  fact   "The pipeline source under src/ and run_v*.py"
            check  "Scan pipeline source imports for GPU or network modules"
            holds  "No GPU or network module is imported"
     and `s` then says why those two together mean the environment is CPU-only.
  **b.** Keep one leg and narrow it to whichever half R9 is really about, dropping the other.
     Cheaper, and it makes the argument cover less than it currently claims.
  (a) costs three nodes and gives you a failure that names itself, which is the whole reason to
  split an argument into legs rather than write one big check.

Cost: adds 1 fact, 1 check, 1 intermediate claim, 4 links. Recompile and re-render
  ·  Reference: `[JD-A05]`, and `[JD-A07]` for the strategy above it

### 3. This says the check passed, which is what it is supposed to establish

`requirements/r3.jd:14` · `evidence e_schema` · "A schema check over each split passes"

**What's wrong.** This is written as a fact, but it is a conclusion: deciding whether it is true
means running the check and judging the result. So the leg assumes what it exists to show.

**Why it matters.** Nothing in this leg can fail. If the schema drifts tomorrow, the model still
says the check passes, still compiles, and still renders green. Noticing when it stops being true is
the one thing an assurance case has to do, and this leg cannot.

**Options.**
  **a.** Name what gets inspected, and let the existing strategy `s` do the checking:
     `evidence e_schema` → "The committed train, test and counterfactual splits"
     `strategy s`        → "Confront each split's columns with the SPECS §2 schema"
     The conclusion above is unchanged, and the leg now fails when a column goes missing.
  **b.** If the schema check covers several things you would want reported separately (columns,
     types, row counts), split those into legs as in finding 2.
  (a) unless you want the finer diagnosis. It is two label edits.

Worth knowing: jPipe's own documentation uses `evidence e is "Test suite passes"` in its worked
example, so this is the shape the tutorial leads you to rather than an oversight.

Cost: two labels, no ids change  ·  Reference: `[JD-A01]`

### 4. Three unrelated facts feed one check, so a failure cannot be traced

`requirements/r14.jd:9` · `model r14` · strategy `s`

**What's wrong.** `e_decision`, `e_severe` and `e_cfg` connect straight to the top strategy. Each
supports a different intermediate step, but none of those steps is written down, so `s` is silently
combining three judgements into one.

**Why it matters.** A red light on `s` tells you R14 failed and nothing more. With three inputs
that is a three-way guess every time, and it gets worse as the model grows.

**Options.**
  **a.** Give each of the three its own intermediate claim and check, then let `s` state why the
     three together establish R14. This is the standard shape for a multi-part argument.
  **b.** If two of the three are really the same step, merge those first and this becomes two legs
     rather than three.
  (a). The extra nodes are what let a failure name itself.

Cost: adds 3 intermediate claims, 3 checks, rewires 9 links. Structural, so do it last, then
  recompile and re-render  ·  Reference: `[JD-A03]`

## 🟡 Suggestions (1)

### 5. This file does not say which requirement it serves

`requirements/r14.jd:1` · file header

**What's wrong.** No comment block at the top. Nothing connects this model to REQUIREMENTS.md or to
the decisions behind it.

**Why it matters.** Mostly for whoever picks this up in a year, including you. It is also the
natural home for something missing elsewhere: `s_thresh` confronts accuracy with "the 0.8
threshold", and nothing in the file says where 0.8 came from or who agreed to it.

**Options.**
  **a.** Add a header naming the requirement, the goals it serves, and the decision that fixed 0.8.
  **b.** Leave it, and record the 0.8 rationale wherever your project keeps that instead.
  A convention rather than a defect: take it or leave it.

Cost: a comment  ·  Reference: `[JD-C06]`

## Per file

| File | Model | Elements | 🔴 | 🟠 | 🟡 |
|---|---|--:|--:|--:|--:|
| requirements/r3.jd | r3 | 3 | 1 | 1 | 0 |
| requirements/r9.jd | r9 | 8 | 0 | 1 | 0 |
| requirements/r14.jd | r14 | 5 | 0 | 1 | 1 |
| g2_fates.jd | fairness | 4 | 0 | 0 | 0 |

## What to do first

1. **Finding 1**, the missing file. Everything else assumes the argument is about real artifacts.
2. **Finding 2**, the split. Before 4, because it produces the legs 4's structure hangs on.
3. **Finding 3**, two label edits, no structural effect.
4. **Findings 4 and 5**, structural and documentation. Recompile and re-render after 4.

## Open questions

**`requirements/r7.jd:11` · `evidence e_model`** names "the fitted classifier", which a run produces
rather than something committed. `model/` is git-ignored and empty in a clean checkout, but
`run_v2.py` writes it, so the fact is reachable. Not reported as a missing file. Is resting on a
produced artifact deliberate here?

**`requirements/r32.jd:9`** reads "core test modules pass", which is the shape of finding 3. But R32
is literally about the test suite, so "the suite's last run record" may be the honest fact rather
than a verdict in disguise. Judgement call, left alone.

## Not looked at

- **How these models fit together.** Each was read on its own. Whether two argue the same fact under
  different wording, or whether two labels will merge when composed, needs the whole corpus:
  `jpipe-survey` answers that. A clean report here means each model holds on its own terms.
- **Whether any of this compiles.** Nothing was built, because nothing was edited. `jpipe diagnostic`
  and your editor are the authority there, and have already told you.
- **`justifications/steps/`**, the Python step library, is out of scope for this review.
```
