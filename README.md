# jpipe-skills

Reference [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for
[jPipe](https://www.jpipe.org), the justification / assurance-case language.

## Install

```
/plugin marketplace add jpipe-mcscert/jpipe-skills
/plugin install jpipe-skills@jpipe
```

Skills also work by plain copy — each directory under `skills/` is self-contained, so
`cp -r skills/jpipe-review ~/.claude/skills/` is equivalent.

`jpipe-review` needs the [jPipe compiler](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH`
(`brew install jpipe`, `apt install jpipe`, or `scoop install mcscert/jpipe`).

## Skills

| Skill | What it does |
|---|---|
| [`jpipe-review`](skills/jpipe-review/) | Reviews the *argument* in an existing `.jd` model — abstraction, atomicity, grounding, reuse, corpus conventions — and proposes fixes you approve before anything is edited |

## What `jpipe-review` is for

The compiler and the VS Code extension already catch syntax, unresolved symbols, cycles, and missing
operator keys, with better line numbers than a language model will produce. This skill deliberately
does none of that. It compiles the model once as a **gate** and then asks the questions no tool asks:

- **Abstraction** — is each element at the right level? `evidence` should supply a datum, `strategy`
  should license an inference, `conclusion` should assert the claim. A leaf reading *"a schema check
  passes"* asserts the verdict its own leg exists to reach, so the argument proves itself.
- **Atomicity** — one leaf, one fact. *"The Pipfile and the pipeline source"* is two facts fused: one
  check cannot test both, and neither half can be shared.
- **Grounding** — does the repository actually contain what the evidence names? A renamed file leaves
  an argument that still compiles, still renders, and is quietly false.
- **Reuse** — is the same fact argued twice under different words? jPipe unifies identical labels
  into one node, so sharing is mechanical: worded alike, a check runs once and supports two goals;
  worded differently, the work is done twice.
- **Conventions** — does the model sit right in the surrounding corpus?

Nothing is edited until you approve a numbered fix list, and every finding says what backs it — the
language, the argument model, or house practice — so you can tell a fact from an opinion.

## Reference material

The skill's `references/` are written to be read by people too, and they are the reason this repo
exists as more than a wrapper:

| | |
|---|---|
| [`language.md`](skills/jpipe-review/references/language.md) | The jPipe language, objectively — elements, the one `supports` relation and its legal pairings, `load`, templates, the two operators, and the `unified_N` renumbering hazard |
| [`abstraction.md`](skills/jpipe-review/references/abstraction.md) | The argument model: Toulmin's claim / grounds / warrant mapped onto jPipe's kinds, the fact → check → verdict ladder, atomicity, and the category errors |
| [`grounding.md`](skills/jpipe-review/references/grounding.md) | Checking evidence against the tree, and the discipline that keeps it from crying wolf |
| [`sharing.md`](skills/jpipe-review/references/sharing.md) | Finding facts argued twice, and why clustering by artifact beats clustering by string |
| [`conventions.md`](skills/jpipe-review/references/conventions.md) | McSCert corpus practice — refine placement, one entry point, provenance headers |
| [`rules.md`](skills/jpipe-review/references/rules.md) | The rule catalogue: id, authority, trigger, fix |

### On the argument model

Mapping jPipe onto Toulmin is **this repository's contribution**, not a claim about the language
designers' intent — neither Toulmin nor GSN is referenced anywhere else in the ecosystem. It earns
its place by making the rules explainable instead of merely asserted: *"this leaf is bad"* becomes
*"this is a Claim written into a Grounds slot"*, which tells you what to do about it.

Findings from it are tagged `authority: argument` and are always declinable. Worth knowing up front:
jPipe's own documentation uses `evidence e is "Test suite passes"` in its worked example, which this
reading flags. Optimising a language tour for brevity is fair; it just makes a poor argument.

## Development

```bash
python3 tools/validate_skills.py     # frontmatter, references, budgets, manifests
python3 tools/check_jd_blocks.py     # every published .jd example must compile (needs jpipe)
```

Both run in CI. The first is stdlib-only and needs no network.

A skill is prose — nothing executes it, so it fails silently. These tools catch the two ways that
happens: **structural rot** (a renamed reference file, a frontmatter name that drifts from its
directory, version skew between the manifests) and **factual rot** (an example in the docs that no
longer compiles). Fixtures live in [`tests/corpus/`](tests/corpus/), which has its own README.

### Adding a skill

Name it `jpipe-<verb>` and make the directory name match the frontmatter `name`. The `description`
must contain `Use when …` and at least one `NOT for …` clause naming the sibling that *does* cover
that case — auto-invocation degrades as a family grows unless each skill says what it is not.

Shared reference material currently lives inside `jpipe-review`. When a second skill needs the same
text, hoist the canon to a root `references/` and add a sync check to CI; the move is mechanical, and
it is deliberately deferred rather than forgotten.

### Before a release

`tools/` cannot test what the skill *concludes* — an LLM's prose report is not golden-testable. Run
these by hand and check the assertion, not the wording:

1. A clean model → no findings, **zero edits**.
2. A known-good multi-leg model → 🟢, and its evidence grounds against the real tree. *Guards against
   false positives, the failure mode that makes a reviewer useless.*
3. A model that does not compile → stops at the gate; no semantic review; does not re-explain the
   compiler.
4. A model with a broken `load` → caught, even though the fatal appears **only on stderr** with an
   empty Diagnostics section. *The bug most likely to ship.*
5. A leaf naming a nonexistent file → one `JD-G01`, citing the searches it ran.
6. `tests/corpus/shared/` → exactly one `JD-S01`, and **nothing** on the decoy.
7. `--apply`, answering *"1 and 3 only"* → exactly two edits, re-verified, nothing committed.

## License

MIT — see [LICENSE](LICENSE).
