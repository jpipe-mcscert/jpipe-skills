# jpipe-survey

Surveys a whole corpus of jPipe justification models (`.jd`) for what no single file can show.

> [!CAUTION]
> This skill surveys arguments **you** wrote. It does not author assurance cases, and generative AI
> should not be used to write one: text that reads like an argument, produced without anyone having
> reasoned about the system, is worse than no argument at all. Findings here are a language model's
> judgement, documented so you can check them, and nothing is edited without your approval. The
> responsibility for the case stays with you. Experimental, and not part of jPipe core: see the
> [repository README](../../README.md).

## What it does

[`jpipe-review`](../jpipe-review/) reads one model at a time, deliberately. That leaves a class of
question it cannot answer, because the evidence is spread across files:

| | |
|---|---|
| **Shared evidence** | Two goals rest on the same artifact, worded differently. jPipe merges byte-identical labels into one node, so wording is mechanical: worded alike, the check runs once and supports both goals; worded differently, the same work is done twice and the diagram hides it |
| **Accidental merging** | The inverse, and a real defect. Two leaves in different models both say *"the reported metrics"* while denoting different files. Under `assemble` they become one node, and the composed model claims something neither author wrote |
| **Available refinements** | A leaf asserts something another model in the corpus proves with a whole argument. The proof exists and the model declines to use it |
| **Structure** | Models nothing loads, and corpora with two roots where there should be one |

Nothing is edited until you approve a numbered fix list. Every finding names the shared artifact, both
locations, both labels, and its blast radius, because aligning two labels creates a unified group and
renumbers every `unified_N` after it.

## It asks you questions

Whether *"The committed training split"* and *"The train.csv split as committed"* name the same file is
**not in the files**. It is knowledge you have and the corpus does not record. Guessing yes produces a
wrong merge, which is worse than finding nothing: it collapses a distinction you drew on purpose and,
if applied, quietly changes what your case claims.

So the skill asks, in prose, before concluding:

```text
1. Same artifact?
   r13.jd:11  `e_train`  "The committed training split"
   r20.jd:9   `e_data`   "The train.csv split as committed"
   I read both as data/train.csv. If yes, I will align both labels and assemble will unify
   them into one node, so the check runs once for both goals.
```

Answers land in a **Decisions** section of the report, including the ones where you said no, so a later
run does not re-litigate them. At most 7 questions by default (`--questions N` to change it), ordered
by how many models each touches; anything past the budget is reported as an open question rather than
silently dropped. Answer none of them and the report is still useful: every uncertain cluster becomes
an open question and nothing is applied.

## Usage

```
jpipe-survey <target> [--no-refine] [--questions N] [--apply]
```

`<target>` is a directory, a glob, or nothing (the repository root). It needs **two or more** models,
since every rule compares models. Without `--apply` it reports and stops.

Needs [`jpipe`](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH`
(`brew install jpipe`, `apt install jpipe`, or `scoop install mcscert/jpipe`).

## Scope: the corpus, not the argument

This skill says nothing about whether any single model is a good argument. Whether a leaf asserts a
verdict instead of naming a fact, whether one leaf fuses two facts, whether the artifacts named exist
in the tree: all of that is [`jpipe-review`](../jpipe-review/), which reads one model properly rather
than glancing at many. **A CLEAN survey and a CLEAN review are different claims**, and a corpus wants
both.

## Authority: which findings you can argue with

- **`language`**: the compiler decides. Only `R03` is here, and it is not negotiable: the composed
  model already asserts the merge.
- **`house`**: McSCert practice, and *irrelevant* if your project states its own conventions in a
  `CLAUDE.md` or a `justifications/README.md`. Those win.

## Reference material

The `references/` are written to be read by people too, not only loaded by the skill:

| | |
|---|---|
| [`sharing.md`](references/sharing.md) | Finding facts argued twice, and why clustering by artifact beats clustering by string |
| [`refinement.md`](references/refinement.md) | When a leaf should refine against an argument the corpus already contains, and where the refine belongs |
| [`interview.md`](references/interview.md) | The question mechanism: what to ask, what never to ask, and why the budget is small |
| [`rules.md`](references/rules.md) | The rule catalogue: id, description, authority, trigger, fix |
| [`report-format.md`](references/report-format.md) | The report's shape, with a worked example |
| [`language.md`](references/language.md) † | The jPipe language, objectively: the two operators, and the `unified_N` renumbering hazard behind every finding here |
| [`artifacts.md`](references/artifacts.md) † | Resolving an evidence label to the thing it names, and why string similarity is not artifact identity |

† Vendored, byte-identical, from the repository's shared [`references/`](../../references/) canon, so
the skill directory stays self-contained and copyable on its own. Edit the canon, not the copy:
see [Shared reference material](../../CONTRIBUTING.md#shared-reference-material).

## On the rule ids

`jpipe-review` once carried an `S01`-`S04` sharing family and retired it when it narrowed to one model.
Retired ids are never reused, so the same checks live here under `JD-R`, and the corpus-structure
checks it retired as `C03`/`C04` live here under `JD-F`. `references/rules.md` has the translation
table, in case you meet an older report.

`F01` is the one that is genuinely new rather than renamed. `jpipe-review`'s `C01` could only ask
*"if an argument for R22 exists, refine against it. Does one?"*, because it cannot look. This skill
looks.
