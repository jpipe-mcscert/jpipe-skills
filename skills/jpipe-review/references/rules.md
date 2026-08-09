# Rule catalogue

**This file is for you, not for the reader of the report.** It is the lookup table that decides whether
a rule fires and what to propose. Almost none of its vocabulary belongs in a report: the person reading
that is the engineer who built the system, and they have no reason to know what a warrant is or what
`A05` means. → `report-format.md`, which is about writing for them.

Every rule here is decidable **within the scope**, and the scope is `scope.md`: the named file's closure,
one model's closure under `-m`, or the repository under `--global`. That is one argument, however many
files it spans. A rule that would need to *compare* two arguments is not in this catalogue, by
construction, and being able to read a loaded file does not make comparing it fair game.

One rule turns on which of those was chosen. `C01` is a **finding** when the model that proves the tagged
requirement is in scope and a **question** when it is not, so `-m` can turn one back into the other by
leaving that model outside. Everything else here is decided from a single element and its neighbours.

| Column | For |
|---|---|
| **Trigger** | you, deciding whether the rule fires |
| **Description** | you, as the one-line summary of what the rule is about. Do not paste it into the report as an explanation; say what is wrong with *their* element instead |
| **Typical fix** | the starting point for the options you offer. **Where it says decompose, decomposing is the recommendation**, not one alternative among two |

| Authority | Backed by | Declinable? | Say to the reader |
|---|---|---|---|
| `language` | the grammar and the compiler | No | "the compiler will do this whether or not you agree" |
| `argument` | Toulmin's model of argument (`abstraction.md`) | Yes, with a rationale | "this is a judgement about the argument; disagree and it stands" |
| `house` | McSCert house practice (`conventions.md`) | Yes, and irrelevant if the project states its own conventions | "a convention, take it or leave it" |

Severity is about whether the argument survives, not about how much work the fix is. The right-hand
column is what a report says out loud; the middle column never appears in one:

| | Internal | In the report |
|---|---|---|
| 🔴 | UNSOUND | **The argument does not hold.** Someone could read this and be reassured by nothing |
| 🟠 | ABSTRACTION | **The argument will not tell you when it breaks.** It holds today and cannot report its own failure |
| 🟡 | CONVENTION | **Suggestions.** The argument is fine; this would make it easier to live with |

---

## JD-A · abstraction & atomicity, *authority: argument* → `abstraction.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| A01 | claim-as-evidence | A leaf asserts a verdict where it should name an artifact | A leaf asserts a judgement rather than naming an artifact: *"a … check passes"*, *"… confirms …"*, *"… is computed correctly"*, *"X is a Y"*. Test: could it be false in a way that needs reasoning to discover? | Rests on more than one thing: **decompose** into a leg per thing, each with its own `sub-conclusion` + `strategy`. Rests on exactly one: reword the leaf down to its artifact and move the judgement into the existing strategy | 🟠 |
| A02 | warrant-without-inference | A strategy that does not license the step it sits on | A strategy names an artifact, restates the claim, or gives a title (*"Testing argument"*) instead of licensing a step | State what is confronted with what, and what would have to hold | 🟠 |
| A03 | missing-intermediate-claim | A leg reaches a verdict that nothing writes down | Independent legs wire straight into the top strategy with no `sub-conclusion`; a failing leg cannot be localised | Add one `sub-conclusion` per leg, each with its own strategy | 🟠 |
| A04 | claim-restates-warrant | A conclusion and its strategy say the same thing | A conclusion and the strategy beneath it say the same thing | Rewrite the strategy to say *how*, not *what* | 🟠 |
| A05 | non-atomic-evidence | One leaf names two independent facts | One leaf names two or more independent artifacts. Test: would splitting force two different checks? | **Decompose** into one leg per artifact; no wording makes one leaf two facts. Fix before grounding: a fused leaf has no single artifact to search for | 🟠 |
| A06 | unfalsifiable-warrant | A check with no observable pass or fail | The check has no observable pass/fail: *"the approach is sound"* | Name the artifact and the comparison; a comparison is falsifiable by construction, so do not append the verdict | 🟠 |
| A07 | non-atomic-strategy | One strategy performs two independent checks | Two checks joined by "and", a semicolon or a "then". Test: would this check still make sense with half of it deleted? | **Decompose**: one leg per check, and the parent strategy then states why the legs are jointly sufficient | 🟠 |

