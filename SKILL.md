---
name: artifact-standard
description: The user's house standard for every artifact page (any project): a 한글 · EN language toggle top-right (Korean default) and an always-visible 편집하기 (Edit) button bottom-right with in-page edit mode saved through the artifact capability. Load this before writing or republishing ANY artifact HTML page (reports, briefs, docs, dashboards, case studies). It ships the two shared pieces and the build step.
---

# Artifact standard: 한글 · EN toggle + 편집하기

Every artifact page for this user has, no exceptions:

1. **Language toggle** top-right: 한글 / EN pills, Korean shown first, choice kept in `localStorage['claude-artifact.lang']`. Every heading, paragraph, label, table cell and caption exists in both languages.
2. **편집하기 (Edit) button** bottom-right, always visible to people who can edit the artifact. In-page edit mode: text edits, block reordering, side-by-side rows, undo/redo, autosave to `data/edits.json` through the `artifact` capability, so the next viewer sees the edits.

Both come from the pet game concept doc v2 and are kept here as drop-in files. Don't rewrite them; include them.

## Default look: the full-diagnosis document style

Unless the user names another theme (a client's brand, the Shop Vitals report ivory/gold, the pet game), use `shared/theme-review.css`: the Complete Elixir marketing review look. White page, ink text, muted gold accent, Cormorant Garamond display + Inter body + Noto Sans KR for Korean, generous spacing, eyebrow + lede + sections, `.card`, `.kpi`, `.pill.good/.warn/.crit`, `.tbl`, `.grid.g2/.g3`, `.band`, `.callout`, `.steps`, `.phase`. Include it inline with `<!-- @include shared/theme-review.css -->` inside the page's `<style>`, then add the page's own rules after it. Load its Google Fonts link from the comment at the top of the file.

## How to build a page

1. Write the page as `page.html` (the Artifact tool's page body: `<title>`, `<style>`, content; no `<html>/<head>/<body>`).
   - Put all content inside `<div class="wrap">…</div>` (the edit mode needs it).
   - Write text in pairs: `<p lang="ko">…</p><p lang="en">…</p>`, or inside one element `<span lang="ko">…</span><span lang="en">…</span>`. `class="ko"` / `class="en"` pairs work too (the review document used them). Elements with neither show in both languages (numbers, symbols, brand names).
   - Korean keeps the English product/marketing terms the user uses (SEO, funnel, Add to cart, Search Console…).
   - Define these CSS tokens on `:root` (and in the dark blocks): `--bg --surface --fg --muted --line --accent --accent-ink --accent-soft --font-body --font-mono`, plus the toggle colours `--lt-bg --lt-line --lt-fg --lt-on --lt-on-fg`. The edit bar and toggle are styled from them.
   - Add `[hidden]{display:none!important}` if the page uses grid/flex on hidden blocks.
2. Insert the two pieces:
   ```html
   <!-- @include shared/lang-toggle.html -->      ← right after <style>, before .wrap
   …page content…
   <script>
   window.PB_EDIT = {
     wrap: '.wrap',
     edit: 'h1,h2,h3,p,li,td,th,.eyebrow,.meta,.lbl,footer',   // editable text
     noEdit: 'svg,table,.table-scroll',                           // never editable
     unit: 'h1,.card',                                            // moved as one block
     cont: 'header,section,.sec-head,.stack,.grid-2,.grid-3,.card', // containers whose children can be reordered
     noCont: 'svg,table,.table-scroll',
     stash: '<page-name>-edit-stash'
   };
   </script>
   <!-- @include shared/edit-mode.html -->           ← last thing in the file
   ```
3. Build: `python3 ~/.claude/skills/artifact-standard/tools/include.py page.html index.html` (run from a folder that has `shared/` next to it, or copy `~/.claude/skills/artifact-standard/shared/` beside `page.html` first; the include path is relative to the folder you run in, see the script's docstring).
4. Create an empty edits file: `mkdir -p data && echo '{}' > data/edits.json`.
5. Publish with the Artifact tool from the working directory or the scratchpad (it refuses other paths):
   `file_path: <dir>/index.html`, `root: <dir>`, `files: {"data/edits.json": "data/edits.json"}`, `capabilities: {artifact: {}}`.
   On a republish, keep `capabilities` (omit it to carry it forward) and do **not** resend `data/edits.json`, or you overwrite the user's edits.
6. Check once in headless Chrome: Korean blocks visible by default, all hidden after clicking `[data-set-lang="en"]`, `.e-bar` present, no horizontal overflow, no console errors.

## Scripted text

Text that JavaScript writes (chart labels, counters) picks the language with `document.documentElement.dataset.lang` (`'ko' | 'en'`) and redraws on the `claude-artifact:lang` event. `aria-label`, `alt` and `title` take their English in `data-en-aria-label` etc.

## When the page is a typed Artifact (Docs, Slides, Dashboard)

Those types can't carry the toggle or the edit button. For a document the user will read in both languages, build a plain HTML page with this standard instead, unless the user asks for that type by name.

## Reference

- Pieces: `shared/lang-toggle.html` (4 KB), `shared/edit-mode.html` (75 KB), `shared/theme-review.css` (12 KB), `tools/include.py`.
- First pages built this way: pet game concept doc v2, Shop Vitals opportunity brief (`/Volumes/hello ssd/shop-vitals/docs/opportunity/page.html`).
- The user's words (2026-10-26): "언제나 아티팩트 만들때 펫게임 만들때 임플레멘트한 에디팅 시스템 꼭 임플레멘트해줘 그리고 한글영어 토글도 언제나."
