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

[`jpipe-review`](../jpipe-review/) examines the elements of one argument. This asks a different question,
about any two elements anywhere in your scope: **what do they each mean, and what does the relation
between them oblige you to do?** There are five answers worth acting on, and each is a different edit:

| Relation | What it looks like | What to do |
|---|---|---|
| **One claim, two wordings** | *"The source is available"* and *"The code is available"*. Neither names a path, so nothing mechanical connects them, and jPipe shares a fact only when two labels match **exactly** | Put both on one wording, and the check runs once for both goals |
| **One leaf, two things** | *"The source and test code are available"*. Unique by construction, because no other model needs exactly that pair, so it can never be shared with anything | Split it. Then the test half is a leaf four other requirements can rest on |
| **An assertion you can already prove** | A bare leaf saying *"The trained model artifact"*, while another model concludes *"The model is trained properly"* | Graft that argument under the leaf with `refine`, instead of taking it as given |
| **One claim, two rungs** | The same comparison written as a `strategy` in one model and an `evidence` in another. One of them cannot fail properly | Named, not fixed. Which rung is right is one model's business, so it goes to `jpipe-review` |
| **Two moments, one subject** | One model treats the metrics as a committed file, another as something a run writes. Compose them and there is no time at which the whole case can be checked | Say when, in the label, or split the case by moment |

There is also the inverse of the first: two leaves with **byte-identical** labels denoting different
things. Composed, they become one node, and that node says something neither file says. It is the one
finding here nobody can decline, because it is what the compiler does.

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

## It ranks, rather than asking

The report opens with the one section most people will finish:

```text
## Worth your time, in order

1. #4  the test suite becomes one leaf instead of three, and its check runs once   high
2. #2  r22's argument goes under a leaf that four goals take on faith              medium
3. #1  stops the composed case claiming one file grounds two unrelated legs        high
```

Ranked by what the corpus gains, not by severity: the one serious finding in a corpus is often a
two-label edit, while the one that restructures three goals is the day's real work. Each finding then
carries what it would touch, including whether a shared node appears or disappears, since that renumbers
every later shared-node id.

**Nothing is asked before the report.** Whether *"The source is available"* and *"The code is available"*
mean one thing is a judgement, and it is stated as one: every finding says how sure the skill is and what
reading it is resting on, in your words rather than in an identity claim it cannot support.

```text
Confidence: medium, both are about the source tree but neither label says which paths
```

That is what makes a finding safe to act on and cheap to overrule. Three consequences worth knowing:
**low confidence never proposes an edit**, only a candidate and what would settle it; a **wrong merge is
worse than a missed one**, so when the reading is doing too much work the skill says so instead of
guessing; and every choice you make in the fix list is recorded under **What you decided**, so a rerun
does not re-propose something you declined.

## It never looks for your files

There is no grounding pass here, and there will not be one. A justification can be discharged at any
point in its life, at design time or from CI, so a file absent from a clean checkout may be git-ignored,
or may simply not exist until a run makes it. **A missing file is never a finding**, because nothing is
ever searched for.

What it does read is what your labels *say* about when their artifacts exist, which is a different and
more useful question: a corpus that disagrees with itself about that is one nobody can execute at either
moment. Where absence genuinely matters, [`jpipe-review`](../jpipe-review/) searches deliberately, records
every pattern it ran, and only reports a concrete committed path that turned up nothing.

## Usage

```
jpipe-survey <path/to/model.jd> [-m <model>] [--global]
```

**Scope** is one `.jd` file plus everything it transitively `load`s. Pass `--global` instead to take
every `.jd` in the repository. Passing no file, or more than one, is an error rather than a guess.

Every rule compares two elements in different models, so the scope needs two or more of them. A file that
loads nothing gives a scope of one, and `--global` is the invocation for a corpus that is not rooted in a
single model.

There are no other flags. `--questions` and `--no-refine` were removed in 0.2.0: nothing is asked any
more, and skipping a rule family turned out to be a setting nobody wanted.

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
| [`semantics.md`](references/semantics.md) | **The method.** Reading a label as a subject and an assertion, the five relations and the order they are tested in, and how confidence is decided |
| [`prove.md`](references/prove.md) | Comb-shaped arguments, and grafting an argument the corpus already contains under a leaf that asserts it |
| [`lifecycle.md`](references/lifecycle.md) | When evidence is supposed to exist, and why absence is never a finding here |
| [`topology.md`](references/topology.md) | The graph rules: files nothing loads, and corpora with two roots |
| [`rules.md`](references/rules.md) | The rule catalogue: id, description, authority, trigger, fix |
| [`report-format.md`](references/report-format.md) | The report's shape, with a worked example |
| [`language.md`](references/language.md) † | The jPipe language, objectively: the two operators, and the `unified_N` renumbering hazard behind every finding here |
| [`artifacts.md`](references/artifacts.md) † | Resolving an evidence label to the thing it names, and why string similarity is not artifact identity |

† Vendored, byte-identical, from the repository's shared [`references/`](../../references/) canon, so
the skill directory stays self-contained and copyable on its own. Edit the canon, not the copy:
see [Shared reference material](../../CONTRIBUTING.md#shared-reference-material).

## On the rule ids

**They changed in 0.2.0, and the old ones are gone for good.** The families are now keyed to the edit a
finding asks for, because that is what you have to decide about: `JD-D` split, `JD-M` merge, `JD-P` prove,
`JD-L` re-level, `JD-N` name, `JD-T` topology.

Twelve ids have been retired across two rounds and none will ever be reused, so four letters are burnt:
`S` and `C` by `jpipe-review`, `R` and `F` here. If you meet `R01` or `F01` in an older report,
[`references/rules.md`](references/rules.md) has the translation table. Two entries in it are not
straight renames, and the difference is the point of the rewrite:

- **`R01` → `M01`** no longer needs a resolvable artifact. It compares what two elements mean, at any
  kind, on a stated reading, so it finds pairs the old rule passed over in silence.
- **`F01` → `P01`** fires when one element would *establish* another rather than restate it. A leaf
  saying *"The trained model artifact"* and a model concluding *"The model is trained properly"* are not
  the same claim, and grafting the second under the first is still right.

`R04` was dropped rather than renamed: with `M01` widened to every kind, two checks saying one thing is
just `M01` between strategies.
