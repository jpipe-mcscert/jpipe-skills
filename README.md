# jpipe-skills

Reference [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for
[jPipe](https://www.jpipe.org), the justification / assurance-case language.

> [!DANGER]
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

```
/plugin marketplace add jpipe-mcscert/jpipe-skills
/plugin install jpipe-skills@jpipe
```

Each directory under `skills/` is self-contained, so plain copying works too:
`cp -r skills/jpipe-review ~/.claude/skills/`.

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
