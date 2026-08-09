#!/usr/bin/env python3
"""Keep vendored reference copies byte-identical to the canon.

Skills cannot share a references/ directory: each must stay self-contained so
that copying one into ~/.claude/skills/ still works. So shared text lives once
at the repository root and is *vendored* into each skill that needs it.

The rule is deliberately zero-config. For every references/<name>.md at the
root, any skills/*/references/<name>.md that already exists must match it
byte-for-byte. A skill opts in by having the file; nothing enumerates anything,
so there is no list to forget to update.

  python3 tools/sync_refs.py            copy canon over every existing copy
  python3 tools/sync_refs.py --check    report drift and exit 1 (this is CI)

--check is the CI gate; the bare form is the fix. Nothing here ever *creates* a
copy: vendoring a file into a skill for the first time is a deliberate act, so
you copy it by hand once, and this tool keeps it honest afterwards.

Usage:  python3 tools/sync_refs.py [--check] [--root DIR]
Exit:   0 clean (or synced), 1 on drift under --check, 2 on a layout problem.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def canon_files(root: Path) -> list[Path]:
    """The shared reference material, at the repository root."""
    canon_dir = root / "references"
    if not canon_dir.is_dir():
        return []
    return sorted(p for p in canon_dir.glob("*.md") if p.is_file())


def copies_of(root: Path, canon: Path) -> list[Path]:
    """Every skill that has vendored this canon file, by its existence."""
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return []
    found = []
    for skill in sorted(d for d in skills_dir.iterdir() if d.is_dir()):
        candidate = skill / "references" / canon.name
        if candidate.is_file():
            found.append(candidate)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                       help="report drift instead of fixing it")
    parser.add_argument("--root", type=Path,
                       default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()

    canon = canon_files(root)
    if not canon:
        print(f"sync_refs: no canon found at {root / 'references'}", file=sys.stderr)
        return 2

    drifted: list[Path] = []
    synced: list[Path] = []
    vendored = 0

    for source in canon:
        want = source.read_bytes()
        for copy in copies_of(root, source):
            vendored += 1
            if copy.read_bytes() == want:
                continue
            if args.check:
                drifted.append(copy)
            else:
                shutil.copyfile(source, copy)
                synced.append(copy)

    names = ", ".join(p.name for p in canon)
    if args.check:
        if drifted:
            print(f"sync_refs: {len(drifted)} vendored copy/copies drifted from the canon\n")
            for copy in drifted:
                print(f"  {copy.relative_to(root)}")
            print("\nThe canon at references/ is the source of truth. If your edit belongs")
            print("in the shared text, make it there; then run:\n")
            print("  python3 tools/sync_refs.py")
            return 1
        print(f"sync_refs: OK ({vendored} vendored cop(y/ies) of {len(canon)}: {names})")
        return 0

    for copy in synced:
        print(f"  updated {copy.relative_to(root)}")
    print(f"sync_refs: {len(synced)} updated, {vendored} vendored cop(y/ies) of {len(canon)}: {names}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
