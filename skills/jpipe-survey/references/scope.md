# Scope: which models are being compared

Read this at Step 1, before resolving anything, and again at Step 5 if `-m` was passed.

Every rule in this skill is a claim about **two models**, so the first thing it has to get right is
which models are in and which are out. A finding stated across a boundary nobody drew is a false
positive, and two of those cost the reader their trust in the whole report.

---

## 1. Three scopes, and the flag that picks one

| Invocation | Scope | Resolved by |
|---|---|---|
| `<file.jd>` | every model that file declares, plus every model in the files it transitively `load`s | following `load` until nothing new appears |
| `<file.jd> -m <model>` | `<model>` plus every model it is **built from**, transitively | following operator sources from `<model>` |
| `--global` | every model in every `.jd` in the repository | `Glob` for `*.jd` |

`-m` is jPipe's own spelling, from `jpipe process -m <model> -i <file>`, and it means the same thing
here: of the models this file makes available, that one.

**`-m` and `--global` contradict each other**, one naming a single model and the other refusing to name
any. Passing both is an error: say so and stop.

## 2. `load` resolves names. Under `-m` it does not set the scope

This is the distinction the flag exists for.

A `load` makes a model's name available to the loading file. It does not say the loaded model belongs to
any particular argument. A file that loads eight requirement models to compose two goals from four each
has eight models in its namespace and two arguments in its contents, and those are different numbers.

So under `-m` the load closure is still the **search space**: it is how you find where the sources are
declared, and reading a file to find a source is not the same as putting that file's other models in
scope. The scope is the model closure of §3, which is narrower.

Without `-m` the two coincide often enough for the difference to stay invisible: one goal per file,
everything loaded is something composed. They come apart the moment a file declares two roots, and that
file is the reason to pass `-m`.

## 3. The model closure

From `<model>`, take what it is built from, and repeat until nothing new appears:

| Declaration | Sources |
|---|---|
| `justification X is assemble(a, b, c) { … }` | `a`, `b`, `c` |
| `justification X is refine(base, refiner) { … }` | `base` and `refiner` |
| `justification X implements T { … }` | `T`, whose elements are part of `X` |
| `justification X { … }` | none. A leaf, and the closure ends here |

Operators **cannot nest** (`language.md` §6), so composing a composition means naming the intermediate
and using that name as a source. Every edge of this graph therefore runs between two **named** models,
which is what makes following it cheap: the declaration headers harvested at Step 2 hold all of it, and
no file has to be read to walk it.

Take the closure of a **name**, never of a file. Two models declared side by side in one file are
unrelated unless an operator connects them, and that is true however adjacent they look.

## 4. Errors, and the one non-error worth saying out loud

- **No file, or more than one.** An error, and the oldest one here: a directory or a glob used to be
  accepted and is not, because a scope assembled by wildcard is a scope nobody chose.
- **`-m` naming a model the file does not declare.** An error. List what the file declares, since the
  usual cause is a typo or a half-remembered name. If the name is declared elsewhere in the load
  closure, say which file and that pointing at *that* file is the invocation they want: a model is
  scoped from the file that declares it, not from one that happens to load it.
- **`-m` given twice, or with `--global`.** An error. Do not pick one.
- **`-m` naming a leaf model**, built from no sources. Not an error, and not silent either: the scope is
  one model, so no rule here can fire. Say that, and say the two ways on (drop `-m` for the file's other
  models, or `--global` for the repository).

## 5. Attribution: which model does an element belong to?

Under `-m` this stops being optional. "In scope" is now a property of a **model**, while the harvest
returns **elements**, and `file:line` no longer settles it: one file can hold a model in the closure and
a model outside it.

So the Step 2 harvest takes in declaration headers alongside elements, and every element belongs to the
nearest `justification` or `template` header above it in the same file.

Two rules already needed this and were quietly getting it from one-model-per-file corpora:

- **`F01`** matches an evidence label against a conclusion label **in a different model**. Same model,
  and it is one argument's own internal shape, which is `jpipe-review`'s business rather than this
  skill's.
- **`R01` and `R03`** are claims about two models. Two identical labels inside one model are one author
  repeating themselves, not two wordings that drifted apart, so there is nothing to align and nobody to
  ask.

## 6. What a narrower scope changes about the rules

Two `JD-F` rules are answers to *"is this model reachable?"*, and `-m` answers that by construction:

- **`F03` (orphan model) cannot fire under `-m`.** Every model in the closure is reachable from the one
  you named, because that is what put it there, and every unreachable model is out of scope. The rule
  has nothing left to find but itself.
- **`F04` (multiple entry points) cannot fire under `-m`.** You named the entry point. There is one root
  in scope by definition.

Put both in **Not looked at** rather than dropping them silently, because a file declaring two roots is
exactly where `F04` has something to say, and `-m` is exactly the flag that hides it.

One rule gets **sharper** instead, and it is the one nobody can decline:

> **`R03` needs a model that composes both sides.** Byte-identical labels merge when they land in one
> composed model. In two models never composed together the merge simply never happens, so there the
> finding is not weaker, it is wrong.

Under `-m` that condition holds by construction: the closure is one composition and you named it.
Without `-m` it has to be checked, and the check is the graph from §3, walked from every model in scope:
one of them must have both sides in its closure. If none does, the identical labels are a hazard waiting
for a composition nobody has written, which is an open question and not a 🔴.

## 7. Say the scope back to them

The report's opening lines name it: the model surveyed, the models in its closure, and, where `-m`
narrowed things, the models declared in the file that were left out. A reader who cannot tell which of
their models were compared cannot tell what a CLEAN verdict covers, and under `-m` the honest answer is
*one of your arguments*. → `report-format.md`
