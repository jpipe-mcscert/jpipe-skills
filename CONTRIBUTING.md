# Contributing

## Tooling

```bash
python3 tools/validate_skills.py     # frontmatter, reference links, budgets, manifests
python3 tools/check_jd_blocks.py     # every published .jd example must compile (needs jpipe)
```

Both run in CI on push and pull request. The first is stdlib-only and needs no network.

A skill is prose, so nothing executes it and it fails silently. These tools cover the two ways that
happens:

- **Structural rot**: a renamed reference file leaving a dangling path in `SKILL.md`, a frontmatter
  `name` drifting from its directory, version skew between the two manifests. None of this raises an
  error at runtime; the skill just quietly degrades into guesswork.
- **Factual rot**: an example in the documentation that no longer compiles. A published `.jd` that
  stopped building is a skill teaching a wrong pattern.

Fixtures live in [`tests/corpus/`](tests/corpus/), which has its own README explaining what each
directory guards.

## Adding a skill

Name it `jpipe-<verb>`, and make the directory name match the frontmatter `name` exactly. The
loader keys on it, and a mismatch means the skill silently never loads.

The `description` must contain `Use when …` and at least one `NOT for …` clause naming the sibling
that *does* cover that case. This is not boilerplate: a skill is selected by matching its
description, so as the family grows, each skill saying what it is **not** is what keeps the right one
being picked.

Keep `SKILL.md` to procedure (the workflow, the guardrails, the output contract) and push
everything with a "read this when…" trigger into `references/`. A reference the model loads on every
invocation regardless of need is just an expensive part of `SKILL.md`.

Do not declare `AskUserQuestion` in `allowed-tools`; the linter rejects it. When a skill needs a
decision, ask for it in prose. That reads the same in every host and still works in a headless run,
where an interactive picker cannot be answered and an approval step built on one would deadlock.

### Shared reference material

Skills cannot share a `references/` directory; each must be self-contained so that copying one
directory into `~/.claude/skills/` still works.

Today all reference material lives inside `jpipe-review`. When a second skill needs the same text,
hoist the canon to a root `references/`, vendor copies into each skill, and add a drift check to CI.
That is deliberately deferred rather than forgotten. With one skill it would be machinery guarding a
problem that does not exist, and the move is mechanical when it arrives.

## Before a release

The tools cannot test what a skill *concludes*. An LLM's prose report is not golden-testable, and
asserting on wording would produce a flaky suite that gets deleted. So run these by hand and check
the assertion, never the phrasing:

1. A clean model → no findings, and **zero edits**. *The approval gate holds.*
2. A known-good multi-leg model (`jpipe-tutorial-2026/justifications/requirements/r9.jd`) → 🟢, and
   its evidence grounds against the real tree. *The most important one: it guards against false
   positives, which are what make a reviewer useless.*
3. A model that does not compile → stops at the gate, attempts no semantic review, and does not
   re-explain the compiler's diagnostics.
4. A model with a broken `load` → caught, even though the fatal appears **only on stderr** and stdout
   is completely empty. *The bug most likely to ship.*
5. A leaf naming a nonexistent file → one `JD-G01`, citing the searches it ran.
6. A directory of several models → N independent reviews, and **no finding stated in terms of a
   second file**. *The scope boundary: the skill reads one model at a time.*
7. `--apply`, answering *"1 and 3 only"* → exactly two edits, re-verified, nothing written to git.

Record the outcome in `CHANGELOG.md` for the release.

## Releasing

**Bump the version, or the release reaches nobody.** Claude Code ships an update to installed plugins
only when the `version` field in `.claude-plugin/plugin.json` changes. Pushing to `main` is not a
release; an unbumped push is invisible to everyone who installed the plugin.

Three fields move together, and `claude plugin tag` refuses to tag if the first two disagree:

| File | Field |
|---|---|
| `.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `plugins[].version` for `jpipe-skills` |
| `.claude-plugin/marketplace.json` | `metadata.version`, the catalog's own version |

Then:

1. Move the `[Unreleased]` entries in `CHANGELOG.md` under a dated `[x.y.z]` heading, and add its
   link reference at the bottom of the file.
2. `python3 tools/validate_skills.py && python3 tools/check_jd_blocks.py`, plus `claude plugin
   validate .` for the manifests.
3. Merge to `main`. Users pick it up with `/plugin marketplace update jpipe`, or automatically if they
   enabled auto-update, which is **off** by default for third-party marketplaces.

Rule ids are a public interface, so retiring one is a breaking change even when nothing else moves.
Retired ids are never reused: `rules.md` keeps a **Retired ids** section, and the numbering keeps its
gaps rather than closing them.

## Changelog

`CHANGELOG.md` describes the net user-facing effect of a change, not the commit history. New skills,
new or renamed rule ids, changed report formats, and new requirements all belong there. Internal
refactors and churn within an unreleased change set do not.

Rule ids are a public interface: people cite them in review threads and may script against them.
Renaming or removing one is a breaking change.

## Branches

`main` stays releasable; `/plugin marketplace add` tracks the default branch, so anything merged is
immediately live for anyone who has installed the marketplace. Work on a feature branch and open a
pull request.
