# Rule catalogue

**This file is for you, not for the reader of the report.** It is the lookup table that decides whether a
rule fires and what to propose. Almost none of its vocabulary belongs in a report: the person reading that
is the engineer who built the system, and they have no reason to know what `M01` means or what "unify" is.
→ `report-format.md`, which is about writing for them.

Every rule here needs **at least two elements in different models** to state, except `N01`, which needs a
composition. That is the whole point of this skill and also its risk: a claim about two models is twice as
easy to get wrong as a claim about one.

**The families are keyed to the edit**, because that is what the reader has to decide about:

| Family | The relation that fires it | The edit | Method |
|---|---|---|---|
| `JD-D` **split** | one element claims two separately checkable things | decompose it | `semantics.md` §3.1 |
| `JD-M` **merge** | one claim under two wordings | align or extract | `semantics.md` §3.3 |
| `JD-P` **prove** | one element would establish another's assertion | graft with `refine` | `prove.md` |
| `JD-L` **re-level** | one claim written as two different kinds | move one rung | `semantics.md` §3.2 |
| `JD-N` **name** | the labels disagree about when the artifact exists | say when | `lifecycle.md` |
| `JD-T` **topology** | the graph, not the elements | rewire or document | `topology.md` |

Which models are eligible at all is `scope.md`. Three rules turn on it: `M03` needs a model that composes
both sides, while `T01` and `T02` cannot fire under `-m`.

| Column | For |
|---|---|
| **Trigger** | you, deciding whether the rule fires |
| **Description** | you, as the one-line summary. Do not paste it into a report as an explanation; say what is wrong with *their* elements instead |
| **Typical fix** | the starting point for the options you offer, never the whole of them |

| Authority | Declinable? | Say to the reader |
|---|---|---|
| `language` | No | "this is what the compiler does when it composes them, so there is nothing to agree or disagree with" |
| `argument` | Yes, with a rationale | "this is a judgement about the argument; disagree and it stands" |
| `house` | Yes, and irrelevant if the project states its own conventions | "a convention rather than a defect: take it or leave it" |

Severity is about whether the argument survives, not about how much work the fix is. The right-hand column
is what a report says out loud; the middle column never appears in one:

| | Internal | In the report |
|---|---|---|
| 🔴 | UNSOUND | **Composing these models makes a claim nobody wrote** |
| 🟠 | STRUCTURE | **The argument is shallower than the corpus can support** |
| 🔵 | REUSE | **The same work is being done twice.** An opportunity, never a defect |
| 🟡 | CONVENTION | **Suggestions.** Fine as it stands; these would make the corpus easier to live with |

---

## JD-D · split, *authority: house* → `semantics.md` §3.1

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| D01 | fused-leaf-blocks-sharing | A leaf names two things, and one of them would merge with another model's | An `evidence` label names two separately checkable things, **and** a named element elsewhere matches one of them | Split into one leg per thing, then align the matching half with the partner | 🔵 |
| D02 | fused-check-blocks-sharing | A strategy runs two checks, one of which another model also runs | A `strategy` performs two independent checks, **and** a named strategy elsewhere performs one of them | Split into one leg per check; the parent strategy then says why the legs are jointly sufficient | 🔵 |

**Discipline:** never report either without naming the partner. A fused element with no partner is
`jpipe-review`'s `A05` or `A07`, decidable from one file, and restating it here duplicates that skill while
adding nothing. The test for fusion is *would splitting force two different checks?*, so a conjunction on
its own is not the tell.

## JD-M · merge → `semantics.md` §3.3

Mixed authority, so it is per row rather than per family.

| Id | Name | Description | Authority | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|---|
| M01 | same-proposition | Two elements of one kind make one claim in two wordings | house | Same subject and, on a stated reading, one assertion. Any kind, and neither label need name a path | Align both on one wording; `assemble` then merges them into one `unified_N` | 🔵 |
| M02 | duplicated-leg | The same fact, check and verdict is argued in two models | house | A whole `fact → check → verdict` triple repeats in two or more models | Extract into a requirement model; the others `refine` at their leaf (`prove.md` `P02`) | 🔵 |
| M03 | accidental-unification | Identical labels name different things and will silently merge | **language** | Byte-identical labels in two models denote different things, **and a model in scope composes both**. Absent that, nothing merges: report it as a candidate, not a defect | Disambiguate the labels (`unifyExclude` only as a workaround) | 🔴 |

**Discipline:** an `M01` or `M02` finding quotes both labels in full and states the reading that makes them
one claim. Align **leaves only**: the same fact legitimately grounds different checks, so two strategies
above a merged leaf usually both stay. `N02` on a pair **blocks** `M01` on it.

## JD-P · prove, *authority: house* → `prove.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| P01 | assertion-with-proof-available | A bare leaf asserts something a model here would establish | Some model's `conclusion`, if true, would be a reason to believe this leaf. A matching `(Rnn)` tag is the strongest signal, not a precondition | `refine(base, refiner) { hook: "<leaf-id>" }`, checking the direction first | 🟠 |
| P02 | refine-placement | A refine is bound at the branch, not the requirement file | Bound under a new name at a consumer instead of exported from the requirement file under the reused name | Move it; consumers then need no change | 🟡 |

**Discipline:** `P01` names the model and the `conclusion` that would prove the leaf, with its `file:line`.
"Something here probably argues this" is not a finding. Check the direction: if the other conclusion is the
weaker statement, refining is backwards.

