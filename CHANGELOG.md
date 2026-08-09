# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions read as
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) triples. While the repository is
experimental it stays on `0.1.x`, so a patch bump here can carry a new skill or a changed report
format; read the entry, not the number. The plugin is versioned as a whole and individual skills are
not, so per-skill changes are grouped under the headings below.

## [Unreleased]

## [0.1.5] - 2026-08-09

### Added

- **`jpipe-survey` takes `-m <model>`**, narrowing the scope to one model in the named file plus the
  models it is built from, following `assemble`, `refine` and `implements` sources transitively. A `load`
  makes a model's name available without making it part of any particular argument, so a file that
  composes two goals out of separate requirement files holds two arguments while the survey has been
  treating it as one scope. Spelled as jPipe spells it, as in `jpipe process -m <model> -i <file>`. It
  contradicts `--global`, and naming a model the file does not declare is an error that lists the ones it
  does. The report names the models it compared, and under `-m` names the file's other models as not
  looked at.
- Under `-m`, `JD-F03` (files nothing loads) and `JD-F04` (competing entry points) no longer fire, since
  that flag answers by construction the question both of them ask: everything in scope is reachable from
  the model you named. They are listed as not looked at rather than dropped quietly, because a file
  declaring two roots is exactly where they had something to say.

### Fixed

- **`JD-R03` now requires a model that composes both sides.** Identical labels merge inside a composed
  model, so two models that nothing composes together keep their own nodes and the merge never happens.
  Any two byte-identical labels over different artifacts anywhere in scope were previously reported as a
  🔴, which in a file declaring two independent roots was a false positive on the one finding nobody can
  decline. Those collisions are now open questions: a hazard waiting on a composition nobody has written.
- **`JD-F01` compares models rather than files.** The label harvest now carries each element's enclosing
  `justification`, so in a corpus with several models per file a leaf is no longer matched against its own
  model's conclusion, which is one argument's internal shape and `jpipe-review`'s to judge.

## [0.1.4] - 2026-08-09

### Changed

- **Both skills now take exactly one `.jd` file as their scope**, together with everything that file
  transitively `load`s. That closure is the object of study, because a goal assembled from four
  requirement files is one argument rather than four, and reviewing or surveying half an argument tells
  you little. **Breaking**: passing a directory, a glob, or nothing at all used to work and is now an
  error, as is passing more than one file. Pass `--global` to scope either skill to every `.jd` in the
  repository instead.
- **`jpipe-review` now reports findings in loaded files.** Previously the files a model loaded were read
  for context only and "never the site of a finding", so getting findings on a requirement file meant
  invoking the skill again on that file. Point it at your top-level goal and it now reviews the whole
  tree beneath it, once, with each element examined a single time even under `--global`.
- One consequence worth having: `C01` (a leaf tagged with a requirement that should be a `refine`) can
  now be a **finding** rather than always a question, when the model that proves the requirement is in
  the closure. It stays a question when it is not, because inventing an answer is that rule's own
  failure mode.
- **The `--apply` flag is gone.** It was ceremony: the prose approval step is what protects you, so the
  fix list now always follows the report and still edits nothing until you name the numbers. `jpipe` on
  `PATH` is needed only once you approve something.
- `jpipe-survey` needs two or more models in scope, so a file that loads nothing is reported as a scope
  of one with `--global` suggested, rather than surveyed alone.

### Fixed

- `jpipe-survey`'s output contract still described the pre-0.1.3 finding shape, asking for a rule
  description and a `file:line:col` that no longer exists. It now matches the report format the rest of
  the skill was rewritten to.
- `jpipe-survey` had no guardrail bounding what it reads. "Corpus" and "target" were used
  interchangeably without ever being equated, so the harvest step could reach past whatever was passed
  in. The two words are now defined as the same set, and the harvest is told to pass the scope's files
  explicitly rather than a directory.

## [0.1.3] - 2026-08-09

### Changed

#### Both skills

- **Reports are now written for the engineer who built the system**, not for a safety specialist. If
  you have never heard of Toulmin, never read this skill, and have no idea what `A05` means, nothing in
  a report should require you to look anything up. Findings are phrased in terms of your system, and
  give you three things in order: **what's wrong** about the element in front of you, **why it matters**
  (what goes undetected, what a reader is wrongly reassured about, what breaks silently later), and
  **your options**, usually more than one, with the trade-off named and a recommendation. You choose.
