# artifact-standard

A Claude Code skill: every artifact page gets a **한글 · EN language toggle** (top right, Korean default) and an **always-visible 편집하기 / Edit button** (bottom right) with in-page editing saved through the artifact capability. Ships the two drop-in pieces, the full-diagnosis document theme and a one-line build step.

## Install

```bash
git clone https://github.com/FenixJung/artifact-standard ~/.claude/skills/artifact-standard
```

Then add to `~/.claude/CLAUDE.md`:

```
- Load the `artifact-standard` skill before writing or republishing any artifact HTML page.
```

## What's inside

| File | What |
|---|---|
| `SKILL.md` | the rules and build steps Claude follows |
| `shared/lang-toggle.html` | the 한글 · EN toggle (works with `lang="ko"/"en"` or `class="ko"/"en"` pairs) |
| `shared/edit-mode.html` | in-page edit mode: text edits, reordering, rows, undo/redo, autosave to `data/edits.json` |
| `shared/theme-review.css` | the default look (white, ink, muted gold; Cormorant Garamond + Inter + Noto Sans KR) |
| `tools/include.py` | `python3 tools/include.py page.html index.html` inlines the `<!-- @include … -->` pieces |

## Build a page

1. Write `page.html` with everything inside `<div class="wrap">`, text in `lang="ko"` / `lang="en"` pairs.
2. Add `<!-- @include shared/lang-toggle.html -->` after `<style>`, set `window.PB_EDIT` selectors, and end with `<!-- @include shared/edit-mode.html -->`.
3. `python3 ~/.claude/skills/artifact-standard/tools/include.py page.html index.html`
4. `mkdir -p data && echo '{}' > data/edits.json`
5. Publish `index.html` with `files: {"data/edits.json": …}` and `capabilities: {artifact: {}}`.

The edit mode and toggle were first built for the Pet Battle concept doc v2; the theme comes from the Complete Elixir marketing review (October 2026). MIT.
