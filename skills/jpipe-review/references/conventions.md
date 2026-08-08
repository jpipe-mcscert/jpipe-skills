# Corpus conventions

**Authority: `house`.** McSCert practice for organising a corpus of justification files. The most
local and most declinable of the three reference tiers. A project that does things differently is
not wrong, it is different. Say so in the report rather than asserting these as rules.

Promoted from `jpipe-tutorial-2026/CLAUDE.md` §Justifications and
`jpipe-tutorial-2026/justifications/README.md`. Read at Step 5.

**Before raising any finding here, check whether the project has its own stated conventions**: a
`CLAUDE.md`, a `justifications/README.md`, a contributing guide. If it does, that document wins, and
these conventions are irrelevant. Only fall back on this file when the corpus has no stated practice
of its own.

---

## C01 · A leaf that restates another argument's conclusion should be a refine

The signature case. An evidence leaf says something another model in the corpus already argues for.
Written as a bare leaf, it asserts what could be established: the corpus contains a proof and
declines to use it.

The house tell is a trailing requirement tag in the label: `"… is the full 27-cell identity grid (R22)"`
where `r22.jd` exists and concludes exactly that.

The fix is `refine(base, refiner) { hook: "<leaf-id>" }`, which grafts the refiner's whole argument
where the leaf was (`language.md` §6).

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

## C03 · Conclude at goal level, never requirement level

A goal justification assembles the requirement arguments that serve it, and concludes at the goal's
own altitude. A requirement file concludes at its requirement. A goal file that concludes at
requirement level has collapsed a layer.

## C04 · One entry point

Exactly one model is the root: the one that is compiled, rendered, and (when bindings exist)
executed. Other goal models are sub-trees, compiled for viewing but never run separately.

This is not tidiness. `assemble` renames elements under the parent namespace, so binding at the root
means each node is renamed **once**; binding per-goal duplicates every shared node and multiplies the
work. Two roots over the same sub-trees is the tell.

## C05 · Orphan models

A model that nothing loads, assembles, implements, or refines is dead. Usually one of: a draft left
behind, a model whose consumer was renamed, or a genuine entry point that should be documented as
such. Report it as a question rather than a defect, since you cannot tell which from the corpus
alone.

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

Every structural finding carries a blast-radius line, and this is when it must say so explicitly.

---

## Naming

| | Convention | Rationale |
|---|---|---|
| Goal files | carry the goal number, `g2_fates.jd` | the file is the goal |
| Requirement files | goal-agnostic, `requirements/r13.jd` | one requirement serves several goals; naming it after one is a lie the moment a second cites it |
| Model name inside a file | semantic, `justification fairness` in `g2_fates.jd` | the diagram reads better than `g2` |
| Element ids | `c` / `s_*` / `sc_*` / `e_*` | kind is visible at a glance in the relation block |

Element id conventions are the weakest item here. Do not raise a finding for id style alone unless
the corpus is otherwise consistent and one file departs from it.

---

## Report shape

Conventions are 🟡 **CONVENTION**: the model is fine on its own and sits oddly in the corpus. Two
exceptions escalate: `C01` reaches 🟠 when the leaf is also `A01` (it restates a conclusion *and*
is a verdict in a grounds slot), and `C07` is a property of a proposed fix rather than a finding, so
it appears as a blast-radius line, never as its own entry.

Because this whole file is house practice, phrase findings as observations with a rationale, not as
violations:

```text
**C1 · `[JD-C06 missing-header]` · requirements/r14.jd:1**
No `/** */` provenance header. Every other file under `requirements/` has one tracing its
argument to REQUIREMENTS.md and the decisions behind it; this one is the exception.
→ Worth adding, and it is where the backing for `s_thresh`'s 0.8 threshold belongs: the
  warrant cites the number but nothing says what authorizes it.
```