- The internal vocabulary is gone from the output. No "a Claim in a Grounds slot", no "wrong level of
  abstraction", no `UNSOUND`/`ABSTRACTION`/`CONVENTION` headings, no "authority: argument". Sections now
  say what they mean: *the argument does not hold*, *the argument will not tell you when it breaks*,
  *suggestions*. Rule ids still appear, once, at the end of each finding, because people cite them in
  review threads and script against them; they are a reference number, never the explanation.
- In `jpipe-survey` the same rule reaches further, because its **questions** are the most reader-facing
  text either skill produces. They now ask *"Are these the same file?"* rather than *"Same artifact?"*,
  and explain the consequence in terms of the reader's system: two boxes instead of one when the models
  are composed, so a check that runs twice. Compiler vocabulary is out, `unify` included, since it names
  a pass nobody invokes; `assemble` and `refine` stay, because those are keywords the reader writes.
  The report's `Decisions` section is now called **What you told me**.
- Survey section headings say what they mean too: *composing these models makes a claim nobody wrote*,
  *an argument the corpus already contains is being asserted instead*, *the same work is being done
  twice*, *suggestions*.

#### `jpipe-review`

- **Decomposition is now the recommendation, not one option among two.** Where an element does two jobs,
  the review leads with splitting it into legs, and gives the reason that matters to you: a split
  argument tells you *which* half failed, and each half can be checked on its own. Reworking a label in
  place is offered second, for the case where a leg genuinely rests on one thing.
- **New rule `JD-A07`, non-atomic-strategy.** Atomicity previously covered evidence only, so a strategy
  running two checks at once ("check the packages against the allowlist **and** scan the imports")
  passed unremarked while producing exactly the defect `A05` describes: one pass/fail for two questions.
  It usually pairs with `A05`, and one decomposition fixes both.
- **Proposed labels are short**: under 10 words for a fact, 15 for a check. Two mechanical reasons, both
  new to the guidance: labels are the node text in a rendered diagram, so a 25-word label produces a
  diagram nobody reads; and unification is exact string equality, so long labels accumulate incidental
  wording and never collide, which is what shared nodes need. A long label is also usually a *structural*
  tell rather than a writing one, since the words are long because the element is doing two jobs.
- `jpipe-survey` holds proposed labels to the same limits, where the reason is sharper still: a label is
  shared only when two files match it **exactly**, so a long canonical wording is a merge that quietly
  never happens.

## [0.1.2] - 2026-08-09

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

### Changed

- **Neither skill compiles your model before reviewing it.** `jpipe-review` used to open with a compile
  gate and refuse to review a file that did not build. It no longer does, and `jpipe-survey` never did.
  Whether a file compiles is the compiler's answer to give, and you already have it from
  `jpipe diagnostic` and your editor; an argument's shape is legible long before it parses, so refusing
  to look was friction rather than rigour. Compilation now happens in exactly one place: **after** an
  approved edit, verifying work the skill itself did.
- Consequences worth knowing. **Reporting needs no tools at all**, so both skills work in a checkout
  with no compiler, and `jpipe-survey` will survey a corpus caught mid-edit. `--apply` still requires
  `jpipe` on `PATH` and now says so and stops *before* editing, because an edit to an assurance case
  that cannot be verified is worse than a finding merely reported. The **BLOCKED** verdict is gone from
  `jpipe-review` and **PARTIAL** never shipped in `jpipe-survey`; a report's header no longer carries a
  compile-gate line, and neither verdict claims anything about whether your files build.
- Findings cite `file:line` rather than `file:line:col`. The column came from the compile gate's symbol
  table, which is no longer read; a column is still given when the label's opening quote can be pointed
  at directly.

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
[0.1.5]: https://github.com/jpipe-mcscert/jpipe-skills/compare/074251e56519460a4e3e8a51e9272aa6ddcb1633...main
[0.1.4]: https://github.com/jpipe-mcscert/jpipe-skills/compare/00295157ff39c658efd568b0b245fda1847a9df6...074251e56519460a4e3e8a51e9272aa6ddcb1633
[0.1.3]: https://github.com/jpipe-mcscert/jpipe-skills/compare/c0bef5968ed24e6da8eef07df9053d55340ee776...00295157ff39c658efd568b0b245fda1847a9df6
[0.1.2]: https://github.com/jpipe-mcscert/jpipe-skills/compare/15c57b9f650c121b39bcd8a4ef28367bf8264e99...c0bef5968ed24e6da8eef07df9053d55340ee776
[0.1.1]: https://github.com/jpipe-mcscert/jpipe-skills/commit/15c57b9f650c121b39bcd8a4ef28367bf8264e99
