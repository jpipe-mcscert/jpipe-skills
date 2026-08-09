#!/usr/bin/env python3
"""Compile every jPipe example this repository publishes.

Two sources, one rule: if we show it, it must build.

  * fenced ```jd blocks in the shared references/, the skills' markdown, and README.md
  * every .jd file under tests/corpus/

The corpus fixtures are *semantically* flawed on purpose -- that is what the
skill reviews -- but they must be syntactically valid, or they would be testing
the compiler instead of the skill. A doc example that stopped compiling is a
skill teaching a wrong pattern, which is why this runs in CI.

Blocks tagged ```text are fragments or deliberately-wrong snippets and are
skipped by design.

Usage:  python3 tools/check_jd_blocks.py [--root DIR] [--jpipe BIN]
Exit:   0 clean, 1 on any failure, 2 if jpipe is unavailable.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE_RE = re.compile(r"^```jd[ \t]*\n(.*?)^```", re.S | re.M)
SCAN_GLOBS = ("references/**/*.md", "skills/**/*.md", "README.md")


def compile_one(jpipe: str, path: Path) -> tuple[bool, str]:
    """Return (ok, detail). A file passes only on exit 0 with no diagnostics and
    a clean stderr -- a failed `load` is fatal and reports *only* on stderr while
    leaving the Diagnostics section empty."""
    try:
        proc = subprocess.run(
            [jpipe, "--headless", "diagnostic", "-i", str(path)],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return False, "timed out after 120s"

    problems = []
    if proc.returncode != 0:
        problems.append(f"exit {proc.returncode}")
    if "[ERROR]" in proc.stdout:
        problems.append("diagnostics reported")
    if proc.stderr.strip():
        problems.append("non-empty stderr (fatal)")
    if not problems:
        return True, ""

    detail = "; ".join(problems) + "\n"
    for line in proc.stdout.splitlines():
        if "[ERROR]" in line:
            detail += f"      {line.strip()}\n"
    for line in proc.stderr.splitlines()[:6]:
        if line.strip():
            detail += f"      stderr: {line.strip()}\n"
    return False, detail.rstrip()


def collect_blocks(root: Path, tmp: Path) -> list[tuple[str, Path]]:
    """Extract fenced jd blocks to real files; return (label, path) pairs."""
    out = []
    paths: list[Path] = []
    for pattern in SCAN_GLOBS:
        paths.extend(sorted(root.glob(pattern)))
    for md in paths:
        text = md.read_text(encoding="utf-8")
        for i, block in enumerate(FENCE_RE.findall(text)):
            rel = md.relative_to(root)
            dest = tmp / f"{str(rel).replace('/', '_')}.block{i}.jd"
            dest.write_text(block, encoding="utf-8")
            out.append((f"{rel} block {i}", dest))
    return out


def collect_fixtures(root: Path) -> list[tuple[str, Path]]:
    corpus = root / "tests" / "corpus"
    if not corpus.exists():
        return []
    return [(str(p.relative_to(root)), p) for p in sorted(corpus.rglob("*.jd"))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--jpipe", default="jpipe")
    args = parser.parse_args()

    jpipe = shutil.which(args.jpipe)
    if not jpipe:
        print(f"check_jd_blocks: {args.jpipe!r} not found on PATH", file=sys.stderr)
        return 2

    version = subprocess.run([jpipe, "--version"], capture_output=True, text=True).stdout.strip()
    print(f"check_jd_blocks: using {version or jpipe}")

    with tempfile.TemporaryDirectory() as tmpdir:
        targets = collect_blocks(args.root, Path(tmpdir)) + collect_fixtures(args.root)
        if not targets:
            print("check_jd_blocks: nothing to check", file=sys.stderr)
            return 1

        failures = []
        for label, path in targets:
            ok, detail = compile_one(jpipe, path)
            if not ok:
                failures.append((label, detail))
            print(f"  {'ok  ' if ok else 'FAIL'} {label}")

    print()
    if failures:
        print(f"check_jd_blocks: {len(failures)} of {len(targets)} failed\n", file=sys.stderr)
        for label, detail in failures:
            print(f"  {label}: {detail}", file=sys.stderr)
        return 1

    print(f"check_jd_blocks: OK ({len(targets)} examples)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
