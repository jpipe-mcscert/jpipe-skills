# Fixtures

Small `.jd` models used to exercise the skills. **Every file here compiles cleanly**, and that is the
point. These are semantic defects, not syntax errors; a fixture that fails `jpipe diagnostic` would be
testing the compiler instead of the skill.

CI (`tools/check_jd_blocks.py`) asserts exactly that: every file in this tree builds without a
diagnostic.

The tree splits by what a fixture *is*: a single model, or a corpus.

| Directory | Skill | Contents | Expected outcome |
|---|---|---|---|
| `good/` | `jpipe-review` | Models already at the right abstraction | **No findings.** These guard against false positives, which is the failure mode that makes a reviewer useless |
| `bad/` | `jpipe-review` | One smell per file, named in the header as `expect: JD-XNN` | Exactly that rule id, at that element |
| `corpora/<case>/` | `jpipe-survey` | Two or more models whose relationship is the subject | Named in each file's header. Findings **must** be stated across files here |

**Each `corpora/` case is rooted**, so it is exercised the way a real corpus is: point the skill at the
case's root file and its scope is that file plus everything it loads. No flags. Most have a `root.jd` that
composes the case with `assemble`; in `refine_available/`, `f1_consumer.jd` loads the requirement it
should refine against, so it is the root itself.

Those roots are not scaffolding, and two cases show why the label they carry is load-bearing.
`comb_shaped/`'s refiner concludes something *close to* the leaf it would graft under rather than
identical to it, because `assemble` merges byte-identical labels and the merged node would then have two
strategies beneath it, which does not build. `kind_mismatch/`'s root had to be given a `conclusionLabel`
distinct from every source's conclusion for the same reason. That the composition only works through
`refine` is the rule's own argument, made by the compiler.

`scoped_model/` is the one case run **twice**, with `-m fairness` and without, because what it guards is
the difference between the two. Its root file declares two arguments rather than one, which is the
situation `-m` exists for. It is also the only `corpora/` case that exercises **both** skills, since `-m`
narrows a review the same way: `jpipe-review goals.jd -m fairness` must examine the elements of
`fairness`, `r1`, `r2` and `r3` and say nothing about `efficiency`'s.

The roots are not scaffolding. `assemble` is the operator that would actually merge two identical
labels, so `accidental_unification/root.jd` is what makes that case's defect real rather than
hypothetical.

Files under `good/` and `bad/` load nothing, so each is a scope of one and a finding stated in terms of
a second fixture is a bug in the skill. Under `corpora/` the opposite holds: the root's closure is the
scope, findings are expected to span its files, and a finding that could have been made from a single
file is out of scope.

Fixtures are deliberately generic (a release, a build, a coverage report) rather than drawn from any
one project, so they read the same to someone who has never seen the tutorial corpus.

## `corpora/` cases

| Case | Guards |
|---|---|
| `semantic_duplicate/` | One claim under two wordings, **neither naming a path**. One `JD-M01` at medium confidence, with the reading stated. The case the 0.2.0 rewrite exists for: the artifact-clustering method reported nothing here |
| `shared_evidence/` | The same fact under drifted labels, both resolvable. Exactly one `JD-M01` (s1 ⇄ s2) and **nothing** on the decoy (s3) |
| `fused_blocks_sharing/` | A leaf covering two things, one of which is another model's leaf verbatim. One `JD-D01` naming the partner. Remove the partner and it must fall **silent** |
| `comb_shaped/` | Four bare leaves under one strategy, one of which a sibling model argues. One `JD-P01` at that leaf only, and no complaint about the flatness itself |
| `kind_mismatch/` | One comparison written as a check in one model and a fact in another. One `JD-L01`, proposing no edit and handing the re-level to `jpipe-review` |
| `untimed/` | A composition spanning artifacts that exist at different moments. One `JD-N01`, one `JD-N02`, and **nothing** about the file that exists nowhere in this repository |
| `accidental_unification/` | Byte-identical labels denoting different artifacts, composed together. One `JD-M03`, 🔴 |
| `refine_available/` | A leaf asserting what a sibling model proves. One `JD-P01`, and a low-confidence candidate instead if the sibling is removed |
| `scoped_model/` | One file, two arguments. `-m fairness` gives exactly one `JD-M01` and says nothing about `efficiency`; without `-m`, the same `JD-M01` plus a **candidate** where a `JD-M03` would be plausible and wrong, nothing composing those two models together |

Two of those are negative assertions, and they are the ones that fail quietly. `fused_blocks_sharing/`
without its partner must produce **no** finding rather than a bare atomicity complaint, which belongs to
`jpipe-review`. `untimed/` names `model/metrics.json`, which is in no checkout of this repository, and
must say nothing about it: the label says a run writes it, so its absence is correct. A finding there
means the skill has started searching the tree, which it must never do.

`shared_evidence/` is the sharpest guard in the whole tree, because it is built so that **string
distance and artifact identity point in opposite directions**:

| File | Label | Artifact |
|---|---|---|
| `s1_fairness.jd` | "The committed training split" | `data/train.csv` |
| `s2_provenance.jd` | "The train.csv split as committed" | `data/train.csv` |
| `s3_decoy.jd` | "The committed training configuration" | `config/train.yaml` |

s1 and s3 are the *closest* pair by wording and the wrong answer; s1 and s2 are the *farthest* and the
right one. Anything that clusters on label similarity returns the exactly inverted result: a false
positive on the decoy and a miss on the real duplicate. That is the whole test.

s2's header carries a second assertion worth keeping: the two warrants genuinely differ (a column-set
intersection versus a checksum match), and that must **not** be flagged. Sharing a fact is not sharing
a check, so only the leaves should ever be aligned.

## Fixtures that need a repository

Some passes cannot be exercised by `.jd` files alone, and there are deliberately no fixtures for them:

- **Grounding** (`jpipe-review` Step 3) checks evidence labels against files in the working tree.
  `jpipe-survey` has no equivalent pass and must never acquire one: it never looks for an artifact a
  label names, so `untimed/` doubles as the guard on that.
- **The report's ranking and prose** cannot be asserted mechanically. What a `corpora/` case pins down is
  which candidates are found, at what confidence, and which must not be found at all.

Both are verified end-to-end against real project trees instead, per the release checklist in
[CONTRIBUTING.md](../../CONTRIBUTING.md).
