# Pascha, Not "Easter"

**On Calendar, Tradition, and Restraint**

A booklet examining historical claims circulating in some evangelical and Hebrew-roots circles — that Constantine corrupted Christian doctrine at Nicaea, replaced Passover with a pagan holiday called "Easter," and imposed a new calendar to sever Christianity from its Jewish roots. The booklet shows, point by point, that these claims collapse under historical scrutiny.

Written by Marcus R., a layperson and householder who has lived inside Orthodox, Hebrew-roots, and evangelical charismatic traditions.

Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

## What makes this unusual

The booklet was independently reviewed by three AI systems — Claude Opus 4.6 (Anthropic), GPT 5.2 (OpenAI), and Gemini 1.5 Pro (Google) — and their commentary is included inline, unedited, for the reader to evaluate. Reviewer notes, fact-checks, disagreements, and corrections are all visible. The review process is part of the document.

## Structure

- **Introduction** — What is actually being claimed?
- **Part I: The Specific Claims, Examined** — Easter as a word, Melito of Sardis, the Ishtar/Asherah etymology, rabbits/eggs/folk practices, the biblical calendar, the Bishop of Jerusalem, the Quartodeciman controversy, what Nicaea actually decided
- **Part II: The Historical Context** — Late-antique rhetoric, the men who shaped Nicaea
- **Part III: The Larger Frame** — Providence, power, embodiment, messy conversion, fruit
- **Appendix 1** — Late-antique rhetoric examples (across targets)
- **Appendix 2** — Scholarly references with debate-level assessments
- **Appendix 3** — Summary of reviewer's assessment
- **Appendices 4–6** — Internal cautions against absolutizing practice (Rabbinic, Orthodox, Evangelical)
- **Personal Note** — The author's own journey across traditions
- **Appendices 7–8** — Closing remarks from Claude and GPT on the review process
- **Appendix 9** — Closing remarks from Gemini on historical asymmetry, AI and faith
- **Appendix 10** — Glossary of terms

## File organization

### Source files (author's content)

- `manuscript.txt` — The raw manuscript: all author-written prose, no formatting or commentary markup. This is the **source of truth** for the author's voice.
- `me.txt` — Original draft of the personal note (now incorporated into manuscript and .tex)
- `st-constantine.txt` — Research notes / source material on Constantine

### Rendered outputs

- `pascha-not-easter-booklet.tex` — Full LaTeX booklet with all content, reviewer commentary boxes, formatting, and layout. Currently the **most complete version** of the document.
- `cross-ornament-{1,2,3}.svg` — Decorative cross ornaments for the title page

### Archived

- `archived-html-versions/` — Earlier HTML rendering attempts (Python build scripts, HTML files, browser-rendered PDFs). Superseded by the LaTeX approach.

## Rendering strategy

The manuscript and the `.tex` file are currently **fully in sync** content-wise. The manuscript contains all author prose and all reviewer/AI commentary in plain-text format (using ASCII box borders). The `.tex` file renders the same content with LaTeX markup.

**Workflow going forward:** Maintain the raw manuscript (`manuscript.txt`) as the canonical source for **all** content — both author prose and commentary. The `.tex` file is a downstream rendering that adds:

- LaTeX formatting and layout (tcolorbox environments for commentary, titlesec styling, etc.)
- Typographic details (ornamental rules, colors, fonts, page geometry)

When new content is added — whether author prose or commentary — it should be written in `manuscript.txt` first, then formatted into the `.tex`. This keeps the door open for alternative renderings (EPUB, web, plain PDF) from the same manuscript source without having to reverse-engineer content out of LaTeX markup.

The manuscript uses a simple convention for commentary blocks:

```
  ┌─────────────────────────────────────────────────────────┐
  │ REVIEWER'S NOTE (Claude Opus 4.6, AI assistant):        │
  │                                                         │
  │ Commentary text here...                                 │
  └─────────────────────────────────────────────────────────┘
```

These map to `\begin{reviewerbox}`, `\begin{westernbox}`, `\begin{gptbox}`, and `\begin{reviewerfinalbox}` in the `.tex`.

## Building the PDF

Requires `pdflatex` (TeX Live or similar):

```bash
pdflatex pascha-not-easter-booklet.tex
pdflatex pascha-not-easter-booklet.tex   # run twice for TOC/refs
```

To use the SVG cross ornament on the title page, first convert to PDF:

```bash
inkscape cross-ornament-3.svg --export-filename=cross-ornament-3.pdf
```

Then uncomment the `\includegraphics` line in the .tex file (around line 221).

---

## Dev journal

Considerations, suggestions, and open questions logged during development. Each entry notes who raised it.

### 2026-02-27 — Layout fixes, content additions, and third reviewer (Claude Opus 4.6 + Marcus)

**Layout fixes (all done):**

- [x] Title page: "Winter 2026" → "Lent 2026"
- [x] Colophon: added "First edition" and CC BY 4.0 licensing
- [x] Epigraph attribution: "— after Vladimir Lossky"
- [x] Appendix numbering: forced arabic (1, 2, 3...) instead of LaTeX default letters
- [x] Added "How to use this booklet" page before epigraph
- [x] Made all commentary boxes breakable across page breaks
- [x] Fixed headheight warning
- [x] Fixed PDF bookmark warnings (added bookmark package, `\texorpdfstring` on subsection titles)
- [x] Visual distinction for Personal Note (custom title, no chapter number, gold rule)

**Content additions (all done):**

- [x] Quartodeciman controversy section (Polycarp/Anicetus, Victor, Irenaeus)
- [x] What Nicaea actually decided about Pascha (three determinations)
- [x] Melito of Sardis, *Peri Pascha* (c. 170 AD) — earliest Christian Paschal homily
- [x] Rabbits, eggs, and folk practices section
- [x] Glossary of terms (Appendix 10)
- [x] Personal letter: paragraphs on reading the Fathers and the Church's fixed prayers
- [x] GPT 5.2 commentary on all four new sections
- [x] Author prose tightened per GPT suggestions
- [x] Appendix 3 confirmed-items list updated (items 10–13)
- [x] Gemini 1.5 Pro closing remarks (Appendix 9) and four historical footnotes
- [x] Swapped Glossary and Gemini order (Gemini 9, Glossary 10)

### 2026-02-27 — Project cleanup (Marcus + Claude Opus 4.6)

- [x] Created `.gitignore`
- [x] Created `README.md`
- [x] Renamed `pascha-not-easter-booklet.txt` → `manuscript.txt` for clarity
- [x] Initialized git repo, pushed to private GitHub repository
- [x] Verified manuscript.txt and .tex are fully in sync (all content including commentary exists in both)
- [x] Documented manuscript ↔ .tex sync workflow in README
