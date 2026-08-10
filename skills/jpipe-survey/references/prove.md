# Prove it instead of asserting it

**Authority: `house`.** McSCert practice for how a corpus of justification files fits together. The most
declinable tier here: a project that does things differently is not wrong, it is different.

**Before raising anything in this file, check whether the project states its own conventions**: a
`CLAUDE.md`, a `justifications/README.md`, a contributing guide. If it does, that document wins and this
file is irrelevant.

Read this at Steps 3 and 4.

---

## 1. Comb-shaped arguments

This is what the family is for, and it is worth naming because once you see it you see it everywhere.

```text
                         conclusion
                             │
                          strategy
        ┌──────┬──────┬──────┼──────┬──────┐
        e      e      e      e      e      e
```

One strategy, a row of bare leaves, no depth anywhere. Every leaf may be perfectly good ground and the
argument may be entirely true. It is still the weakest useful shape an assurance case can take, for two
reasons that have nothing to do with whether it holds:

- **It cannot fail informatively.** One check covers six facts, so a failure cannot say which leaf let
  go. `jpipe-review` sees this much from one file and calls it `A03`.
- **Every tooth is an assertion.** A leaf is a place the argument stops and says *take this as given*. Six
  teeth is six things nobody argued.

`jpipe-review` can only propose **local** depth: add a `sub-conclusion` per leg so each one states what it
establishes. That is right, and it is all one file can offer.

**This skill can propose imported depth.** Somewhere in the corpus there is probably already a whole
argument about one of those teeth, with its own evidence and its own check. Grafting it turns an assertion
into an argument and costs one `refine`. That is `P01`, and it is the only finding in this family worth
ranking high.

## 2. `P01` · A leaf asserts what the corpus can prove

**The trigger is `establishes`, not identity**, and this is the deliberate widening: it fires far more
often than a same-proposition test would, and the extra cases are the useful ones.

Ask: *would this other element's `conclusion`, if true, be a reason to believe this leaf?*

```text
a1.jd:11  evidence   e_model is "The trained model artifact"
b2.jd:4   conclusion c       is "The model is trained properly"
```

These are **not** one claim. a1 says a file exists; b2 says a property holds of what is in it. Merging
them would be nonsense, and a rule that required identity would pass over this pair in silence. But b2 is
an entire argument about the very thing a1 takes as given, so a1 can stop asserting and start resting on
it.

Three signals, in descending strength:

| | Signal | Confidence |
|---|---|---|
| 1 | The leaf carries a requirement tag, `(Rnn)`, and a model's conclusion carries the same tag | **high**, and unambiguous |
| 2 | The leaf and some conclusion name the same subject, and the conclusion asserts a property of it | **medium**. The common case, and the one worth having |
| 3 | The leaf's subject appears somewhere in a model's conclusion, loosely | **low**. Report, do not propose |

The tag used to be the precondition. It is now only the strongest signal: a leaf that asserts what another
model concludes is `P01` whether or not anybody typed `(R22)` after it.

### Check the direction

**If the corpus model's conclusion is the weaker statement, refining is backwards.** A model concluding
*"the model file exists"* does not prove a leaf claiming *"the model is trained on the frozen split"*. The
graft has to add reasoning under the leaf, not restate it more feebly. Getting this wrong produces a
model that looks deeper and argues less, which is worse than the comb.

### The fix

`refine(base, refiner) { hook: "<leaf-id>" }` grafts the refiner's whole argument where the leaf was
(`language.md` §6). Note from that section that **the refiner's conclusion is written to match the label of
the hooked element**, which is what makes the graft read continuously instead of splicing an unrelated
claim into the tree. Where the two labels differ, say which one the refiner's conclusion should become.

### The discipline

Name the model and the `conclusion` that would prove the leaf, with its `file:line`. A finding that says
*"something in the corpus probably argues this"* is not a finding. And **one graft at a time**: each is
structural, touches at least two files, and changes the shape of the composed tree, so they are applied
and recompiled one by one rather than batched.

Severity 🟠: the argument holds as written, and it asserts a step the corpus can prove, which is the
redundancy an assurance case exists to remove.

## 3. `P02` · Store the refine in the requirement file, under the reused name

Because operators cannot nest, a refine needs a named intermediate. The convention fixes **where** it
lives, and the choice matters more than it looks.

Split the body into `rNN_base`, `load` the refiner, and export the refined model under the **reused** name
`rNN`, all in `requirements/rNN.jd`:

```text
requirements/r20.jd
    load "r22.jd"
    justification r20_base { … evidence e_grid is "… (R22)" … }
    justification r20 is refine(r20_base, r22) { hook: "e_grid" }
```

Every branch that assembles `r20` now picks up the refined form with no change to the branch file. The
alternative, binding the refine at the branch under a new name like `justified_r20`, works, but each
consuming branch must then know to use the refined name, and one that forgets **silently gets the
unrefined argument**. jPipe permits it; the house does not do it.

With the corpus in hand this is checkable rather than inferable: find the refine, find every consumer, and
say which consumers would miss it. Severity 🟡.

---

## Naming

`P01` findings arrive with a placement question, and this is the house answer:

| | Convention | Rationale |
|---|---|---|
| Goal files | carry the goal number, `g2_fates.jd` | the file is the goal |
| Requirement files | goal-agnostic, `requirements/r13.jd` | one requirement serves several goals, so naming it after one is a lie the moment a second cites it |
| Model name inside a file | semantic, `justification fairness` | the diagram reads better than `g2` |
| Element ids | `c` / `s_*` / `sc_*` / `e_*` | the kind is visible at a glance in the relation block |

Do not raise a finding for naming alone unless the corpus is otherwise consistent and one file departs from
it. A whole corpus in view finally makes that judgement possible, which also makes it tempting: resist. A
naming finding is the lowest-value thing this skill can say.

---

## Report shape

Follow `report-format.md`. `refine` and `assemble` are worth naming as themselves, since they are keywords
the reader writes. *"The refiner's conclusion merges with the hooked element"* is not: that is compiler
internals nobody asked about.

```text
### 1. b2 already argues what a1 takes for granted

`a1.jd:11` `e_model` · "The trained model artifact"
`b2.jd:4` `c` · "The model is trained properly"

**What's wrong.** a1 stops at *the file is there*. b2 is a whole argument that the thing in that file was
trained the way you intended, with its own evidence beneath it. a1 could rest on that argument and does
not.

**Why it matters.** As written, the two are connected by nothing at all. If b2's argument stops holding,
a1 carries on treating the model as a given and nothing tells you. a1 is also the fourth bare leaf under
one strategy, so if that leg ever fails you will not know which of the four gave way.

**Options.**
  **a.** Graft b2 under the leaf with `refine`. Conventionally this lives in a1's own file under the same
     name, so nothing composing a1 has to change:
       load "b2.jd"
       justification a1_base { ... evidence e_model is "The trained model artifact" ... }
       justification a1 is refine(a1_base, b2) { hook: "e_model" }
     b2's conclusion is then reworded to match the leaf it replaces.
  **b.** Leave it. The leaf is honest about being an assumption, and one fewer moving part.
  (a). It is one file's change, and it is the reason `refine` exists.

Confidence: medium, both are about the trained model and b2 asserts a property of it
Impact: a1.jd only. Structural, so recompile and re-render; everything composing a1 gets the fuller
  argument unchanged  ·  Reference: `[JD-P01]`
```

Where these land: `P01` goes under **an argument you already have is being asserted instead**, `P02` among
the suggestions. Because this whole file is house practice, phrase both as observations with a rationale
and say they are declinable.
