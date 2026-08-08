# jpipe-review

Reviews the *argument* in an existing jPipe justification model (`.jd`).

> [!DANGER]
> This skill reviews an argument **you** wrote. It does not author assurance cases, and generative
> AI should not be used to write one: text that reads like an argument, produced without anyone
> having reasoned about the system, is worse than no argument at all. Findings here are a language
> model's judgement, documented so you can check them, and nothing is edited without your approval.
> The responsibility for the case stays with you. Experimental, and not part of jPipe core: see the
> [repository README](../../README.md).

## What it does

The compiler and the VS Code extension already catch syntax, unresolved symbols, cycles, and missing
operator keys, with better line numbers than a language model will produce. This skill deliberately
does none of that. It compiles the model once as a **gate**, and if it builds, asks the five
questions no tool asks:

| | |
|---|---|
| **Abstraction** | Is each element at the right level? `evidence` should supply a datum, `strategy` should license an inference, `conclusion` should assert the claim. A leaf reading *"a schema check passes"* asserts the verdict its own leg exists to reach, so the argument proves itself |
| **Atomicity** | One leaf, one fact. *"The Pipfile and the pipeline source"* is two facts fused: one check cannot test both, and neither half can be shared |
| **Grounding** | Does the repository actually contain what the evidence names? A renamed file leaves an argument that still compiles, still renders, and is quietly false |
| **Reuse** | Is the same fact argued twice under different words? jPipe merges identical labels into one node, so sharing is mechanical: worded alike, a check runs once and supports two goals; worded differently, the work is done twice |
| **Conventions** | Does the model sit right in the surrounding corpus? |

Nothing is edited until you approve a numbered fix list. Every finding carries a rule id, a
`file:line:col`, the proposed replacement, and a blast-radius line, because a one-word label edit
can renumber every `unified_N` downstream.

## Usage

```
jpipe-review <target> [--corpus <dir>] [--no-grounding] [--apply]
```

`<target>` is a `.jd` file, a directory, a glob, or nothing (the `.jd` files changed in your working
tree). Without `--apply` it reports and stops.

Needs [`jpipe`](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH`
(`brew install jpipe`, `apt install jpipe`, or `scoop install mcscert/jpipe`).

## Authority: which findings you can argue with

Every finding says what backs it, so you can tell a fact from an opinion:

- **`language`**: the compiler decides. Not negotiable.
- **`argument`**: the Toulmin reading below. Declinable, with a rationale.
- **`house`**: McSCert corpus practice, and *irrelevant* if your project states its own conventions
  in a `CLAUDE.md` or a `justifications/README.md`. Those win.

## Reference material

The `references/` are written to be read by people too, not only loaded by the skill:

| | |
|---|---|
| [`language.md`](references/language.md) | The jPipe language, objectively: elements, the `supports` relation and its legal pairings, `load`, templates, the two operators, and the `unified_N` renumbering hazard |
| [`abstraction.md`](references/abstraction.md) | The argument model: Toulmin's claim / grounds / warrant mapped onto jPipe's kinds, the fact → check → verdict ladder, atomicity, and the category errors |
| [`grounding.md`](references/grounding.md) | Checking evidence against the tree, and the discipline that keeps it from crying wolf |
| [`sharing.md`](references/sharing.md) | Finding facts argued twice, and why clustering by artifact beats clustering by string |
| [`conventions.md`](references/conventions.md) | McSCert corpus practice: refine placement, one entry point, provenance headers |
| [`rules.md`](references/rules.md) | The rule catalogue: id, authority, trigger, fix |
| [`report-format.md`](references/report-format.md) | The findings report's shape, with a worked example |

## On the argument model

Mapping jPipe onto Toulmin is **this repository's contribution**, not a claim about the language
designers' intent, and neither Toulmin nor GSN is referenced anywhere else in the ecosystem. It
earns its place by making the rules explainable instead of merely asserted: *"this leaf is bad"*
becomes *"this is a Claim written into a Grounds slot"*, which tells you what to do about it. It
also replaces the concept's previous informal name, *altitude*.

Worth knowing up front: jPipe's own documentation uses `evidence e is "Test suite passes"` in its
worked example, which this reading flags. Optimising a language tour for brevity is fair; it just
makes a poor argument, and an author who followed the tutorial did the reasonable thing.
