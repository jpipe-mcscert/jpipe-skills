<!-- CANON: /references/language.md. Do not edit a vendored copy; edit the canon and run tools/sync_refs.py. -->

# The jPipe language

**Authority: `language`.** Everything here is defined by the grammar and enforced by the compiler.
It is not a matter of opinion: where this file and a preference disagree, the model does not build.

Sourced from `JPipe.g4` (ANTLR, `jpipe-compiler/jpipe-lang/src/main/antlr4/ca/mcscert/jpipe/lang/`),
`jpipe.langium` (`jpipe-vscode/packages/language/src/`), and `jpipe-compiler/docs/design/`.
Verified against jpipe 2.3.1.

---

## 1. File structure

A `.jd` file is one or more of: `load`, `justification`, `template`. Whitespace and newlines are
insignificant. Comments are `//` to end of line and `/* … */`.

Identifiers are `[A-Za-z_][A-Za-z0-9_]*`. Labels are single- or double-quoted and **may not contain a
newline**. There is no escape syntax, so a label cannot contain its own quote character; switch
quote style instead.

---

## 2. Elements

Every element declaration has the same shape:

```
<kind> <qualified_id> is "<label>"
```

| Kind | Meaning | Where legal |
|---|---|---|
| `conclusion` | what the model asserts | justification, template |
| `sub-conclusion` | an intermediate assertion inside the model | justification, template |
| `strategy` | the reasoning step | justification, template |
| `evidence` | the ground the argument rests on | justification, template |
| `@support` | an abstract placeholder to be overridden | **template only** |

A justification must have exactly one `conclusion`. A template that declares no `@support` leaves
implementors nothing to override; the editor validator warns.

## 3. The support relation

There is exactly one relation:

```
<from> supports <to>
```

Read it as *"from supports to"*: the supporter is on the **left**. The compiler accepts only these
combinations (`docs/design/language.md` §Support edges):

| Supporter | Supportable |
|---|---|
| `evidence` | `strategy` |
| `sub-conclusion` | `strategy` |
| `@support` | `strategy` |
| `strategy` | `conclusion` |
| `strategy` | `sub-conclusion` |

The consequence worth internalising: **every step in a jPipe argument passes through a `strategy`.**
Evidence never attaches directly to a conclusion, and a conclusion is never supported by anything but
a strategy. The language enforces a strict alternation between assertions and the reasoning that
reaches them.

A minimal well-formed model:

```jd
justification minimal {
  conclusion c is "The release is ready"
  strategy   s is "All release gates pass"
  evidence   e is "The committed CHANGELOG.md and its Unreleased section"
  s supports c
  e supports s
}
```

## 4. Qualified ids

An id is either a bare name (`s`) local to its model, or a colon-separated path
(`template:s`, `namespace:Model:s`). Qualified ids are how cross-model references work: overriding a
template's `@support`, referencing an element in a loaded namespace, or naming an element inside a
composed model.

**The common mistake:** overriding an abstract support with an unqualified id. The override key must
name the template:

```jd
template quality {
  conclusion ready is "The release is ready"
  strategy   gates is "All release gates pass"
  @support   tested is "Testing is demonstrated"
  gates supports ready
  tested supports gates
}

justification readiness implements quality {
  sub-conclusion quality:tested is "The code is tested"
  strategy       testing        is "The suite covers the changed paths"
  evidence       suite          is "The committed tests/ directory and its last CI run record"
  testing supports quality:tested
  suite   supports testing
}
```

`quality:tested`, not `tested`. The unqualified form is
`jpipe-compiler/examples/invalid/008_unknown_override_target.jd`.

An `@support` may only be overridden by an `evidence` or a `sub-conclusion`.

## 5. `load`

```
load "path.jd"
load "path.jd" as ns
```

Paths are relative to the loading file. Glob patterns are supported (`load "g[1-7]_*.jd"`,
`load "requirements/*.jd"`). Without `as`, symbols land flat in the current scope, so two loaded
files declaring the same model name collide. With `as ns`, they are reachable as `ns:Model:element`.

A `load` failure is **fatal**: the compiler aborts before the model is built, and, importantly for
tooling, reports **entirely on stderr**. Verified on 2.3.1: stdout is completely empty, not even the
`=== Diagnostics ===` header, and the exit code is `1`. Anything that reads only stdout will call a
file with a broken `load` clean. Load cycles are detected and rejected the same way.

## 6. Composition operators

```
justification <id> is <operator>(<source>, …) { key: "value" … }
```

Operators **cannot be nested**. To compose a composition, name the intermediate result and use it as
a source. `012_chaining_operators.jd` in the compiler examples is the reference for this.

### `assemble(s₁, …, sₙ) { conclusionLabel: "…" strategyLabel: "…" }`

