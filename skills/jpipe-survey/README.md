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

[`jpipe-review`](../jpipe-review/) examines the elements of one argument. That leaves a class of
question it does not answer, because it is about how separate arguments relate:

| | |
|---|---|
| **Shared evidence** | Two goals rest on the same artifact, worded differently. jPipe merges byte-identical labels into one node, so wording is mechanical: worded alike, the check runs once and supports both goals; worded differently, the same work is done twice and the diagram hides it |
| **Accidental merging** | The inverse, and a real defect. Two leaves in different models both say *"the reported metrics"* while denoting different files. Under `assemble` they become one node, and the composed model claims something neither author wrote |
| **Available refinements** | A leaf asserts something another model in the corpus proves with a whole argument. The proof exists and the model declines to use it |
| **Structure** | Models nothing loads, and corpora with two roots where there should be one |

Nothing is edited until you approve a numbered fix list.

## The report is written for you, not for a safety auditor

Findings are phrased for **the engineer who built the system**. No internal rule names, no severity
jargon, and no compiler vocabulary: nothing in a report should require you to look up what "unify"
means. Each finding gives you three things:

1. **What's wrong**, naming both places and quoting both labels.
2. **Why it matters**, in terms of your system: work done twice, a check that will not run once, or a
   claim the composed case makes that neither of your files says.
3. **Your options**, usually more than one, with the trade-off named and a recommendation. You choose.

Rule ids appear once, at the end of each finding, because people cite them in review threads. They are
a reference number, never the explanation.

Duplication is normal, and the report says so. Two engineers writing two goals months apart will word
the same fact differently; that is the absence of a mechanism, not carelessness, and supplying the
mechanism is what this skill is for.

## It asks you questions

Whether *"The committed training split"* and *"The train.csv split as committed"* name the same file is
**not in the files**. It is knowledge you have and the corpus does not record. Guessing yes produces a
wrong merge, which is worse than finding nothing: it collapses a distinction you drew on purpose and,
if applied, quietly changes what your case claims.

So the skill asks, in prose, before concluding:

```text
1. Are these the same file?
   requirements/r13.jd:11  `e_train`  "The committed training split"
   requirements/r20.jd:9   `e_data`   "The train.csv split as committed"
   I read both as data/train.csv. If that is right, I will put both on one wording, and the
   two become a single box when the models are composed, so whatever checks the training
   split runs once instead of twice.
```

Answers land in a **What you told me** section of the report, including the ones where you said no, so a
later run does not re-litigate them. At most 7 questions by default (`--questions N` to change it), ordered
by how many models each touches; anything past the budget is reported as an open question rather than
silently dropped. Answer none of them and the report is still useful: every uncertain cluster becomes
an open question and nothing is applied.

## Usage

```
jpipe-survey <path/to/model.jd> [-m <model>] [--global] [--no-refine] [--questions N]
```

**Scope** is one `.jd` file plus everything it transitively `load`s. Pass `--global` instead to take
every `.jd` in the repository. Passing no file, or more than one, is an error rather than a guess.

Every rule compares models, so the scope needs two or more of them. A file that loads nothing gives a
scope of one, and `--global` is the invocation for a corpus that is not rooted in a single model.

### `-m`: one argument out of a file that holds several

A `load` makes a model's name available. It does not make that model part of your argument. So a file
that loads eight requirements and composes two goals from four each has eight models in scope and two
arguments in the file, and surveying it whole compares models you never put together:

```text
justification fairness   is assemble(r13, r20) { ... }
justification efficiency is assemble(r31, r32) { ... }
```

`-m fairness` scopes the survey to `fairness` and the models it is built from, following `assemble`,
`refine` and `implements` sources as far as they go. `r31` and `r32` are then out, and the report says
so by name.

It is jPipe's own flag, spelled the same as in `jpipe process -m <model> -i <file>`, and it changes two
findings rather than just narrowing the search:

- Identical labels in two models only merge when something composes them, so under `-m` a merge hazard
  is a fact about your argument instead of a possibility about two files that may never meet.
- Files nothing loads, and corpora with two roots, stop being reportable: you named the root, so
  everything in scope is reachable from it. Run without `-m` when that is the question you have.

`-m` and `--global` contradict each other and passing both is an error, as is naming a model the file
does not declare.

Reporting needs no tools at all: the survey runs on a `grep` over label declarations, which works
whether or not the files parse. Approving a fix needs
[`jpipe`](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH` (`brew install jpipe`,
`apt install jpipe`, or `scoop install mcscert/jpipe`), to recompile and re-render what it edited.

## Scope: the corpus, not the argument

This skill says nothing about whether any single model is a good argument. Whether a leaf asserts a
verdict instead of naming a fact, whether one leaf fuses two facts, whether the artifacts named exist
in the tree: all of that is [`jpipe-review`](../jpipe-review/), which reads one model properly rather
than glancing at many. **A CLEAN survey and a CLEAN review are different claims**, and a corpus wants
both.

## Which findings you can argue with

Every finding says, in plain words, how much room you have to disagree. Here there are two kinds:

- **The compiler decides.** Exactly one finding is this: two identical labels *will* become one node
  when the models are composed, so there is nothing to agree or disagree with.
- **Everything else is a proposal**, whether an opportunity to share work or a convention about
  placement. Decline any of it. Conventions are *irrelevant* if your project states its own in a
  `CLAUDE.md` or a `justifications/README.md`; those win.

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
