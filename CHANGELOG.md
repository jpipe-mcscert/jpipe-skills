# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The plugin is versioned as a whole;
individual skills are not, so per-skill changes are grouped under the headings below.

## [Unreleased]

### Added

#### `jpipe-survey`

- **New skill: surveys a whole corpus** for what no single file can show. `jpipe-review` reads one
  model at a time on purpose, which left three questions unowned, and this skill owns them: whether
  the same fact is argued twice under labels that will **not** unify, whether two labels are identical
  enough to merge under `assemble` into a claim nobody wrote, and whether a leaf asserts something
  another model in the corpus already proves. It also reports orphan models and competing entry points.
- **It asks you questions, and that is the point.** Whether *"The committed training split"* and
  *"The train.csv split as committed"* name the same file is knowledge you have and the corpus does not
  record. Guessing produces a wrong merge, which is worse than finding nothing: it collapses a
  distinction you drew on purpose and, applied, quietly changes what your case claims. So uncertain
  clusters become numbered prose questions before anything is reported, at most 7 by default
  (`--questions N`), ordered by how many models each touches. Anything past the budget is reported as
  an open question rather than dropped. Answers, **including the ones where you say no**, land in a
  `Decisions` section so a later run does not re-ask.
- Answer nothing and the run is still useful: every uncertain cluster degrades to an open question and
  nothing is applied. Questions are prose rather than an interactive picker for exactly this reason.
- **Two new rule families**: `JD-R` for sharing (`R01` duplicate-fact-not-unified, `R02`
  extract-shared-leg, `R03` accidental-unification, `R04` redundant-check) and `JD-F` for refinement
  and structure (`F01` should-be-refine, `F02` refine-not-in-requirement-file, `F03` orphan-model,
  `F04` multiple-entry-points). `R03` is the only one backed by `language`: the composed model already
  asserts the merge, so it is reported without asking and cannot be declined.
- These are new ids, not revived ones. `jpipe-review` retired `S01`-`S04` and `C03`/`C04` in 0.1.1 and
  retired ids are never reused, so `references/rules.md` carries a translation table for anyone holding
  an older report. `F01` is the only rule that is genuinely new rather than renumbered: `jpipe-review`'s
  `C01` could only ask *"if an argument for R22 exists, refine against it. Does one?"*, and this skill
  answers that question.
- Needs **two or more** models, and says so rather than pretending: every rule here compares models.

#### Shared reference material

- **Reference text is now shared between skills**, via a canon at `references/` vendored byte-identically
  into each skill. Skills still cannot share a directory, because copying one into `~/.claude/skills/`
  has to keep working, so each ships its own copy and `tools/sync_refs.py --check` (in CI) fails if a
  copy drifts. `python3 tools/sync_refs.py` is the fix. Consumer-visible effect: none, unless you edit
  a vendored copy, which now fails CI with a pointer to the canon.
- `references/language.md` is the canon for the language itself, and `references/artifacts.md` is new:
  resolving an evidence label to the thing it names. Grounding asks *does this exist?* and sharing asks
  *have I seen this one before?*, and both read the same noun phrase, so the extraction lives in one
  place rather than drifting into two.

#### Fixtures

- `tests/corpus/corpora/` holds multi-model fixtures, where a finding **must** be stated across files.
  The single-model rule still holds for `good/` and `bad/`. `corpora/shared_evidence/` restores the
  three fixtures retired in 0.1.1, including the decoy that shares most of its wording with a real
  duplicate while denoting a different artifact.

## [0.1.1] - 2026-08-08

### Added

- **Stated scope: these skills review arguments, they do not write them.** Generative AI should not
  be used to author a safety case. An assurance case is a claim somebody is accountable for, and
  text that merely reads like an argument persuades without anyone having reasoned about the system.
  Everything here is built to review an argument a human wrote and to propose changes that author
  accepts or rejects. Stated in the README, in the skill's own README, and in the plugin description
  shown at install time.
- **Status: experimental.** This repository is a research exploration and is **not** a supported part
  of the jPipe toolchain. No stability guarantee; conventions here may change or be abandoned.