## JD-G · grounding, *authority: argument* → `grounding.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| G01 | artifact-absent | The evidence names something the repository does not contain | A concrete token was searched for and nothing plausible exists in the tree | Correct the label, or add the artifact | 🔴 |
| G02 | artifact-stale | The label missed a rename; a near-match exists under another name | Nothing matches, but a near-match exists under a different name, i.e. a rename the label missed | Label-only; report the candidates, do not guess | 🔴 |
| G03 | no-artifact-named | The leaf names nothing anyone could inspect | The leaf names nothing inspectable at all | Usually co-occurs with A01/A06; fix the abstraction first | 🟠 |
| G04 | check-not-performable | The artifact exists, but the check cannot be run against it | The artifact exists, but the strategy's check cannot be carried out against it | Either the leg needs a different ground, or the warrant is about the wrong thing | 🔴 |

**Discipline:** a grounding finding must name what was searched for and where. No search, no
finding; it is an open question. Never report against `steps/` or outside the repository root.

## JD-C · conventions, *authority: house* → `conventions.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| C01 | should-be-refine | A leaf asserts a tagged requirement instead of refining against it | A leaf carries a requirement tag (house tell: a trailing `(Rnn)`), so the author has written down that a requirement is what makes it true | `refine(base, refiner) { hook: "<leaf-id>" }`. A finding when the model that proves the requirement is in scope, a question when it is not | 🟡 (🟠 if also A01) |
| C02 | refine-not-in-requirement-file | The refine is bound at the branch instead of the requirement file | The refine is bound at a branch under a new name instead of exported from the requirement file under the reused name | Move it; consumers then need no change | 🟡 |
| C05 | concludes-below-goal-level | A goal file concludes at requirement altitude | A goal file concludes at requirement altitude | Raise the conclusion to the goal | 🟡 |
| C06 | missing-header | No provenance header tracing the argument to what it serves | No `/** */` block tracing the argument to its goals / requirements / decisions | Add one. This is also where **backing** belongs | 🟡 |
| C07 | unification-hazard | A proposed fix that renumbers `unified_N` downstream | *A property of a proposed fix*: it creates, destroys, or renames a unified group and renumbers every later `unified_N` | Not a standalone finding; appears as a blast-radius line | n/a |

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

None of this is a gap in the review. These are corpus questions, and they belong to `jpipe-survey`,
which reads a whole corpus, rather than to a reviewer holding one file. Its `JD-R` and `JD-F` families
are where these checks live now, and its `rules.md` carries the translation table.

## What is *not* in this catalogue

Syntax, unresolved symbols, cycles, missing operator keys, illegal support pairings, duplicate ids,
un-overridden `@support`, broken `load`s. All of it is caught by `jpipe diagnostic` and the VS Code
extension, with better locations than a reader will produce.

This review does not compile the model at all until it has edited it, so it has nothing to say about
whether the file builds and should never imply otherwise. `language.md` §8 lists that territory so you
can recognise and stay off it.

## Ordering findings

Within the report, order by severity, then by blast radius ascending. The suggested **fix** order is
different, and it is a dependency order rather than an importance order:

1. 🔴 first: nothing else is trustworthy while the argument rests on a hole
2. **Decompositions, A05 then A07**: first among the 🟠, because the legs they produce are what every
   other finding is then written against. A05 before A07: split the leaf, and the checks follow it
3. zero-blast-radius rewords: A01 where it rests on one thing, A02, A04, A06
4. remaining structure: A03, C01/C02; recompile and re-render after each
