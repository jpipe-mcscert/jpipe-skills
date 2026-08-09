# Rule catalogue

**This file is for you, not for the reader of the report.** It is the lookup table that decides whether
a rule fires and what to propose. Almost none of its vocabulary belongs in a report: the person reading
that is the engineer who built the system, and they have no reason to know what `R01` means or what
"unify" is. → `report-format.md`, which is about writing for them.

Every rule here needs **at least two models** to state. That is the whole point of this skill, and it
is also its risk: a claim about two files is twice as easy to get wrong as a claim about one.

| Column | For |
|---|---|
| **Trigger** | you, deciding whether the rule fires |
| **Description** | you, as the one-line summary of what the rule is about. Do not paste it into the report as an explanation; say what is wrong with *their* two elements instead |
| **Typical fix** | the starting point for the options you offer, never the whole of them |

| Authority | Declinable? | Say to the reader |
|---|---|---|
| `language` | No | "this is what the compiler does when it composes them, so there is nothing here to agree or disagree with" |
| `house` | Yes, and irrelevant if the project states its own conventions | "a convention rather than a defect: take it or leave it" |

Severity is about whether the argument survives, not about how much work the fix is. The right-hand
column is what a report says out loud; the middle column never appears in one:

| | Internal | In the report |
|---|---|---|
| 🔴 | UNSOUND | **Composing these models makes a claim nobody wrote** |
| 🟠 | STRUCTURE | **An argument the corpus already contains is being asserted instead** |
| 🔵 | REUSE | **The same work is being done twice.** An opportunity, never a defect |
| 🟡 | CONVENTION | **Suggestions.** Fine as it stands; these would make the corpus easier to live with |

---

## JD-R · reuse & sharing → `sharing.md`

Mixed authority, so it is per row rather than per family.

| Id | Name | Description | Authority | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|---|
| R01 | duplicate-fact-not-unified | Two leaves name the same artifact but will not unify | house | Same artifact under drifted labels, confirmed by the author | Align both labels on one wording; `assemble` then merges them into one `unified_N` | 🔵 |
| R02 | extract-shared-leg | The same fact, check and verdict is argued in two models | house | A whole `fact → check → verdict` triple repeats in ≥2 models | Extract into a requirement model; the others `refine` at their leaf (`refinement.md` F02) | 🔵 |
| R03 | accidental-unification | Identical labels name different things, and will silently merge | **language** | Byte-identical labels in ≥2 models denote different artifacts | Disambiguate the labels (`unifyExclude` only as a workaround) | 🔴 |
| R04 | redundant-check | Two warrants run the same check on one datum | house | Two strategies perform the same comparison on the same artifact in different words | Usually resolves once the leaves unify; rarely worth a structural change | 🔵 |

**Discipline:** an `R01`/`R02` finding must name the shared artifact and quote both labels in full.
Cluster by artifact, never by string similarity (`artifacts.md` §3).

## JD-F · refinement & structure, *authority: house* → `refinement.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| F01 | should-be-refine | A leaf asserts what another model in the corpus proves | An evidence leaf states a claim that some model's `conclusion` establishes, and that model exists here | `refine(base, refiner) { hook: "<leaf-id>" }` | 🟠 |
| F02 | refine-not-in-requirement-file | A refine is bound at the branch, not the requirement file | Bound under a new name at a consumer instead of exported from the requirement file under the reused name | Move it; consumers then need no change | 🟡 |
| F03 | orphan-model | Nothing in the corpus loads, assembles, or refines this model | No `load`, `assemble` source, `implements` or `refine` anywhere names it | Report as a question: a draft, a stale consumer, or an undocumented entry point | 🟡 |
| F04 | multiple-entry-points | Two roots compose the same sub-trees | Two models are each a root over an overlapping set of sources | Pick one root; the others become sub-trees | 🟡 |

**Discipline:** `F01` must name the model and the `conclusion` that proves the leaf, with its
`file:line`. "Something probably argues this" is an open question.

**Before raising any JD-F finding**, check whether the project states its own conventions
(`CLAUDE.md`, `justifications/README.md`, a contributing guide). If it does, that document wins.

---

## Ids this skill must never mint

`jpipe-review` retired `S01`-`S04`, `C03` and `C04` when it narrowed to one model, and retired ids are
never reused (`CONTRIBUTING.md`). Several rules here are the same *checks* under new ids, deliberately:

| Retired | Now | Why it is not a straight rename |
|---|---|---|
| `S01` | `R01` | Now confirmed by asking the author, not inferred |
| `S02` | `R02` | unchanged in substance |
| `S03` | `R03` | unchanged in substance |
| `S04` | `R04` | unchanged in substance |
| `C01` | `F01` | The reviewer could only ask *"does an argument for R22 exist?"*. Here it is answered, so this is a finding rather than a question |
| `C03` | `F03` | unchanged in substance |
| `C04` | `F04` | unchanged in substance |

Never write those ids in a report, prefixed or not. If an author cites one at you, it came from a
`jpipe-review` report predating 0.1.1, and the table above is the translation.

## What is *not* in this catalogue

**Anything decidable from one model.** Abstraction, atomicity, whether a leaf asserts a verdict,
whether the artifacts it names exist in the tree: all of it belongs to `jpipe-review`, which reads one
model properly rather than glancing at many. Do not restate its findings here, even when a survey pass
makes one obvious.

Syntax, unresolved symbols, cycles, operator errors and broken `load`s belong to `jpipe diagnostic`
and the VS Code extension (`language.md` §8). This skill does not compile anything until it has edited
something, and a label declaration clusters whether or not its file parses.

## Ordering findings

Within the report, order by severity, then by how many models a finding touches, descending: a
misalignment across four goals is worth more than one across two.

The suggested **fix** order is different, and it is a dependency order:

1. 🔴 `R03`: the composed model currently claims something nobody wrote
2. `R01` label alignments: each creates a unified group, so re-render before judging the next
3. `F01` refinements: structural, one file at a time, recompile after each
4. `R02` extractions: the largest blast radius, and usually easier once `R01` has settled the wording
5. 🟡 `F02`-`F04` and `R04`: placement and tidiness, last
