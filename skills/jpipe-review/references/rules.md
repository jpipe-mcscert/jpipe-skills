# Rule catalogue

The lookup table. Every finding cites an id from here **and quotes its description**, because a bare
`JD-A01` means nothing to an author who has not read this file, and a report they cannot read without
a lookup table is a report they will not read. Every id also carries an **authority** saying what
backs it, which decides whether the author can decline it.

The **Description** column is the line the report quotes: short enough for a header, and phrased so
the finding is comprehensible without opening this catalogue. **Trigger** is for you, deciding whether
the rule fires at all.

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

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| A01 | claim-as-evidence | A leaf asserts a verdict where it should name an artifact | A leaf asserts a judgement rather than naming an artifact: *"a … check passes"*, *"… confirms …"*, *"… is computed correctly"*, *"X is a Y"*. Test: could it be false in a way that needs reasoning to discover? | Single-leg: reword the leaf down to its artifact, move the judgement into the existing strategy. Multi-leg: give the leg its own `sub-conclusion` + `strategy` | 🟠 |
| A02 | warrant-without-inference | A strategy that does not license the step it sits on | A strategy names an artifact, restates the claim, or gives a title (*"Testing argument"*) instead of licensing a step | State what is confronted with what, and what would have to hold | 🟠 |
| A03 | missing-intermediate-claim | A leg reaches a verdict that nothing writes down | Independent legs wire straight into the top strategy with no `sub-conclusion`; a failing leg cannot be localised | Add one `sub-conclusion` per leg, each with its own strategy | 🟠 |
| A04 | claim-restates-warrant | A conclusion and its strategy say the same thing | A conclusion and the strategy beneath it say the same thing | Rewrite the strategy to say *how*, not *what* | 🟠 |
| A05 | non-atomic-evidence | One leaf names two independent facts | One leaf names two or more independent artifacts. Test: would splitting force two different checks? | Split into one leg per artifact. Fix before grounding: a fused leaf has no single artifact to search for | 🟠 |
| A06 | unfalsifiable-warrant | A check with no observable pass or fail | The check has no observable pass/fail: *"the approach is sound"* | Name the artifact, the comparison, and what would count as failure | 🟠 |

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
| C01 | should-be-refine | A leaf asserts a tagged requirement instead of refining against it | A leaf carries a requirement tag (house tell: a trailing `(Rnn)`), so the author has written down that a requirement is what makes it true | `refine(base, refiner) { hook: "<leaf-id>" }`. Report as a question: whether an argument for that requirement exists is not visible from here | 🟡 (🟠 if also A01) |
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
