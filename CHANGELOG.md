# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The plugin is versioned as a whole;
individual skills are not, so per-skill changes are grouped under the headings below.

## [Unreleased]

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
