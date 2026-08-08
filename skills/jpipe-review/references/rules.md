# Rule catalogue

The lookup table. Every finding cites an id from here, and every id carries an **authority** saying
what backs it, which decides whether the author can decline it.

Every rule here is decidable from **one model**: the file under review and the files it `load`s. A
question that needs a second model is not in this catalogue, by construction.

| Authority | Backed by | Declinable? |
|---|---|---|
| `language` | the grammar and the compiler | No; the model will not build, or already claims something unintended |
| `argument` | Toulmin's model of argument (`abstraction.md`) | Yes, with a rationale |
| `house` | McSCert house practice (`conventions.md`) | Yes, and irrelevant if the project states its own conventions |

Severity is about whether the argument survives, not about how much work the fix is:

| | | |
|---|---|---|
| 🔴 | **UNSOUND** | The argument does not support its claim, or asserts something nobody wrote |
| 🟠 | **ABSTRACTION** | It holds, but an element sits at the wrong rung |
| 🟡 | **CONVENTION** | The argument is fine; the file departs from house style |

---

## JD-A · abstraction & atomicity, *authority: argument* → `abstraction.md`

| Id | Name | Trigger | Typical fix | Sev |
|---|---|---|---|---|
| A01 | claim-as-evidence | A leaf asserts a judgement rather than naming an artifact: *"a … check passes"*, *"… confirms …"*, *"… is computed correctly"*, *"X is a Y"*. Test: could it be false in a way that needs reasoning to discover? | Single-leg: reword the leaf down to its artifact, move the judgement into the existing strategy. Multi-leg: give the leg its own `sub-conclusion` + `strategy` | 🟠 |
| A02 | warrant-without-inference | A strategy names an artifact, restates the claim, or gives a title (*"Testing argument"*) instead of licensing a step | State what is confronted with what, and what would have to hold | 🟠 |
| A03 | missing-intermediate-claim | Independent legs wire straight into the top strategy with no `sub-conclusion`; a failing leg cannot be localised | Add one `sub-conclusion` per leg, each with its own strategy | 🟠 |
| A04 | claim-restates-warrant | A conclusion and the strategy beneath it say the same thing | Rewrite the strategy to say *how*, not *what* | 🟠 |
| A05 | non-atomic-evidence | One leaf names two or more independent artifacts. Test: would splitting force two different checks? | Split into one leg per artifact. Fix before grounding: a fused leaf has no single artifact to search for | 🟠 |
| A06 | unfalsifiable-warrant | The check has no observable pass/fail: *"the approach is sound"* | Name the artifact, the comparison, and what would count as failure | 🟠 |

## JD-G · grounding, *authority: argument* → `grounding.md`

| Id | Name | Trigger | Typical fix | Sev |
|---|---|---|---|---|
| G01 | artifact-absent | A concrete token was searched for and nothing plausible exists in the tree | Correct the label, or add the artifact | 🔴 |
| G02 | artifact-stale | Nothing matches, but a near-match exists under a different name, i.e. a rename the label missed | Label-only; report the candidates, do not guess | 🔴 |
| G03 | no-artifact-named | The leaf names nothing inspectable at all | Usually co-occurs with A01/A06; fix the abstraction first | 🟠 |
| G04 | check-not-performable | The artifact exists, but the strategy's check cannot be carried out against it | Either the leg needs a different ground, or the warrant is about the wrong thing | 🔴 |

**Discipline:** a grounding finding must name what was searched for and where. No search, no
finding; it is an open question. Never report against `steps/` or outside the repository root.

## JD-C · conventions, *authority: house* → `conventions.md`

| Id | Name | Trigger | Typical fix | Sev |
|---|---|---|---|---|
| C01 | should-be-refine | A leaf carries a requirement tag (house tell: a trailing `(Rnn)`), so the author has written down that a requirement is what makes it true | `refine(base, refiner) { hook: "<leaf-id>" }`. Report as a question: whether an argument for that requirement exists is not visible from here | 🟡 (🟠 if also A01) |
| C02 | refine-not-in-requirement-file | The refine is bound at a branch under a new name instead of exported from the requirement file under the reused name | Move it; consumers then need no change | 🟡 |
| C05 | concludes-below-goal-level | A goal file concludes at requirement altitude | Raise the conclusion to the goal | 🟡 |
| C06 | missing-header | No `/** */` block tracing the argument to its goals / requirements / decisions | Add one. This is also where **backing** belongs | 🟡 |
| C07 | unification-hazard | *A property of a proposed fix*: it creates, destroys, or renames a unified group and renumbers every later `unified_N` | Not a standalone finding; appears as a blast-radius line | n/a |

**Before raising any JD-C finding**, check whether the project states its own conventions
(`CLAUDE.md`, `justifications/README.md`, a contributing guide). If it does, that document wins.

---

## Retired ids

Never reused, so a rule id cited anywhere always means one thing. These were removed when the skill
became single-model: each needed to read a `.jd` other than the one under review, which this skill
does not do.

- **The whole `S01`–`S04` family**, sharing & reuse: duplicate facts, shared legs, accidental
  unification, redundant checks. Every one of them compares two models.
- **`C03`**, orphan-model. *Nothing loads this model* cannot be decided without reading everything
  that might.
- **`C04`**, multiple-entry-points. Needs the set of all roots.

The `C` numbering keeps its gaps rather than closing them, so `C05` still means what it always meant.

`S03` is the substantive loss and worth naming: identical labels on different artifacts **do** merge
under `assemble` into a node nobody wrote, and nothing here will catch it. It is a real hazard that
this skill is the wrong shape to find.

## What is *not* in this catalogue

Syntax, unresolved symbols, cycles, missing operator keys, illegal support pairings, duplicate ids,
un-overridden `@support`, broken `load`s. All of it is caught by `jpipe diagnostic` and the VS Code
extension, with better locations than a reader will produce.

The compile gate reports *that* a file does not build and stops. It never re-explains, ranks, or
catalogues what the compiler already said. `language.md` §8 lists that territory so you can recognise
and stay off it.

## Ordering findings

Within the report, order by severity, then by blast radius ascending. The suggested **fix** order is
different, and it is a dependency order rather than an importance order:

1. 🔴 UNSOUND: nothing else is trustworthy while the argument rests on a hole
2. **A05 atomicity splits**: first among the 🟠, because the atoms they produce are what the other
   findings are then written against
3. zero-blast-radius rewords: A01 single-leg, A02, A04
4. structural: A03, C01/C02; recompile and re-render after each