- **Installable as a Claude Code plugin.** `/plugin marketplace add jpipe-mcscert/jpipe-skills`
  followed by `/plugin install jpipe-skills@jpipe`, which keeps itself updated. `/plugin` is a
  terminal CLI command and does not exist in the VS Code or JetBrains extensions, so the README also
  documents installing by hand: each directory under `skills/` is self-contained, and copying or
  symlinking one into `~/.claude/skills/` or a project's `.claude/skills/` works in every host.

#### `jpipe-review`

- New skill: reviews the *argument* in an existing `.jd` justification model and proposes
  improvements. It compiles the model once as a gate and then checks four things no tool checks:
  **abstraction** (is each element at the right level?), **atomicity** (one leaf, one fact),
  **grounding** (do the artifacts the evidence names exist in the repository?), and the **house
  conventions** a single file can be held to.
- **Reviews one model at a time.** The skill reads the model you give it and the files that model
  `load`s, and never another `.jd`; a directory target is N independent reviews rather than one
  review of a corpus. So a CLEAN verdict means *this model holds on its own terms*, and cross-model
  questions are explicitly out of scope: whether the same fact is argued twice under labels that
  will not unify, whether two identical labels merge under `assemble` into a node nobody wrote, and
  whether anything still loads a given model. Every report names this limit in its **Not reviewed**
  section rather than letting a narrow review read as a broad one.
- Findings carry a rule id, a `file:line:col`, the proposed replacement text, and a blast-radius
  line. Nothing is edited until you approve a numbered fix list.
- Every finding names the **authority** backing it: `language` (the compiler decides, not
  negotiable), `argument` (the Toulmin reading, declinable), or `house` (McSCert practice, and
  irrelevant if your project states its own conventions).
- Syntax, unresolved symbols, cycles, and operator errors are **not** reported: `jpipe diagnostic`
  and the VS Code extension already cover them, with better locations. A model that does not compile
  stops at the gate rather than being re-explained.
- Requires the jPipe compiler on `PATH`.

#### Reference material

- Published the jPipe **house modelling style** as reference documentation. It previously existed
  only inside one tutorial repository, which made it unciteable by anyone else.
- `abstraction.md` grounds that style in **Toulmin's model of argument**, mapping `conclusion` →
  Claim, `strategy` → Warrant, `evidence` → Grounds, and naming Backing / Qualifier / Rebuttal as
  roles jPipe cannot express. This framing is new to the jPipe ecosystem and is offered as an
  explanatory lens, not as a claim about the language's design intent. It also replaces the previous
  informal name for the concept, *altitude*.
- `language.md` documents the language itself, separately from the house style, so a finding can say
  whether it rests on the grammar or on an opinion.
- **Erratum recorded:** `jpipe-compiler/docs/design/operators.md` documents `refine`'s hook argument
  as `"modelName/elementId"`; the compiler's own examples use a colon-qualified element id
  (`hook: "e"`, `hook: "first:e"`). `language.md` follows the examples.

#### Tooling

- `tools/validate_skills.py`: lints SKILL.md frontmatter, reference links, size budgets, rule-id
  definitions, and manifest agreement. Stdlib-only, no network.
- `tools/check_jd_blocks.py`: compiles every `.jd` this repository publishes: fenced examples in the
  documentation and every fixture under `tests/corpus/`.
- Both run in CI on push and pull request.

#### Documentation

- **How to update an installed copy**, in the README. Both paths: `/plugin marketplace update jpipe`
  then `/plugin update jpipe-skills@jpipe` for a plugin install, and re-copying or `git pull` for a
  hand install. Also how to turn auto-update on for this marketplace, and a `Releasing` checklist in
  `CONTRIBUTING.md` for the three version fields that have to move together.

### Fixed

- **The README claimed a plugin install "keeps itself updated". It does not.** Claude Code enables
  marketplace auto-update by default only for official Anthropic marketplaces; third-party ones, this
  repository included, have it **disabled** by default. Anyone who read that line was running whatever
  version they first installed. The `Update` section above replaces the claim with the commands that
  actually fetch a new version.

[Unreleased]: https://github.com/jpipe-mcscert/jpipe-skills/compare/main...HEAD
[0.1.1]: https://github.com/jpipe-mcscert/jpipe-skills/commits/main
