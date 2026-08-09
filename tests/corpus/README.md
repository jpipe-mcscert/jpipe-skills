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

None of the `corpora/` cases has a root file that loads the others, on purpose: they are corpora, not
composed models. So exercise them with **`--global` from inside the case directory**, which is the
invocation for a corpus not rooted in a single model. Pointing either skill at one of the files gives a
scope of one, which for `jpipe-survey` is an error it should report rather than work around.

Files under `good/` and `bad/` are reviewed **on their own**, which is the only way `jpipe-review`
reviews anything: a finding there stated in terms of a second fixture is a bug in the skill. Under
`corpora/` the opposite holds, and a finding that could have been made from one file is out of scope.

Fixtures are deliberately generic (a release, a build, a coverage report) rather than drawn from any
one project, so they read the same to someone who has never seen the tutorial corpus.

## `corpora/` cases

| Case | Guards |
|---|---|
| `shared_evidence/` | The same fact under drifted labels. Exactly one `JD-R01` (s1 ⇄ s2) and **nothing** on the decoy (s3) |
| `accidental_unification/` | Byte-identical labels denoting different artifacts. One `JD-R03`, 🔴, reported without asking |
| `refine_available/` | A leaf asserting what a sibling model proves. One `JD-F01`, and an open question instead if the sibling is removed |

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

- **Grounding** (`jpipe-review` Step 4) checks evidence labels against files in the working tree.
- **The interview** (`jpipe-survey` Step 5) needs a human to answer, so what a `corpora/` case can
  assert is which clusters get *asked about*, not what the answer produces.

Both are verified end-to-end against real project trees instead, per the release checklist in
[CONTRIBUTING.md](../../CONTRIBUTING.md).
