# Refinement: the corpus already contains the proof

**Authority: `house`.** McSCert practice for how a corpus of justification files fits together. The
most declinable tier: a project that does things differently is not wrong, it is different. Say so in
the report rather than asserting these as rules.

**Before raising any finding here, check whether the project has its own stated conventions**: a
`CLAUDE.md`, a `justifications/README.md`, a contributing guide. If it does, that document wins and
this file is irrelevant.

Read this at Steps 4 and 6.

---

## Why this pass exists

`jpipe-review` can see that a leaf *looks* like it should be a refine, because the house tell is a
trailing requirement tag in the label: `"… is the full 27-cell identity grid (R22)"`. What it cannot do
is check whether an argument for R22 exists, so it ends by asking the author a question it cannot
answer:

> The leaf cites `(R22)`. If a requirement argument for R22 exists, this is the place to `refine`
> against it rather than assert it. Does one?

**This skill has the corpus in hand, so it answers that question.** That is the entire difference
between `C01` there and `F01` here, and it is why one is a question and the other is a finding.

It also means the tag is a convenience, not a requirement. A leaf that asserts what another model
concludes is `F01` whether or not anyone wrote `(R22)` after it. The tag makes the match cheap to
find; the *conclusion text* is what makes it true.

---

## F01. A leaf asserts what another model proves

The signature case. An evidence leaf states something a model in this corpus establishes with a whole
argument. Written as a bare leaf, it asserts what could be proved: the corpus contains a proof and
declines to use it.

**How to find it.** The Step 3 survey table already holds every `conclusion` and `sub-conclusion` label
in the corpus alongside every `evidence` label. So the match is a lookup, not a search: an evidence
label that restates a conclusion label found in a *different* model. Two signals, in order of strength:

1. The leaf carries a requirement tag, `(Rnn)`, and a model whose conclusion carries the same tag
   exists. Strongest, and unambiguous.
2. The leaf's claim and some model's conclusion denote the same proposition in different words. Weaker,
   and it goes through the interview: this is a semantic judgement, and `interview.md` applies.

**The fix** is `refine(base, refiner) { hook: "<leaf-id>" }`, which grafts the refiner's whole argument
where the leaf was (`language.md` §6). Note from that section that the refiner's conclusion is written
to **match the label of the hooked element**, which is what makes the graft read continuously rather
than splicing an unrelated claim into the tree.

**The discipline.** Name the model and the conclusion that proves the leaf, with its `file:line`. A
finding that says "something in the corpus probably argues this" is an open question. And check
direction: if the *other* model's conclusion is the weaker statement, refining is backwards.

Severity 🟠 **STRUCTURE**: the argument holds as written, but it asserts a step the corpus can prove,
which is exactly the redundancy an assurance case exists to eliminate.

## F02. Store the refine in the requirement file, under the reused name

Because operators cannot nest, a refine needs a named intermediate. The convention fixes **where** it
lives, and the choice matters more than it looks.

Split the body into `rNN_base`, `load` the refiner, and export the refined model under the **reused**
name `rNN`, all in `requirements/rNN.jd`:

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

With the corpus in hand this is checkable rather than inferable: find the refine, then find every
consumer, then say which consumers would miss it.

## F03. Orphan model

A model that nothing in the corpus loads, assembles, implements or refines is dead weight. Usually one
of three things, and the corpus cannot tell you which:

- a draft left behind,
- a model whose consumer was renamed or deleted,
- a genuine entry point that should be documented as such.

**Report it as a question, not a defect.** Note also that the corpus you were given may not be the
whole world: a model can be composed by something outside the target, or loaded by a script. Say what
you searched.

## F04. Multiple entry points

Exactly one model should be the root: the one compiled, rendered, and (when bindings exist) executed.
Other goal models are sub-trees, compiled for viewing but never run separately.

This is not tidiness. `assemble` renames elements under the parent namespace, so binding at the root
means each node is renamed **once**; binding per-goal duplicates every shared node and multiplies the
work. Two roots over an overlapping set of sources is the tell.

---

## Naming

Findings here often come with a placement question, and this is the house answer:

| | Convention | Rationale |
|---|---|---|
| Goal files | carry the goal number, `g2_fates.jd` | the file is the goal |
| Requirement files | goal-agnostic, `requirements/r13.jd` | one requirement serves several goals; naming it after one is a lie the moment a second cites it |
| Model name inside a file | semantic, `justification fairness` in `g2_fates.jd` | the diagram reads better than `g2` |
| Element ids | `c` / `s_*` / `sc_*` / `e_*` | kind is visible at a glance in the relation block |

Do not raise a finding for naming alone unless the corpus is otherwise consistent and one file departs
from it. With a whole corpus in view that judgement is finally possible, which also makes it tempting:
resist it. A naming finding is the lowest-value thing this skill can say.

---

## Report shape

```text
**F1 · `[JD-F01 should-be-refine]` · requirements/r20.jd:11:19 · `evidence e_grid`**
*A leaf asserts what another model in the corpus proves.*
Leaf: "The identity grid is the full 27-cell one (R22)".
Proved by: `requirements/r22.jd:4` `conclusion c` "The identity grid is the full 27-cell one (R22)".
→ Refine against it rather than asserting it, per house practice storing the refine in r20.jd:
    load "r22.jd"
    justification r20_base { … }
    justification r20 is refine(r20_base, r22) { hook: "e_grid" }
Authority: house.
Blast radius: r20.jd only; every branch that assembles `r20` picks up the refined form unchanged.
  Structural: recompile and re-render.
```

Conventions are 🟡, `F01` is 🟠. Because this whole file is house practice, phrase findings as
observations with a rationale, not as violations.
