# jpipe-skills

Reference [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for
[jPipe](https://www.jpipe.org), the justification / assurance-case language.

> [!CAUTION]
> **Do not use generative AI to write a safety case.** An assurance case is a claim somebody is
> accountable for. Text that merely reads like an argument is worse than no argument at all, because
> it persuades without anyone having reasoned about the system, and a reviewer cannot tell the two
> apart by reading. These skills are built to **review an argument a human wrote**, never to author
> one, and every finding is a proposal you accept or reject. The responsibility for the case stays
> with its author.
>
> **Experimental, and not part of jPipe core.** This repository is a research exploration of what
> LLM-based agents can usefully do with justification models. It is **not** a supported component of
> the jPipe toolchain, carries no stability guarantee, and its conventions may change or be abandoned
> without notice. The supported tools are the
> [compiler](https://github.com/jpipe-mcscert/jpipe-compiler), the
> [VS Code extension](https://github.com/jpipe-mcscert/jpipe-vscode), and the
> [runner](https://github.com/jpipe-mcscert/jpipe-runner).

## Authors

- Principal Investigator:
  - [Sébastien Mosser](https://mosser.github.io/), McSCert, McMaster University.

## Skills

| Skill | What it does | Needs |
|---|---|---|
| [**jpipe-review**](skills/jpipe-review/) | Reviews the *argument*: whether its elements sit at the right level, rest on artifacts that exist, and follow the house style. Syntax is left to the compiler. Proposes fixes; edits nothing until you approve them | nothing to report; [`jpipe`](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH` to apply fixes |
| [**jpipe-survey**](skills/jpipe-survey/) | Surveys how models *relate*: the same fact argued twice under wordings that will not match, labels identical enough to merge into a claim nobody wrote, and leaves that assert what another model already proves. Asks you to confirm what the files cannot settle | same |

Both take the same scope: **one `.jd` file plus everything it transitively `load`s**, since a goal
assembled from four requirement files is one argument rather than four. Pass `--global` to scope either
to every `.jd` in the repository. No file, or more than one, is an error rather than a guess.

The split between them is deliberate. **`jpipe-review` examines the elements of one argument;
`jpipe-survey` compares separate arguments with each other.** A clean review and a clean survey are
different claims, and a corpus wants both.

Each skill's directory has its own README.

## Install

Install as a plugin:

```
/plugin marketplace add jpipe-mcscert/jpipe-skills
/plugin install jpipe-skills@jpipe
```

> [!NOTE]
> `/plugin` is a command of the `claude` terminal CLI. The VS Code and JetBrains extensions do not
> have it and answer `/plugin isn't available in this environment`. Install by hand there.

## Update

Claude Code disables auto-update for third-party marketplaces by default, so a plugin install of this
repository does **not** keep itself current. Refresh the catalog, then update the plugin:

```
/plugin marketplace update jpipe
/plugin update jpipe-skills@jpipe
```

Then `/reload-plugins` to apply it in the session you are in, or start a new one.

To stop doing that by hand, turn auto-update on for this marketplace: run `/plugin`, go to
**Marketplaces**, select **jpipe**, and choose **Enable auto-update**. Claude Code then refreshes
after startup, with a random delay of up to ten minutes, and prompts you to `/reload-plugins` when
something changed.

<details>
<summary>Checking, and updating a hand install</summary>

Which version you have, next to what the catalog offers:

```
/plugin list
```

A hand install is a copy, so it does not update. Re-copy over it, from a fresh clone:

```bash
git -C jpipe-skills pull --ff-only
cp -r jpipe-skills/skills/jpipe-review jpipe-skills/skills/jpipe-survey ~/.claude/skills/
```

If you symlinked instead of copying, the `git pull` is the whole update.

</details>

> [!IMPORTANT]
> Updates are gated on the `version` field in `.claude-plugin/plugin.json`. Claude Code ships a new
> version to installed plugins only when that field changes, so pushing to `main` alone reaches
> nobody. Anyone releasing here bumps it: see the checklist in
> [CONTRIBUTING.md](CONTRIBUTING.md#releasing).

<details>
<summary>Installing by hand (works in every host)</summary>

Each directory under `skills/` is self-contained, so installing one means copying it where Claude
Code looks for skills. Shared reference text is vendored into each skill rather than linked between
them, which is what makes copying just one work.

For yourself, in every project:

```bash
git clone https://github.com/jpipe-mcscert/jpipe-skills.git
mkdir -p ~/.claude/skills
cp -r jpipe-skills/skills/jpipe-review jpipe-skills/skills/jpipe-survey ~/.claude/skills/
```

For one project, committed so that everyone who clones it gets the skill too:

```bash
mkdir -p <your-project>/.claude/skills
cp -r jpipe-skills/skills/jpipe-review <your-project>/.claude/skills/
cp -r jpipe-skills/skills/jpipe-survey <your-project>/.claude/skills/
```

Substitute `ln -s "$PWD/jpipe-skills/skills/<name>"` for `cp -r` to track the repository instead and
pick up changes with a `git pull`.

Start a new session for a newly installed skill to be picked up.

</details>

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the tooling, the conventions for adding a skill, and the
pre-release checklist.

## Sponsors

We acknowledge the support of the _Natural Sciences and Engineering Research Council of Canada_
(NSERC) to support this research.

<div align="center">
  <img alt="NSERC logo" src="./docs/sponsors/nserc.svg" width="300">
</div>

## License

MIT. See [LICENSE](LICENSE).
