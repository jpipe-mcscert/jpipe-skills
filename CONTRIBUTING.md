# Contributing

## Tooling

```bash
python3 tools/validate_skills.py     # frontmatter, reference links, budgets, manifests
python3 tools/sync_refs.py --check   # vendored references still match the canon
python3 tools/check_jd_blocks.py     # every published .jd example must compile (needs jpipe)
```

All three run in CI on push and pull request. The first two are stdlib-only and need no network.

A skill is prose, so nothing executes it and it fails silently. These tools cover the three ways that
happens:

- **Structural rot**: a renamed reference file leaving a dangling path in `SKILL.md`, a frontmatter
  `name` drifting from its directory, version skew between the two manifests. None of this raises an
  error at runtime; the skill just quietly degrades into guesswork.
- **Divergent rot**: one skill's copy of a shared reference edited in place, so two skills quietly
  disagree about the language they both describe.
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
directory into `~/.claude/skills/` still works. So shared text lives once at the root and is
**vendored** into each skill that needs it:

| | |
|---|---|
| `references/*.md` | the **canon**. Edit here, and only here |
| `skills/*/references/<same-name>.md` | a vendored copy, byte-identical, shipped with the skill |

The rule is zero-config: for every file in the root `references/`, any same-named file under a skill's
`references/` must match it byte-for-byte. A skill opts in by *having* the file, so there is no
manifest to forget to update. `tools/sync_refs.py --check` is the CI gate, and the fix is one command:

```bash
python3 tools/sync_refs.py           # copy the canon over every vendored copy
```

Each canon file opens with an HTML-comment banner naming itself as the canon, so anyone who opens a
vendored copy and starts typing is told where to go instead. The banner is part of the copied bytes,
which is why byte-identity still holds. `sync_refs.py` never *creates* a copy: vendoring a file into a
skill for the first time is a deliberate act, so do it by hand once and the tool keeps it honest after.

**What belongs in the canon** is text that is true independently of who reads it: the language, the
extraction of an artifact from a label, what a scope is. What does not is anything phrased as an
instruction to one skill. When hoisting, strip the imperatives: a sentence like *"do not report any of
this"* is a guardrail belonging in a `SKILL.md`, not a fact about jPipe. Prefer leaving material in one
skill over hoisting something that then needs a caveat per consumer.

## Before a release

The tools cannot test what a skill *concludes*. An LLM's prose report is not golden-testable, and
asserting on wording would produce a flaky suite that gets deleted. So run these by hand and check
the assertion, never the phrasing:

1. A clean model → no findings, and **zero edits**. *The approval gate holds.*
2. A known-good multi-leg model (`jpipe-tutorial-2026/justifications/requirements/r9.jd`) → 🟢, and
   its evidence grounds against the real tree. *The most important one: it guards against false
   positives, which are what make a reviewer useless.*
3. A model that does not compile → **still reviewed**, and the report does not claim it builds, does
   not re-explain the compiler's diagnostics, and does not refuse. *Nothing is compiled before an edit.*
4. Approving a fix on a model with a broken `load` → the post-edit check catches it, even though the
   fatal appears **only on stderr** with stdout completely empty. *The bug most likely to ship: a
   verifier reading stdout alone calls a broken file clean.*
5. A leaf naming a nonexistent file → one `JD-G01`, citing the searches it ran.
6. A goal file that loads three requirement files → **one** review of all four, with findings landing in
   the loaded files too. Then no file, and two files: both are errors that stop. *The scope contract.*
7. `corpora/scoped_model/goals.jd -m fairness` → the elements of `fairness`, `r1`, `r2` and `r3`
   examined, **nothing** about `efficiency`'s, and `efficiency` named as not reviewed. Then a leaf tagged
   `(Rnn)` whose requirement model the file `load`s but the named model is not built from → `C01` is a
   **question**, not a finding. *The half of the scope contract a file with two roots depends on, and the
   one rule whose verdict the flag can change.*
