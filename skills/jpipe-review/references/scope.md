<!-- CANON: /references/scope.md. Do not edit a vendored copy; edit the canon and run tools/sync_refs.py. -->

# Which models are in scope

**Authority: `language`.** What a model is built from is in the grammar, so the closure below is not a
convention anyone can prefer differently. The three invocations that select one are this toolchain's
contract rather than the compiler's, but what each of them resolves to is the language's business.

It is shared because both skills stand or fall on the same boundary:

| Question | Asked by | What the scope decides |
|---|---|---|
| *Is this element doing its job?* | review | which elements are examined at all |
| *Do these two name the same thing?* | survey | which pairs are eligible to be compared |

Get it wrong and the two failures differ in shape but not in cost. A finding stated outside the scope is
one the reader never asked for; a scope quietly wider than the one they named makes the verdict cover
something they cannot see. Both spend the same thing, which is their willingness to read the next
report.

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
which is what makes following it cheap: a declaration header carries the whole of it, and no file body
has to be read to walk it.

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
- **`-m` naming a leaf model**, built from no sources. Not an error, and whether it is worth remarking on
  depends on the skill: a scope of one model is a full scope for anything that examines elements, and no
  scope at all for anything that compares models.

## 5. Attribution: which model does an element belong to?

Under `-m` this stops being optional. "In scope" is now a property of a **model**, while a label harvest
returns **elements**, and `file:line` no longer settles it: one file can hold a model in the closure and
a model outside it.

An element belongs to the nearest `justification` or `template` header above it in the same file. So
whatever collects elements collects those headers too, in the same pass and in line order, or it cannot
say which model anything is in.

Without `-m` this is invisible, because a corpus of one model per file makes *file* and *model* the same
key. That is a property of those corpora and not of the language, and it stops holding the first time
somebody writes two `justification` blocks in one file.

## 6. Rules that turn on the scope

A rule whose subject is *whether a model is reachable* asks a question `-m` has already answered, so
under that flag it cannot fire: everything in scope is reachable from the model that was named, and
everything unreachable is outside. Retiring such a rule is not a loss of coverage, it is the flag doing
what it was asked. Say so where the report lists what it did not look at, because the invocation that
hides these rules is exactly the one where they had something to say.

A rule whose subject is *what happens when elements land in one composed model* gets sharper instead.
Under `-m` the composition is named, so the answer is a fact about that model rather than a possibility
about files that may never meet.

Which of a skill's rules fall in either group is a property of the rule, so its own `rules.md` says.

## 7. Say the scope back to them

The report's opening lines name it: the models in scope, and, where `-m` narrowed things, the models
declared in the file that were left out. A reader who cannot tell which of their models were looked at
cannot tell what a clean verdict covers, and under `-m` the honest answer is *one of your arguments*.
→ `report-format.md`
