# jpipe-skills

Reference [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for
[jPipe](https://www.jpipe.org), the justification / assurance-case language.

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
| [**jpipe-review**](skills/jpipe-review/) | Reviews the *argument* in an existing `.jd` model — whether its elements sit at the right level, rest on artifacts that exist, and fit the surrounding corpus. Syntax is left to the compiler. Proposes fixes; edits nothing until you approve them | [`jpipe`](https://github.com/jpipe-mcscert/jpipe-compiler) on `PATH` |

Each skill's directory has its own README.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the tooling, the conventions for adding a skill, and the
pre-release checklist.

## License

MIT — see [LICENSE](LICENSE).
