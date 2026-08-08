# Review fixtures

Small `.jd` models used to exercise `jpipe-review`. **Every file here compiles cleanly**, and that
is the point. These are semantic defects, not syntax errors; a fixture that fails `jpipe diagnostic`
would be testing the compiler instead of the skill.

CI (`tools/check_jd_blocks.py`) asserts exactly that: every file in this tree builds without a
diagnostic.

| Directory | Contents | Expected review outcome |
|---|---|---|
| `good/` | Models already at the right abstraction | **No findings.** These guard against false positives, which is the failure mode that makes a reviewer useless |
| `bad/` | One smell per file, named in the header as `expect: JD-XNN` | Exactly that rule id, at that element |

Each fixture is reviewed **on its own**, which is the only way `jpipe-review` reviews anything. A
finding stated in terms of a second fixture is a bug in the skill, not a finding.

The `good/` and `bad/` fixtures are deliberately generic (a release, a build, a coverage report)
rather than drawn from any one project, so they read the same to someone who has never seen the
tutorial corpus.

## Fixtures that need a repository

The grounding pass (Step 4) checks evidence labels against files in the working tree, so it cannot be
exercised by a standalone `.jd`. There are no grounding fixtures here on purpose. Grounding is
verified end-to-end against real project trees instead, per the release checklist in the repository
README.