## JD-L · re-level, *authority: argument* → `semantics.md` §3.2

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| L01 | same-proposition-wrong-kind | One claim appears as two different kinds in two models | The same proposition is a `strategy` in one model and an `evidence`, `conclusion` or `sub-conclusion` in another | **Name the discrepancy only.** Which rung is right is one model's internal shape, so hand the re-level to `jpipe-review` | 🟠 |

**Discipline:** this is the one rule that proposes no edit. Say which of the two looks wrong and why, and
stop. Proposing the fix would mean judging one model on its own, which is the line this skill does not
cross.

## JD-N · name, *authority: house* → `lifecycle.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| N01 | untimed-composition | One composed model rests on leaves that exist at different moments | A composition's leaves span two or more of *now* / *after a run* / *elsewhere*, and no label says so | Put the moment in the labels, or divide the argument so each part is discharged at its own time | 🟠 |
| N02 | kind-inconsistent-subject | Two models disagree about when one subject exists | One subject is a committed path in one model and a produced artifact in another | Settle which it is. The `M01` merge on that pair becomes available afterwards | 🟠 |
| N03 | blocks-comparison | A label naming nothing inspectable stopped a comparison | A leaf has no extractable subject, **and** that is why some comparison could not be made | Point at `jpipe-review`, which decides what a leaf should name. Never restate its rule | 🟡 |

**Discipline: never look for the artifact.** No `Glob`, no `Grep`, not to confirm a finding and not to
raise confidence. A case may be discharged from CI, so an absent file may be git-ignored or may not exist
until a run makes it, and absence is never a finding here (`lifecycle.md` §2).

## JD-T · topology, *authority: house* → `topology.md`

| Id | Name | Description | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| T01 | orphan-model | Nothing in the scope loads, assembles, refines or implements this model | No `load`, `assemble` source, `refine` source or `implements` anywhere in scope names it. **Never under `-m`** | Report as a question: a draft, a stale consumer, or an undocumented entry point | 🟡 |
| T02 | competing-roots | Two roots over overlapping sources | Two models are each a root, over source sets that overlap. **Never under `-m`** | Pick one root; the others become sub-trees | 🟡 |

**Discipline:** say what you looked at and over what. The graph is complete only for the scope, so outside
a rooted scope or `--global`, a model composed by a script looks exactly like an orphan.

---

## Ids this skill must never mint

Twelve retired ids, and retired ids are never reused (`CONTRIBUTING.md`). Four letters are burnt: `S` and
`C` by `jpipe-review`, `R` and `F` here. Several rules above are the same *check* under a new id,
deliberately, because the families are now keyed to the edit rather than to "reuse versus structure".

| Retired | Now | Why it is not a straight rename |
|---|---|---|
| `S01`, then `R01` | `M01` | No longer needs a resolvable artifact. Any kind, on a stated reading, at a stated confidence |
| `S02`, then `R02` | `M02` | unchanged in substance |
| `S03`, then `R03` | `M03` | Now requires a model that composes both sides, so an unreachable collision is a candidate rather than a defect |
| `S04`, then `R04` | `M01` | **Not carried over as its own id.** Two strategies making one claim is `M01` between strategies, and a separate rule for it was double bookkeeping |
| `C01`, then `F01` | `P01` | Fires on *establishes* rather than on identity, so it catches leaves no same-proposition test would |
| `C02`, then `F02` | `P02` | unchanged in substance |
| `C03`, then `F03` | `T01` | unchanged in substance |
| `C04`, then `F04` | `T02` | Now explicitly requires the source sets to overlap |

Never write those ids in a report, prefixed or not. If an author cites one at you it came from a report
predating 0.2.0, and the table above is the translation.

## What is *not* in this catalogue

**Anything decidable from one model.** Whether a leaf asserts a verdict, whether one strategy is
unfalsifiable, whether a leg is missing its `sub-conclusion`, whether the artifacts named exist in the
tree: all of it belongs to `jpipe-review`, which reads one model properly rather than glancing at many. Do
not restate its findings, even when a pass here makes one obvious. `D01`, `D02`, `L01` and `N03` all sit
next to one of its rules and are separated from it by a hard condition: a named partner, or a blocked
comparison.

Syntax, unresolved symbols, cycles, operator errors and broken `load`s belong to `jpipe diagnostic` and the
VS Code extension (`language.md` §8). Nothing is compiled here until something has been edited, and a label
declaration is comparable whether or not its file parses.

## Ordering

**In the report, order by impact**, then by confidence, then by severity. That is what the reader is
deciding with, and `report-format.md` puts it in a list up front.

**The fix order is different, and it is a dependency order:**

1. 🔴 `M03`: the composed model currently claims something nobody wrote.
2. `N02`: settle it, which unblocks any `M01` on the same pair.
3. `D01` and `D02` splits: they unblock the merges beneath them.
4. `M01` alignments: each creates a shared node, so re-render before judging the next.
5. `P01` grafts: structural, at least two files each. One at a time, recompiling after each.
6. `M02` extractions: the largest blast radius, and easier once `M01` has settled the wording.
7. `N01`, `P02`, `T01`, `T02`: labels, placement and tidiness, last.

`L01` never appears in a fix list here. It is handed to `jpipe-review`.
