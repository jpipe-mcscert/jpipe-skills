# How the models are wired together

**Authority: `house`.** Two rules, both about the shape of the corpus graph rather than about what any
element says. Both are 🟡, both are declinable, and both are the cheapest findings in the skill: they come
straight off the graph Step 2's harvest already produced.

Read this at Steps 3 and 4.

---

## Neither fires under `-m`

Both rules answer *"is this model reachable?"*, and `-m` answers that by construction: everything in scope
is reachable from the model that was named, and everything unreachable is outside. So under that flag they
cannot fire, and they belong in **Not looked at** rather than being dropped quietly, because a file
declaring two roots is exactly where they had something to say. → `scope.md` §6

## `T01` · Nothing points at this model

A model that nothing in the scope loads, assembles, refines or implements. Usually one of three things,
and the graph cannot tell you which:

- a draft left behind,
- a model whose consumer was renamed or deleted,
- a genuine entry point that should be documented as such.

**Report it as a question, not a defect**, and state the scope limit explicitly, because this is the one
rule where the boundary can manufacture a finding. The graph is complete only for the scope: a rooted
scope is complete by construction, since anything the root reaches is in it, and `--global` is complete for
the repository. Outside either, a model composed by a script or loaded from another repository is invisible
from here and looks **exactly** like an orphan. Say what you looked at, and over what.

## `T02` · Two roots over overlapping sources

Exactly one model should be the root: the one compiled, rendered, and, where bindings exist, executed.
Other goal models are sub-trees, compiled for viewing but never run separately.

This is not tidiness. `assemble` renames elements under the parent namespace, so binding at the root means
each node is renamed **once**, while binding per goal duplicates every shared node and multiplies the work.
The tell is two models that are each a root over an **overlapping** set of sources. Two roots over disjoint
sources are simply two arguments, which is normal and is what `-m` is for.

---

## Report shape

Both go among the suggestions, phrased as observations. The reader's words are *"nothing loads this file"*
and *"two files both look like the top of the tree"*; **orphan** and **entry point** are ours.

```text
### 6. Nothing in the corpus loads draft_fairness.jd

`draft_fairness.jd:6` `justification draft_fairness`

**What's wrong.** No other model here loads, assembles or refines it. Every other model in this scope is
reachable from `release.jd`; this one is not.

**Why it matters.** Probably nothing, and that is why this is last. But it will not be compiled by anything
that builds the release case, so it can rot without failing: a rename anywhere it depends on would break it
and no build would notice.

**Options.**
  **a.** Delete it, if it was superseded by `g2_fates.jd`, which covers the same requirement.
  **b.** Compose it into `release.jd`, if it was meant to be part of the case.
  **c.** Leave it and say so in its header, if it is a deliberate entry point compiled on its own.
  I cannot tell which from the files. (c) costs one comment and removes the question permanently.

Confidence: high that nothing here loads it; no read on why
Impact: none until you choose. I searched this scope only, so a script or another repository composing
  it would be invisible from here  ·  Reference: `[JD-T01]`
```