8. Answering *"1 and 3 only"* to the fix list → exactly two edits, re-verified, nothing written to git.

Then `jpipe-survey`, whose failure modes are different because it compares elements across models:

9. `corpora/semantic_duplicate/root.jd` → one `JD-M01`, at **medium** confidence, with the reading stated
   and **no path invented** for either label. *The case the 0.2.0 rewrite exists for: neither leaf resolves
   to an artifact, so the method it replaced reported nothing here at all.*
10. `corpora/shared_evidence/root.jd` → exactly one `JD-M01` (s1 ⇄ s2) and **nothing** on the decoy.
    *The regression that matters most, and the pair to run with case 9: comparing meanings must not
    collapse into comparing strings. The decoy is the closest label to s1 by wording and the wrong answer.*
11. `corpora/fused_blocks_sharing/root.jd` → one `JD-D01` naming the partner half and the merge that
    follows the split. Then remove `r14_tests.jd` from the scope and rerun: **silence**, not a bare
    atomicity complaint. *A fused leaf with no partner is `jpipe-review`'s `A05`, and the named partner is
    the whole of what separates the two skills here.*
12. `corpora/comb_shaped/root.jd` → one `JD-P01`, at `e_grid` only, naming the model to graft and the
    hook. It must **not** report the other three leaves, and must **not** report the flatness itself, which
    is `jpipe-review`'s `A03`.
13. `corpora/kind_mismatch/root.jd` → one `JD-L01` that proposes **no edit**, says which side looks wrong
    and why, and hands the re-level to `jpipe-review`. An `L01` must never appear in a fix list.
14. `corpora/untimed/root.jd` → one `JD-N01` naming which leaves exist when, one `JD-N02`, and **nothing
    whatever** about `model/metrics.json`, which exists in no checkout of this repository. Then point the
    skill at a real corpus in a tree where several named files genuinely do not exist: still nothing.
    *A survey that reports a missing file has become a grounding pass, and a wrong one, since a case may
    be discharged from CI where that file is the output rather than the input.*
15. `corpora/accidental_unification/root.jd` → one `JD-M03`, 🔴, at high confidence. The merge is what the
    compiler will do, so it is the one finding nobody can decline.
16. `corpora/refine_available/f1_consumer.jd` → one `JD-P01`, since the model it should refine against is
    in the closure. Then drop the `load` line and rerun: it must become a **low-confidence candidate** with
    no edit proposed, because the tag says a requirement exists, not that anyone argued it.
17. `corpora/scoped_model/goals.jd` **with `-m fairness`** → exactly one `JD-M01`, nothing whatever about
    `efficiency`, and **Not looked at** naming `efficiency` along with `JD-T01` and `JD-T02`. Then the same
    file with no `-m`: the same `JD-M01`, and the two identical `"The reported metrics"` leaves as a
    **candidate** rather than a `JD-M03`. *A merge happens inside a composition, and nothing composes `r3`
    with `efficiency`, so a 🔴 there would be plainly false.*
18. `corpora/scoped_model/goals.jd -m nosuchmodel` → an error that lists the models the file does
    declare. The same file with `-m fairness --global` → an error. Neither picks one and carries on.
19. **Zero questions before the report**, on every case above, and zero edits before a numbered fix list
    is approved. Then decline one numbered fix and rerun: it must appear under **What you decided** and
    must not be proposed again. *What the interview used to protect, now carried by confidence, the
    approval gate and the record of declines.*
20. A report on a real corpus → **Worth your time, in order** comes first, its top entry is defensible,
    and every finding carries a `Confidence:` sentence with a reason and an `Impact:` line. A finding at
    low confidence must propose no edit.
21. A scope where one file does not compile → surveyed like any other, since an element is comparable
    whether or not its file parses. After an approved fix, the post-edit check must not blame that file's
    pre-existing breakage on the edit.
