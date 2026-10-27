#!/usr/bin/env python3
"""Inline shared pieces into an artifact page.

Replaces every <!-- @include path --> line in the source page with that file, looked up
next to the page, one folder up, then in this skill (shared/…), and writes the result.
Usage: python3 tools/include.py docs/archetype/page.html docs/archetype/index.html
"""
import pathlib
import re
import sys

skill = pathlib.Path(__file__).resolve().parent.parent
src, dst = (pathlib.Path(a) for a in sys.argv[1:3])
text = src.read_text()

def piece(name):
    # next to the page first, then the skill's own shared/ folder
    for base in (src.resolve().parent, src.resolve().parent.parent, skill):
        f = base / name
        if f.exists():
            return f.read_text()
    raise SystemExit(f'include not found: {name}')

text = re.sub(r'<!-- @include (\S+) -->', lambda m: piece(m.group(1)), text)
dst.write_text(text)
print(f'wrote {dst} ({len(text) // 1024} KB)')
