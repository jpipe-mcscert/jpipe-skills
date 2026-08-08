#!/usr/bin/env python3
"""Lint the skills and plugin manifests in this repository.

A skill is prose: nothing executes it, so its failure mode is silent. A renamed
reference file or a frontmatter name that drifts from its directory does not
raise an error at runtime -- the skill just quietly degrades into guesswork.
This script catches that class of rot. It needs no network and no jpipe.

Usage:  python3 tools/validate_skills.py [--root DIR]
Exit:   0 clean, 1 on any error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^jpipe-[a-z0-9]+(-[a-z0-9]+)*$")
RULE_ID_RE = re.compile(r"\bJD-[AGSC]\d{2}\b")
REF_MENTION_RE = re.compile(r"references/([A-Za-z0-9_.-]+\.md)")

MAX_SKILL_LINES = 160
MAX_REFERENCE_LINES = 400
MAX_DESCRIPTION_CHARS = 1024
MAX_FILE_BYTES = 40 * 1024

REQUIRED_FRONTMATTER = ("name", "description", "argument-hint", "allowed-tools")

# A skill must not instruct version-control side effects. The guardrail is
# textual, so it is linted textually.
FORBIDDEN = (
    "$ARGUMENTS",
    "git commit",
    "git push",
    "git add",
    "gh pr create",
    "gh pr merge",
)

KNOWN_TOOLS = {
    "Bash", "Read", "Write", "Edit", "Grep", "Glob", "WebFetch", "WebSearch",
    "Task", "Agent", "NotebookEdit", "TodoWrite",
}

# Tools that exist but that skills here must not declare. Enforced only at the
# declaration site: a skill cannot call what it does not declare, so scanning
# prose for the name as well would just stop the documentation from explaining
# the rule.
DISALLOWED_TOOLS = {
    "AskUserQuestion": "ask in prose, which also works in a headless run where "
                       "an interactive picker cannot be answered",
}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse the leading --- block. Deliberately minimal: top-level `key: value`
    pairs only, which is all a SKILL.md frontmatter is allowed to contain."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        if key != key.strip():  # indented -> nested, which we do not allow
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def check_skill(skill_dir: Path, errors: list[str]) -> None:
    rel = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{rel}: no SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{rel}/SKILL.md: frontmatter does not parse")
        return

    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            errors.append(f"{rel}/SKILL.md: missing frontmatter field '{field}'")

    name = fm.get("name", "")
    if not NAME_RE.match(name):
        errors.append(f"{rel}/SKILL.md: name '{name}' must match ^jpipe-<verb>[-<verb>]*$")
    if name != skill_dir.name:
        errors.append(f"{rel}/SKILL.md: name '{name}' != directory '{skill_dir.name}'")

    desc = fm.get("description", "")
    if len(desc) > MAX_DESCRIPTION_CHARS:
        errors.append(f"{rel}/SKILL.md: description is {len(desc)} chars (max {MAX_DESCRIPTION_CHARS})")
    if "Use when" not in desc:
        errors.append(f"{rel}/SKILL.md: description must contain 'Use when'")
    if "NOT for" not in desc:
        errors.append(f"{rel}/SKILL.md: description must contain at least one 'NOT for'")

    for tool in (t.strip() for t in fm.get("allowed-tools", "").split(",")):
        if not tool or tool.startswith("mcp__"):
            continue
        if tool in DISALLOWED_TOOLS:
            errors.append(
                f"{rel}/SKILL.md: '{tool}' must not be declared in allowed-tools; "
                f"{DISALLOWED_TOOLS[tool]}"
            )
        elif tool not in KNOWN_TOOLS:
            errors.append(f"{rel}/SKILL.md: unknown tool '{tool}' in allowed-tools")

    body_lines = text.count("\n") + 1
    if body_lines > MAX_SKILL_LINES:
        errors.append(f"{rel}/SKILL.md: {body_lines} lines (max {MAX_SKILL_LINES})")

    # Every references/... path named in SKILL.md must exist. This is the
    # highest-value check here: a dangling reference is invisible at runtime.
    for mentioned in sorted(set(REF_MENTION_RE.findall(text))):
        if not (skill_dir / "references" / mentioned).exists():
            errors.append(f"{rel}/SKILL.md: references/{mentioned} does not exist")

    for path in sorted(skill_dir.rglob("*.md")):
        rel_path = path.relative_to(skill_dir.parent)
        content = path.read_text(encoding="utf-8")
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{rel_path}: {path.stat().st_size} bytes (max {MAX_FILE_BYTES})")
        if path.name != "SKILL.md":
            lines = content.count("\n") + 1
            if lines > MAX_REFERENCE_LINES:
                errors.append(f"{rel_path}: {lines} lines (max {MAX_REFERENCE_LINES})")
        for bad in FORBIDDEN:
            if bad in content:
                errors.append(f"{rel_path}: contains forbidden string {bad!r}")

    check_rule_ids(skill_dir, errors)


def check_rule_ids(skill_dir: Path, errors: list[str]) -> None:
    """Every rule id cited anywhere in the skill must be defined in rules.md,
    and every rule in rules.md must carry an authority tag."""
    catalogue = skill_dir / "references" / "rules.md"
    if not catalogue.exists():
        return
    cat_text = catalogue.read_text(encoding="utf-8")

    defined = set()
    for line in cat_text.splitlines():
        m = re.match(r"\|\s*([AGSC]\d{2})\s*\|", line)
        if m:
            defined.add("JD-" + m.group(1))

    for path in sorted(skill_dir.rglob("*.md")):
        cited = set(RULE_ID_RE.findall(path.read_text(encoding="utf-8")))
        for rule in sorted(cited - defined):
            errors.append(
                f"{path.relative_to(skill_dir.parent)}: cites {rule}, "
                f"which is not defined in references/rules.md"
            )

    for family, authority_marker in (("A", "authority: argument"),
                                     ("G", "authority: argument"),
                                     ("C", "authority: house")):
        header = re.search(rf"^## JD-{family} .*$", cat_text, re.M)
        if header and authority_marker not in header.group(0):
            errors.append(f"rules.md: JD-{family} section header lacks '{authority_marker}'")


def check_manifests(root: Path, errors: list[str]) -> None:
    plugin_path = root / ".claude-plugin" / "plugin.json"
    market_path = root / ".claude-plugin" / "marketplace.json"
    for path in (plugin_path, market_path):
        if not path.exists():
            errors.append(f"{path.relative_to(root)}: missing")
            return
    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        market = json.loads(market_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f".claude-plugin: invalid JSON -- {exc}")
        return

    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
    if not entries:
        errors.append(
            f"marketplace.json: no plugins[] entry named {plugin.get('name')!r} "
            f"(found {[p.get('name') for p in market.get('plugins', [])]})"
        )
        return
    if entries[0].get("version") != plugin.get("version"):
        errors.append(
            f"version skew: plugin.json {plugin.get('version')!r} != "
            f"marketplace entry {entries[0].get('version')!r}"
        )


def check_house_style(root: Path, errors: list[str]) -> None:
    """No em dashes anywhere. House style: use a colon, a comma, parentheses, or
    a second sentence instead. Enforced rather than remembered, because a single
    stray one in a pull request is easy to wave through."""
    targets = sorted(root.glob("*.md"))
    targets += sorted(root.glob("skills/**/*.md"))
    targets += sorted(root.glob("tests/**/*.md"))
    targets += sorted(root.glob(".claude-plugin/*.json"))
    for path in targets:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "—" in line:
                errors.append(f"{path.relative_to(root)}:{lineno}: em dash; rephrase")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()

    errors: list[str] = []
    skills_dir = args.root / "skills"
    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir()) if skills_dir.exists() else []
    if not skill_dirs:
        errors.append("skills/: no skill directories found")

    for skill_dir in skill_dirs:
        check_skill(skill_dir, errors)
    check_manifests(args.root, errors)
    check_house_style(args.root, errors)

    if errors:
        print(f"validate_skills: {len(errors)} error(s)\n", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"validate_skills: OK ({len(skill_dirs)} skill(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
