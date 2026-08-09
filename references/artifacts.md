<!-- CANON: /references/artifacts.md. Do not edit a vendored copy; edit the canon and run tools/sync_refs.py. -->

# What does this label denote?

**Authority: `argument`.** An `evidence` label is prose written for a human. Before anything can be
done with it mechanically, it has to be resolved to **the thing it names**. This file is that one
step, and nothing else.

It is shared because two different questions turn out to need the same answer:

| Question | Asked by | What it does with the artifact |
|---|---|---|
| *Does this exist?* | grounding | searches the repository for it |
| *Have I seen this one before?* | sharing | clusters leaves that name the same one |

Both read the same noun phrase, and both are wrong in the same way if they read it carelessly. Keeping
the extraction in one place is what keeps the two answers consistent.

---

## 1. Extract the artifact

Read the label and ask what thing it names. The artifact is usually a noun phrase with a possessive
or a qualifier:

| Label | Artifact |
|---|---|
| "The committed Pipfile and its `[packages]` dependency table" | `Pipfile`, section `[packages]` |
| "The committed pipeline source: the `src/` package and the `run_v*.py` entry points" | `src/`, `run_v*.py` |
| "The committed train, test and counterfactual CSV splits and their header rows" | `data/*.csv` (three of them) |
| "The CI run record for the release commit and its coverage job log" | a CI artifact, **likely not in the tree** |
| "The fitted classifier" | a *produced* thing, not a committed one |

Two labels denote the same artifact when they resolve to the same row of that right-hand column, and
**the words on the left are not evidence either way**. This is the single most important property of
the extraction, and §3 is about why.

## 2. Classify what kind of thing it is

The kind decides what can be done with the artifact, and what its absence would mean.

- **Committed path**: a file or directory expected in the tree. `Glob` for it.
- **Path with an internal section**: a file plus a named part (`[packages]`, a heading, a symbol).
  `Glob` for the file, then `Grep` inside it for the section.
- **Named symbol**: a function, class, or config key. `Grep` the tree.
- **Produced artifact**: something a run creates (`model/metrics.json`, a fitted pipeline). It may be
  git-ignored and legitimately absent from a clean checkout, so it resolves to **what produces it**.
  If that is ambiguous, the extraction failed: say so rather than guessing.
- **External**: a hosted record, a published standard, a third-party dataset. **Out of reach.**
  Nothing can be concluded from its absence in a repository.
- **None**: the label names nothing inspectable at all. Not an artifact, and not a candidate for any
  question above.

## 3. String similarity is not artifact identity

Wording and denotation come apart in both directions, and a method that compares strings gets both
cases exactly backwards:

- *"the training split"* and *"the training configuration"* share four of five words and denote
  entirely different things.
- *"The committed Pipfile and its `[packages]` dependency table"* and *"the dependency manifest as
  committed"* share almost nothing and denote the same file.

So resolve first, then compare **artifacts**. Never compare labels.

## 4. When the extraction fails

It often will, and that is not a defect in the model. A label may be too vague to resolve, or resolve
to several candidates at once, or name something out of reach.

> **An unresolved label is an open question, never a finding.**

Whatever is downstream of this file, it inherits that rule: a conclusion drawn from a noun phrase
nobody could pin down is a guess wearing a rule id. Say what the label says, say what could not be
pinned down, and let the author settle it.

A fused label, one naming two or more independent artifacts, is a special case of failure: there is no
single artifact to return. Split the leaf first; then each half extracts cleanly.