Both keys are **required**. Each source's `conclusion` is demoted to a `sub-conclusion`; all of them
are wired through one synthesized `strategy` (id `assembleStrategy`) beneath one synthesized
`conclusion` (id `assembleConclusion`), labelled from the two keys. Every other element is copied
with a source-prefixed id. The result is a `template` if any source is a template.

```jd
justification tested {
  conclusion c is "The changed paths are covered by tests"
  strategy   s is "Confront the coverage report's per-file figures with the changed file list; none is below the threshold"
  evidence   e is "The committed coverage report and the diff of the release branch"
  s supports c
  e supports s
}

justification documented {
  conclusion c is "The release is documented"
  strategy   s is "Confront the CHANGELOG's Unreleased entries with the merged pull requests; each user-facing change appears"
  evidence   e is "The committed CHANGELOG.md and the list of pull requests merged since the last tag"
  s supports c
  e supports s
}

justification top is assemble(tested, documented) {
  conclusionLabel: "The system is fit to release"
  strategyLabel:   "Every release gate holds"
}
```

### `refine(base, refiner) { hook: "<element-id>" }`

`hook` is **required**. It names an element **in `base`**, and the refiner's whole argument is grafted
where that element was: the hooked element and the refiner's conclusion merge into a single
`SubConclusion` whose id is the hook's. Everything else is copied under `sourceName:elementId`.

The hook value is a **colon-qualified element id**, not a path:

```jd
justification base {
  conclusion c is "The release is fit to ship"
  strategy   s is "Confront the release checklist with the repository state; every gate is met"
  evidence   e_cov is "The committed coverage report and its per-file figures"
  s supports c
  e_cov supports s
}

justification refiner {
  conclusion c is "The committed coverage report and its per-file figures"
  strategy   s is "Confront the CI run record with the coverage job's exit status; the report was produced by a green run on the release commit"
  evidence   e is "The CI run record for the release commit and its coverage job log"
  s supports c
  e supports s
}

justification refined is refine(base, refiner) { hook: "e_cov" }
```

Note that `refiner`'s conclusion is written to **match the label of the hooked element**, and that
is what makes the graft read continuously rather than splicing an unrelated claim into the tree.

When `base` was itself composed so its elements carry a source prefix, the hook takes the qualified
form: `hook: "first:e"`.

> **Erratum.** `jpipe-compiler/docs/design/operators.md` documents the hook as
> `"modelName/elementId"` with a slash. That form does not appear in any working example; the
> compiler's own `examples/009_refine.jd` uses `hook: "e"` and `examples/012_chaining_operators.jd`
> uses `hook: "first:e"`. Follow the examples.

The typical reason to refine: an evidence leaf in `base` restates the conclusion of another argument.
Rather than asserting it, graft the argument that establishes it.

## 7. Unification: read this before proposing any label change

After **any** operator runs, the compiler applies a post-composition pass (`Unifier`). Result
elements that are equivalent are merged into a single synthesized element with id `unified_N`, where
**N is a 0-based counter assigned in encounter order**. All original ids are aliased to it and
support edges are rewritten and deduplicated.

| Config key | Default | Meaning |
|---|---|---|
| `unifyBy` | `"sameLabel"` | the equivalence relation; `sameLabel` compares label strings exactly |
| `unifyExclude` | *(empty)* | comma-separated result-element ids to exempt |

Three consequences follow, and they are the reason label wording is load-bearing rather than cosmetic:

1. **Identical labels merge.** By default, two elements anywhere in a composed model with
   byte-identical labels become one node. This is the mechanism that lets a check run once and
   support two goals, and also the mechanism by which two unrelated facts silently become one
   claim.
2. **Near-identical labels do not.** `sameLabel` is exact string equality. One differing article
   or a trailing period is enough to prevent sharing.
3. **`unified_N` numbering is positional.** Adding, removing, or renaming a unified group
   renumbers every later one. The `.jd` diff can look trivial while every downstream `unified_N`
   reference shifts, and those ids may be referenced from outside the model entirely, by bindings in
   a Python step library. A one-line label edit is therefore never guaranteed to be a one-line change.

## 8. What the compiler already checks

`jpipe diagnostic` and the VS Code extension cover all of the following, with better locations than a
reader will produce. It is listed here so it can be recognised as already-covered ground.

*Consistency:* duplicate ids, cycles in the support graph, cycles in `implements`.
*Completeness:* a conclusion is present, and conclusions / strategies / sub-conclusions are supported;
a justification has no `@support` left un-overridden; a template has at least one.
*Structure:* unknown symbols, illegal supporter/supportable pairings, unknown operators, missing or
unknown operator config keys, unknown `unifyBy` methods, unknown hook elements, duplicate model names,
unresolvable / self / circular / non-matching `load`s, and references into a template.

The compiler's negative-test corpus, one mistake per file, is
`jpipe-compiler/examples/invalid/`, and the valid counterparts are one directory up.
