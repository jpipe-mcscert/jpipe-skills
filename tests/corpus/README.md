# Review fixtures

Small `.jd` models used to exercise `jpipe-review`. **Every file here compiles cleanly** — that is
the point. These are semantic defects, not syntax errors; a fixture that fails `jpipe diagnostic`
would be testing the compiler instead of the skill.

CI (`tools/check_jd_blocks.py`) asserts exactly that: every file in this tree builds without a
diagnostic.

| Directory | Contents | Expected review outcome |
|---|---|---|
| `good/` | Models already at the right abstraction | **No findings.** These guard against false positives, which is the failure mode that makes a reviewer useless |
| `bad/` | One smell per file, named in the header as `expect: JD-XNN` | Exactly that rule id, at that element |
| `shared/` | A three-model corpus for the reuse pass | Exactly one `JD-S01` (s1 ⇄ s2) and **nothing** on the decoy (s3) |

`shared/` is the sharper of the two guards. `s3_decoy.jd` shares most of its wording with
`s1_fairness.jd` while denoting a different artifact — `config/train.yaml` rather than
`data/train.csv`. A reviewer that clusters labels by string similarity will propose merging them and
be wrong. Clustering by the artifact named is what `references/sharing.md` requires, and this fixture
is how you find out whether it happened.

The `good/` and `bad/` fixtures are deliberately generic (a release, a build, a coverage report)
rather than drawn from any one project, so they read the same to someone who has never seen the
tutorial corpus.

## Fixtures that need a repository

The grounding pass (Step 4) checks evidence labels against files in the working tree, so it cannot be
exercised by a standalone `.jd`. There are no grounding fixtures here on purpose — grounding is
verified end-to-end against real project trees instead, per the release checklist in the repository
README.
