# House conventions

**Authority: `house`.** McSCert practice for writing a justification file. The most local and most
declinable of the three reference tiers. A project that does things differently is not wrong, it is
different. Say so in the report rather than asserting these as rules.

These are the conventions a **single file** can be checked against. McSCert practice also covers how
a corpus fits together, and those parts are deliberately absent here: this skill reads one model, so
it cannot see them.

Promoted from `jpipe-tutorial-2026/CLAUDE.md` §Justifications and
`jpipe-tutorial-2026/justifications/README.md`. Read at Step 5.

**Before raising any finding here, check whether the project has its own stated conventions**: a
`CLAUDE.md`, a `justifications/README.md`, a contributing guide. If it does, that document wins, and
these conventions are irrelevant. Only fall back on this file when the project has no stated practice
of its own.

---

## C01 · A leaf tagged with a requirement should probably be a refine

The signature case. An evidence leaf asserts something that a requirement argument is supposed to
establish. Written as a bare leaf, it asserts what could be proved.

The house tell is visible in the label alone: a trailing requirement tag, as in
`"… is the full 27-cell identity grid (R22)"`. The author has written down that R22 is what makes
this true. If an argument for R22 exists, this leaf is declining to use it.

The fix is `refine(base, refiner) { hook: "<leaf-id>" }`, which grafts the refiner's whole argument
where the leaf was (`language.md` §6).

**Whether this is a finding or a question depends on the scope.** The argument for R22 may be sitting
right there in the closure, and if it is, you can check it:

- **The refiner is in scope.** Some model the named file loads concludes what this leaf asserts. Then
  this is a finding: name that model and its `conclusion` with a `file:line`, and propose the refine.
- **It is not in scope.** Then nothing here can tell you whether it exists, and inventing an answer is
  the failure this rule is most prone to. Report a question instead:

  > The leaf cites `(R22)`. If a requirement argument for R22 exists, this is the place to `refine`
  > against it rather than assert it. Does one?

Either way, do not go looking for `r22.jd` outside the scope. If the author wants that question
answered across a whole corpus, `jpipe-survey` is the skill that does it, and `F01` is the rule.

## C02 · Store the refine in the requirement file, under the reused name

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

Every branch that assembles `r20` now picks up the refined form with no change to the branch file.
The alternative, binding the refine at the branch under a new name like `justified_r20`, works, but
each consuming branch must then know to use the refined name, and one that forgets silently gets the
unrefined argument. jPipe permits it; the house does not do it.

## C05 · Conclude at goal level, never requirement level

A goal justification assembles the requirement arguments that serve it, and concludes at the goal's
own altitude. A requirement file concludes at its requirement. A goal file that concludes at
requirement level has collapsed a layer.

Which kind of file this is comes from the file itself: its provenance header (`C06`) and its name.
A file that says it serves a goal and then concludes at a requirement is the finding.

## C06 · Source every file

Open each `.jd` with a `/** … */` block tracing its argument to the goals, requirements, and
decisions it serves:

```text
/**
 * Requirement argument - REQUIREMENTS.md R9: the system runs on CPU with no GPU and no network.
 * Serves goals: GOALS.md G6 Efficiency / Green AI. Rationale: DECISIONS ADR-003/ADR-004.
 */
```

This is where **backing** goes: the thing Toulmin's model wants and jPipe cannot express
(`abstraction.md` §1). The warrant says *"confront the declared packages with the CPU-only
allowlist"*; what authorizes that particular allowlist lives in the header, as a citation.

Keep the `.jd` at *what is claimed*. The concrete *how it is checked* belongs in the step code.

## C07 · Unification hazard

Not a property of the model, but a property of a **fix you are proposing**. Any change that creates,
destroys, or renames a unified group renumbers every later `unified_N` (`language.md` §7), and those
ids may be referenced by a step library this skill does not read.

Every structural finding carries a cost line, and this is when it must say so explicitly.

---

## Naming

| | Convention | Rationale |
|---|---|---|
| Goal files | carry the goal number, `g2_fates.jd` | the file is the goal |
| Requirement files | goal-agnostic, `requirements/r13.jd` | one requirement serves several goals; naming it after one is a lie the moment a second cites it |
| Model name inside a file | semantic, `justification fairness` in `g2_fates.jd` | the diagram reads better than `g2` |
| Element ids | `c` / `s_*` / `sc_*` / `e_*` | kind is visible at a glance in the relation block |

Element id conventions are the weakest item here. Do not raise a finding for id style alone unless
this file is internally inconsistent, which is the only kind of inconsistency one file can show.

---

## Report shape

These go under 🟡 **Suggestions**: the argument holds and the file departs from house style. Two
exceptions. `C01` moves up to **will not tell you when it breaks** when the leaf is also `A01`, since
it then both asserts a tagged requirement and states a verdict where a fact belongs. `C07` is a
property of a proposed fix rather than a finding, so it appears as a cost line, never its own entry.

Because this whole file is house practice, phrase findings as observations with a rationale rather than
violations, and say plainly that they are declinable. Keep the rationale inside this file too:
*"every other file under `requirements/` has one"* is a claim about a corpus this skill did not read.

```text
### 5. This file does not say which requirement it serves

`requirements/r14.jd:1` · file header

**What's wrong.** No comment block at the top. Nothing connects this model to REQUIREMENTS.md or to
the decisions behind it.

**Why it matters.** Mostly for whoever picks this up in a year, including you. It is also the natural
home for something missing elsewhere: `s_thresh` confronts accuracy with "the 0.8 threshold", and
nothing in the file says where 0.8 came from or who agreed to it.

**Options.**
  **a.** Add a header naming the requirement, the goals it serves, and the decision that fixed 0.8.
  **b.** Leave it, and record the 0.8 rationale wherever your project keeps that instead.
  A convention rather than a defect: take it or leave it.

Cost: a comment  ·  Reference: `[JD-C06]`
```