22. Either skill on a corpus → **no finding that belongs to the other**. A survey that reports a
    non-atomic leaf with no partner, or a review that compares two models, has crossed the line the split
    exists for.

Record the outcome in `CHANGELOG.md` for the release.

## Releasing

**Bump the version, or the release reaches nobody.** Claude Code ships an update to installed plugins
only when the `version` field in `.claude-plugin/plugin.json` changes. Pushing to `main` is not a
release; an unbumped push is invisible to everyone who installed the plugin.

Three fields move together:

| File | Field | Enforced by |
|---|---|---|
| `.claude-plugin/plugin.json` | `version` | this is the one Claude Code reads |
| `.claude-plugin/marketplace.json` | `plugins[].version` for `jpipe-skills` | `validate_skills.py`, which fails if it disagrees with the above |
| `.claude-plugin/marketplace.json` | `metadata.version`, the catalog's own version | convention only, for a single-plugin repository |

Then:

1. Move the `[Unreleased]` entries in `CHANGELOG.md` under a dated `[x.y.z]` heading, and add its
   link reference at the bottom of the file.
2. `python3 tools/validate_skills.py && python3 tools/sync_refs.py --check && python3
   tools/check_jd_blocks.py`, plus `claude plugin validate .` for the manifests.
3. Merge to `main`. Users pick it up with `/plugin marketplace update jpipe`, or automatically if they
   enabled auto-update, which is **off** by default for third-party marketplaces.

### Versions are `0.1.x` while experimental

A patch bump here can carry a new skill or a changed report format. That departs from semantic
versioning on purpose, and `CHANGELOG.md` says so rather than claiming a discipline the numbers do not
follow: read the entry, not the number. Reconsider at 1.0.

### No git tags before 1.0

**Tagging is not part of releasing yet.** It starts at 1.0 and applies to every release after it.

Nothing in the plugin system needs a tag. Claude Code resolves a plugin's version from `plugin.json`
first, falling back to the marketplace entry, then the commit SHA
([version management](https://code.claude.com/docs/en/plugins-reference#version-management)), so
bumping `version` is the entire delivery mechanism. Tags do exactly one job: they let **another**
plugin depend on this one with a semver range, resolved against `{plugin-name}--v{version}` tags
([dependency versions](https://code.claude.com/docs/en/plugin-dependencies)). Nothing depends on
`jpipe-skills`, so there is nothing for a tag to resolve.

Consequences while this holds:

- `CHANGELOG.md` version links are **compare ranges between release commits**, not tag URLs. They
  resolve today and need no tags. A release cannot link to its own commit, since writing the link
  changes the SHA, so the newest entry ends at `main` until the next release pins it.
- From 1.0, use `claude plugin tag --push`, which derives `jpipe-skills--v<version>` from the manifest
  and refuses unless `plugin.json` and the marketplace entry agree and the tree is clean. Switch the
  changelog links to tag URLs at the same time.

Rule ids are a public interface, so retiring one is a breaking change even when nothing else moves.
Retired ids are never reused: `rules.md` keeps a **Retired ids** section, and the numbering keeps its
gaps rather than closing them.

**Retiring burns the letter, not just the number.** Twelve ids have gone across two rounds, `S01`-`S04`
and `C03`/`C04` when `jpipe-review` narrowed to one model, then `R01`-`R04` and `F01`-`F04` when
`jpipe-survey` re-keyed its families to the edit each finding asks for. So `S`, `C`, `R` and `F` are all
spent, and a new family takes a fresh letter. Two consequences for anyone adding one:

- Add the letter to `RULE_ID_RE` **and** to the definitions regex in `tools/validate_skills.py`. Missing
  either means the id is silently neither a citation nor a definition, and the dangling-reference check
  passes while checking nothing.
- Retired letters stay in that character class on purpose, so a prefixed retired id reads as a dangling
  citation and fails. That is why the catalogues spell retired ids **bare**, without `JD-`.

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
