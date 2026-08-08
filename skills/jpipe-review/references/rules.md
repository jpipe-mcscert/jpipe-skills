# Rule catalogue

The lookup table. Every finding cites an id from here, and every id carries an **authority** saying
what backs it — which decides whether the author can decline it.

| Authority | Backed by | Declinable? |
|---|---|---|
| `language` | the grammar and the compiler | No — the model will not build, or already claims something unintended |
| `argument` | Toulmin's model of argument (`abstraction.md`) | Yes, with a rationale |
| `house` | McSCert corpus practice (`conventions.md`) | Yes — and irrelevant if the project states its own conventions |

Severity is about whether the argument survives, not about how much work the fix is:

| | | |
|---|---|---|
| 🔴 | **UNSOUND** | The argument does not support its claim, or asserts something nobody wrote |
| 🟠 | **ABSTRACTION** | It holds, but an element sits at the wrong rung |
| 🔵 | **REUSE** | An opportunity, never a defect |
| 🟡 | **CONVENTION** | Fine alone; sits oddly in the corpus |

---

## JD-A · abstraction & atomicity — *authority: argument* → `abstraction.md`

| Id | Name | Trigger | Typical fix | Sev |
|---|---|---|---|---|
| A01 | claim-as-evidence | A leaf asserts a judgement rather than naming an artifact: *"a … check passes"*, *"… confirms …"*, *"… is computed correctly"*, *"X is a Y"*. Test: could it be false in a way that needs reasoning to discover? | Single-leg — reword the leaf down to its artifact, move the judgement into the existing strategy. Multi-leg — give the leg its own `sub-conclusion` + `strategy` | 🟠 |
| A02 | warrant-without-inference | A strategy names an artifact, restates the claim, or gives a title (*"Testing argument"*) instead of licensing a step | State what is confronted with what, and what would have to hold | 🟠 |
| A03 | missing-intermediate-claim | Independent legs wire straight into the top strategy with no `sub-conclusion`; a failing leg cannot be localised | Add one `sub-conclusion` per leg, each with its own strategy | 🟠 |
| A04 | claim-restates-warrant | A conclusion and the strategy beneath it say the same thing | Rewrite the strategy to say *how*, not *what* | 🟠 |
| A05 | non-atomic-evidence | One leaf names two or more independent artifacts. Test: would splitting force two different checks? | Split into one leg per artifact. **Blocks any JD-S finding on that leaf** | 🟠 |
| A06 | unfalsifiable-warrant | The check has no observable pass/fail: *"the approach is sound"* | Name the artifact, the comparison, and what would count as failure | 🟠 |

## JD-G · grounding — *authority: argument* → `grounding.md`

| Id | Name | Trigger | Typical fix | Sev |
|---|---|---|---|---|
| G01 | artifact-absent | A concrete token was searched for and nothing plausible exists in the tree | Correct the label, or add the artifact | 🔴 |
| G02 | artifact-stale | Nothing matches, but a near-match exists under a different name — a rename the label missed | Label-only; report the candidates, do not guess | 🔴 |
| G03 | no-artifact-named | The leaf names nothing inspectable at all | Usually co-occurs with A01/A06 — fix the abstraction first | 🟠 |
| G04 | check-not-performable | The artifact exists, but the strategy's check cannot be carried out against it | Either the leg needs a different ground, or the warrant is about the wrong thing | 🔴 |

**Discipline:** a grounding finding must name what was searched for and where. No search, no
finding — it is an open question. Never report against `steps/` or outside the repository root.

## JD-S · sharing & reuse → `sharing.md`

| Id | Name | Authority | Trigger | Typical fix | Sev |
|---|---|---|---|---|---|
| S01 | duplicate-fact-not-unified | house | Two leaves denote the same artifact under drifted labels, so they will not unify | Align the labels; `assemble` then merges them into one `unified_N` | 🔵 |
| S02 | extract-shared-leg | house | The same `fact → check → verdict` appears in ≥2 models | Extract into a requirement model; the others `refine` at their leaf (`conventions.md` C02) | 🔵 |
| S03 | accidental-unification | **language** | Identical labels denote **different** artifacts — they *will* merge into a claim nobody wrote | Disambiguate the labels (`unifyExclude` only as a workaround) | 🔴 |
| S04 | redundant-check | house | Two warrants run the same check on the same datum in different words | Usually resolves once the leaves unify | 🔵 |

**Discipline:** an S01/S02 finding must name the shared artifact and quote both labels in full.
Cluster by artifact, never by string similarity.

## JD-C · conventions — *authority: house* → `conventions.md`

| Id | Name | Trigger | Typical fix | Sev |
|---|---|---|---|---|
| C01 | should-be-refine | A leaf restates a conclusion another model in the corpus argues for (house tell: a trailing `(Rnn)` tag) | `refine(base, refiner) { hook: "<leaf-id>" }` | 🟡 (🟠 if also A01) |
| C02 | refine-not-in-requirement-file | The refine is bound at a branch under a new name instead of exported from the requirement file under the reused name | Move it; consumers then need no change | 🟡 |
| C03 | orphan-model | Nothing loads, assembles, implements, or refines this model | Report as a question — a draft, a stale consumer, or an undocumented entry point | 🟡 |
| C04 | multiple-entry-points | Two roots over the same sub-trees; nodes get renamed and bound more than once | Pick one root; the others become sub-trees | 🟡 |
| C05 | concludes-below-goal-level | A goal file concludes at requirement altitude | Raise the conclusion to the goal | 🟡 |
| C06 | missing-header | No `/** */` block tracing the argument to its goals / requirements / decisions | Add one. This is also where **backing** belongs | 🟡 |
| C07 | unification-hazard | *A property of a proposed fix*: it creates, destroys, or renames a unified group and renumbers every later `unified_N` | Not a standalone finding — appears as a blast-radius line | — |

**Before raising any JD-C finding**, check whether the project states its own conventions
(`CLAUDE.md`, `justifications/README.md`, a contributing guide). If it does, that document wins.

---

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

1. 🔴 UNSOUND — nothing else is trustworthy while the argument rests on a hole
2. **A05 atomicity splits** — before any reuse finding, because a fused leaf has no atom to match
3. zero-blast-radius rewords — A01 single-leg, A02, A04
4. 🔵 REUSE alignment — after the splits, before extraction
5. structural — A03, S02, C01/C02; recompile and re-render after each
