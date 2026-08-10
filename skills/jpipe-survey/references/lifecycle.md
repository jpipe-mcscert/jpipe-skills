# When is the evidence supposed to exist?

**Authority: `house`.** Every finding here is an observation about what the corpus fails to write down,
and the author may decline all of them. None is a defect.

Read this at Steps 3 and 4, and read §2 before writing a single word about a file.

---

## 1. Three moments

A justification is not discharged at one fixed time. It may be read at design time, when the argument
is being built and half the pipeline does not exist yet, or run from CI against a commit, or revisited in
a review months later. Each `evidence` leaf implicitly picks a moment, and `artifacts.md` §2's six kinds
are what pick it:

| Kind | Exists | Ground |
|---|---|---|
| Committed path, path with a section, named symbol | **now**, in any checkout | the file, the section, the symbol |
| Produced artifact | **after a run** | whatever produces it |
| External record | **elsewhere, always** | out of reach from a repository |
| None | never, because the label names nothing inspectable | nothing |

That column is a claim the label makes, usually without meaning to. *"The committed data/train.csv"*
says *now*. *"The reported metrics"* says nothing at all: it could be a checked-in JSON file or the
output of the run this argument is about, and those are different arguments.

**Record the moment per leaf, and record "cannot tell" as its own answer.** It is the common case, and it
is the whole subject of this file.

## 2. Absence means nothing, and this skill never looks

> **Never `Glob` or `Grep` for an artifact a label names.** Not to confirm a finding, not to raise
> confidence, not once.

A produced artifact is *legitimately* missing from a clean checkout: `model/metrics.json` may be
git-ignored, and the whole point of it is that a run creates it. An external record was never in the tree
to begin with. So a survey that goes looking will report a missing file as a problem, and it will be
wrong in exactly the case that matters most, which is a case discharged from CI where that file is the
output rather than the input.

The canon says this in both places it has to: `artifacts.md` §2 resolves a produced artifact to *what
produces it*, and notes that it may be git-ignored and legitimately absent; the same section says nothing
can be concluded from an external record's absence.

**Where absence genuinely matters, it is `jpipe-review`'s.** Its grounding pass searches deliberately,
records the exact patterns it ran, and fires only on a concrete committed token that produced nothing.
That is a different question asked with a different method, and duplicating it here without the searches
would be a guess wearing a rule id.

So the findings below are about **groundability**, never presence: whether a label says enough that
somebody could go and look, and whether the corpus agrees with itself about when there would be anything
to see.

## 3. `N01` · The untimed composition

The one finding here that needs a whole closure to see, and the reason this file exists.

A composed model rests on leaves from more than one moment. Some exist in any checkout, some only after
a pipeline run, and nothing anywhere says so. There is then **no single time at which the argument can be
discharged**: read it at design time and half the leaves have nothing behind them; read it from CI and
the committed half is fine but you cannot tell that was expected.

```text
release is assemble(quality, performance)

  quality.jd:9      evidence e_specs   is "The committed SPECS section 4"        → now
  quality.jd:14     evidence e_schema  is "The committed train.csv header row"   → now
  performance.jd:8  evidence e_timings is "The recorded per-stage durations"     → after a run
  performance.jd:12 evidence e_metrics is "The reported metrics"                 → cannot tell
```

**Mixing moments is normal**, and a pipeline case that did not mix them would be unusual. Say so in the
report. The finding is that it is undocumented, not that it happened.

Two options, and the second is the one people have not considered:

- **Say the moment in the labels.** *"The reported metrics"* becomes *"The metrics.json written by the
  release run"*. Cheapest, and it also fixes the groundability of the leaf for anyone reading it cold.
- **Divide the argument by moment.** One model for what holds at design time, one for what holds after a
  run, composed above. Then each part is discharged when it can be, and a green result means something
  specific.

Severity 🟠: the argument holds, and it cannot tell you *when* it holds, which is the same class of
problem as a leg that cannot report its own failure.

## 4. `N02` · Two models disagree about one subject

Same subject, two moments. One model treats it as committed, the other as produced.

```text
r3.jd:11  evidence e_metrics is "The committed model/metrics.json"      → now
g6.jd:9   evidence e_report  is "The metrics the release run reports"   → after a run
```

One of these is wrong about the artifact, and the corpus cannot tell you which. Perhaps the file is
checked in and g6's author did not know; perhaps it is generated and r3's author is asserting something
that is only true on their machine.

**`N02` blocks `M01` on the same pair.** These two labels have one subject and would otherwise be a
merge candidate, but aligning them picks a winner silently and bakes one author's wrong belief into both
models. Report the disagreement, say the merge is available once it is settled, and stop there.

## 5. `N03` · A label nothing could ground

A leaf whose label names nothing inspectable at any moment: *"Testing is adequate"*, *"the approach is
sound"*. It has no subject to bucket on (`semantics.md` §1), so it cannot be compared with anything.

**Report it only when it blocked a comparison you were trying to make**, and then only to explain the
gap: *"r9's leaf covers two things at once, so there is no single subject to match against r14's"*. The
fix is `jpipe-review`'s, which has a rule for a leaf that names nothing and can say what it should name
instead. Never restate that rule here.

Severity 🟡, and it belongs among the suggestions rather than the findings, because on its own it is an
observation about why this skill went quiet.

---

## Report shape

Follow `report-format.md`. Two words to keep out of it: *groundability*, which is jargon, and
*lifecycle*, which sounds like process consulting. The reader's version is **when**.

```text
### 2. Nothing says when half of these files are supposed to exist

`quality.jd:9` `e_specs` · "The committed SPECS section 4"
`performance.jd:8` `e_timings` · "The recorded per-stage durations"
`performance.jd:12` `e_metrics` · "The reported metrics"

**What's wrong.** Composing `quality` with `performance` puts two kinds of thing side by side. SPECS and
the header row are in the repository and always will be. The durations only exist once the pipeline has
run, and "the reported metrics" could be either, so I could not tell.

**Why it matters.** There is no moment when you can check all of this at once. At design time the timing
leaves have nothing behind them, which looks like a broken argument and is not. In CI they are fine, and
nothing records that this was the intent, so the next person hits the same confusion. This is not a
missing file, and I have not gone looking for one: half of these are supposed to be absent until
something makes them.

**Options.**
  **a.** Put the moment in the three labels that lack it:
     `performance.jd` `e_timings` → "The per-stage durations from the release run"
     `performance.jd` `e_metrics` → "The metrics.json written by the release run"
  **b.** Split the case by moment: what holds before the pipeline runs, what holds after, composed
     above. More work, and a green result then means one specific thing.
  (a) now, and (b) when the case next grows a third goal.

Confidence: high, the kinds are unambiguous for two of the three
Impact: 2 files, labels only. No shared node moves  ·  Reference: `[JD-N01]`
```
