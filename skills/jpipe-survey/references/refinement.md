# Refinement: the corpus already contains the proof

**Authority: `house`.** McSCert practice for how a corpus of justification files fits together. The
most declinable tier: a project that does things differently is not wrong, it is different. Say so in
the report rather than asserting these as rules.

**Before raising any finding here, check whether the project has its own stated conventions**: a
`CLAUDE.md`, a `justifications/README.md`, a contributing guide. If it does, that document wins and
this file is irrelevant.

Read this at Steps 3 and 5.

**`F03` and `F04` are retired under `-m`**, which answers by construction the question both of them ask.
→ `scope.md` §6

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

**How to find it.** The Step 2 survey table already holds every `conclusion` and `sub-conclusion` label
in the corpus alongside every `evidence` label, and holds each one's model, not merely its file. So the
match is a lookup, not a search: an evidence label that restates a conclusion label found in a
*different* model. Same model and there is nothing here: a leaf restating its own model's conclusion is
that argument arguing in a circle, which is one model's own shape and so `jpipe-review`'s side of the
line. Two signals, in order of strength:

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

**Report it as a question, not a defect**, and state the scope limit explicitly, because this is the one
rule where the boundary can manufacture a finding. The graph is complete only for the scope: a rooted
scope is complete by construction, since anything the root reaches is in it, and `--global` is complete
for the repository. Outside either, a model composed by a script or loaded from another repository is
invisible from here and looks **exactly** like an orphan. Say what you searched, and over what.

**Retired under `-m`.** That flag makes every model in scope reachable from the one you named, since that
is what put it there, and puts every unreachable model out of scope. Nothing is left for this rule to
find but itself. Say so in **Not looked at**, because a file declaring a draft next to its goal is
precisely where an orphan would have been worth knowing about.

## F04. Multiple entry points

Exactly one model should be the root: the one compiled, rendered, and (when bindings exist) executed.
Other goal models are sub-trees, compiled for viewing but never run separately.

This is not tidiness. `assemble` renames elements under the parent namespace, so binding at the root
means each node is renamed **once**; binding per-goal duplicates every shared node and multiplies the
work. Two roots over an overlapping set of sources is the tell.

**Retired under `-m` too**, and for the plainer reason: you named the entry point, so the scope holds one
root by definition. This is the rule `-m` most obviously hides, since a file with two roots is both what
makes the flag worth having and what this rule is about. It belongs in **Not looked at** for that reason.

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

Follow `report-format.md`. `refine` and `assemble` are worth naming as themselves, since they are
keywords the reader writes; *"the refiner's conclusion merges with the hooked element"* is not, since
that describes compiler internals nobody asked about.

```text
### 2. r20 states something r22 already proves

`requirements/r20.jd:11` `e_grid` · "The identity grid is the full 27-cell one (R22)"
`requirements/r22.jd:4` `c` · "The identity grid is the full 27-cell one (R22)"

**What's wrong.** r20 takes this as a given. r22 is a whole argument that establishes it, and it
concludes the same sentence.

**Why it matters.** The two are connected only by the `(R22)` you typed in the label. If r22's
argument stops holding, r20 carries on asserting its conclusion as a fact and nothing tells you. The
connection is also invisible in both diagrams.

**Options.**
  **a.** Point r20 at r22's argument with `refine`, grafting r22's tree where the leaf is. This
     conventionally lives in r20's own file under the same name, so nothing using r20 has to change:
       load "r22.jd"
       justification r20_base { ... }
       justification r20 is refine(r20_base, r22) { hook: "e_grid" }
  **b.** Leave the leaf and treat the tag as the link, which keeps the link invisible to the compiler
     and the diagram.
  (a). It is the reason `refine` exists, and it is one file's change.

Cost: r20.jd only. Everything composing `r20` picks up the fuller argument unchanged. Structural,
  so recompile and re-render  ·  Reference: `[JD-F01]`
```

Where these land: `F01` goes under **an argument the corpus already contains is being asserted
instead**; `F02` to `F04` go under **suggestions**. Because this whole file is house practice, phrase
them as observations with a rationale, and say they are declinable.
