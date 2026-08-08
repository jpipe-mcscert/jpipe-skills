# jpipe-skills

Reference [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for
[jPipe](https://www.jpipe.org), the justification / assurance-case language.

> [!CAUTION]
> **Experimental, and not part of jPipe core.** This repository is a research exploration of what
> LLM-based agents can usefully do with justification models. It is **not** a supported component of
> the jPipe toolchain, carries no stability guarantee, and its conventions may change or be abandoned
> without notice. The supported tools are the
> [compiler](https://github.com/jpipe-mcscert/jpipe-compiler), the
> [VS Code extension](https://github.com/jpipe-mcscert/jpipe-vscode), and the
> [runner](https://github.com/jpipe-mcscert/jpipe-runner).
>
> These skills read and propose edits to your models. Nothing is written without your approval, and
> the reasoning behind every finding is documented, but the judgement is a language model's, and it
> is yours to check.

## Install

Install as a plugin, which keeps itself updated:

```
/plugin marketplace add jpipe-mcscert/jpipe-skills
/plugin install jpipe-skills@jpipe
```

> [!NOTE]
> `/plugin` is a command of the `claude` terminal CLI. The VS Code and JetBrains extensions do not
> have it and answer `/plugin isn't available in this environment`. Install by hand there.

<details>
<summary>Installing by hand (works in every host)</summary>

Each directory under `skills/` is self-contained, so installing one means copying it where Claude
Code looks for skills.

For yourself, in every project:

```bash
git clone https://github.com/jpipe-mcscert/jpipe-skills.git
mkdir -p ~/.claude/skills
cp -r jpipe-skills/skills/jpipe-review ~/.claude/skills/
```

For one project, committed so that everyone who clones it gets the skill too:

```bash
mkdir -p <your-project>/.claude/skills
cp -r jpipe-skills/skills/jpipe-review <your-project>/.claude/skills/
```

Substitute `ln -s "$PWD/jpipe-skills/skills/jpipe-review"` for `cp -r` to track the repository
instead and pick up changes with a `git pull`.

Start a new session for a newly installed skill to be picked up.

</details>

## Skills

| Skill | What it does | Needs |
|---|---|---|
| [**jpipe-review**](skills/jpipe-review/) | Reviews the *argument* in an existing `.jd` model: whether its elements sit at the right level, rest on artifacts that exist, and fit the surrounding corpus. Syntax is left to the compiler. Proposes fixes; edits nothing until you approve them | [`jpipe`](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH` |

Each skill's directory has its own README.

## Authors

- Principal Investigator:
  - [Sébastien Mosser](https://mosser.github.io/), McSCert, McMaster University.

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
