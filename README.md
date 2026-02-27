# Pascha, Not "Easter"

**On Calendar, Tradition, and Restraint**

A booklet examining historical claims circulating in some evangelical and Hebrew-roots circles — that Constantine corrupted Christian doctrine at Nicaea, replaced Passover with a pagan holiday called "Easter," and imposed a new calendar to sever Christianity from its Jewish roots. The booklet shows, point by point, that these claims collapse under historical scrutiny.

Written by Marcus R., a layperson and householder who has lived inside Orthodox, Hebrew-roots, and evangelical charismatic traditions.

## What makes this unusual

The booklet was independently reviewed by two AI systems — Claude Opus 4.6 (Anthropic) and GPT 5.2 (OpenAI) — and their commentary is included inline, unedited, for the reader to evaluate. Reviewer notes, fact-checks, disagreements, and corrections are all visible. The review process is part of the document.

## Structure

- **Introduction** — What is actually being claimed?
- **Part I: The Specific Claims, Examined** — Easter as a word, the Ishtar/Asherah etymology, the biblical calendar, the Bishop of Jerusalem
- **Part II: The Historical Context** — Late-antique rhetoric, the men who shaped Nicaea
- **Part III: The Larger Frame** — Providence, power, embodiment, messy conversion, fruit
- **Appendix 1** — Late-antique rhetoric examples (across targets)
- **Appendix 2** — Scholarly references with debate-level assessments
- **Appendix 3** — Summary of reviewer's assessment
- **Appendices 4–6** — Internal cautions against absolutizing practice (Rabbinic, Orthodox, Evangelical)
- **Personal Note** — The author's own journey across traditions
- **Appendices 7–8** — Closing remarks from Claude and GPT on the review process

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

### 2026-02-27 — Layout and content review (Claude Opus 4.6)

**Layout suggestions:**

- [ ] Title page says "Winter 2026" — should probably be "Lent 2026" or just "2026" since distribution is around Pascha
- [ ] Copyright/colophon page is thin — consider adding licensing (CC BY? Public domain?), edition number
- [ ] Epigraph is a composite paraphrase of Lossky, not a direct quote — needs attribution or reframing ("after Vladimir Lossky")
- [ ] Appendix numbering mismatch: LaTeX generates "Appendix A, B, C..." but prose refers to "Appendix 1, 2, 3..." — pick one convention
- [ ] Cross ornament on title page uses a scaled `+` sign — convert one of the SVG ornaments to PDF for the real thing
- [ ] `colorlinks=true` is good for screen but consider a print variant with `hidelinks`
- [ ] Check TOC length in compiled PDF — may want `\setcounter{tocdepth}{0}` or `{1}` if it runs long
- [ ] Part title pages may need `\thispagestyle{empty}` for consistent footer treatment

**Content gaps identified:**

- [ ] **Quartodeciman controversy** — mentioned in Claude's closing remarks but never gets its own section. The 2nd-century debate about *when* to celebrate Pascha (Polycarp vs. Anicetus, Victor vs. the Asian churches) is the most important historical precedent. A short section in Part I or II would show the dating question long predated Constantine.
- [ ] **What Nicaea actually decided about Pascha** — the booklet refutes what Nicaea *didn't* do but never concisely states what it *did* decide (celebrate on the same day everywhere, on a Sunday, calculated independently from the Jewish calendar). A brief positive statement would orient confused readers.
- [ ] **Melito of Sardis, *Peri Pascha*** — one of the earliest Christian homilies (c. 170 AD), explicitly linking Christ to the Passover lamb, 150+ years before Nicaea. Powerful data point against "Constantine changed it."
- [ ] **Rabbits/eggs/folk practices** — the popular "Easter is pagan" claim often centers on bunnies and eggs, not just etymology. A short paragraph noting that egg symbolism entered through medieval folk custom (not Nicaea) and that Orthodox tradition has its own egg tradition (red eggs, Mary Magdalene) would close this gap.
- [ ] **Glossary** — terms like *oikonomia*, *akribeia*, *pikuach nefesh*, *Quartodeciman* could use a brief glossary for the evangelical target audience.
- [ ] **"How to use this booklet" note** — a brief front-matter note ("for personal study and small group discussion, not as a weapon") would align with the booklet's own ethos of restraint.

### 2026-02-27 — Project cleanup (Marcus + Claude Opus 4.6)

- [x] Created `.gitignore`
- [x] Created `README.md`
- [x] Renamed `pascha-not-easter-booklet.txt` → `manuscript.txt` for clarity
- [x] Initialized git repo, pushed to private GitHub repository
- [x] Verified manuscript.txt and .tex are fully in sync (all content including commentary exists in both)
- [x] Documented manuscript ↔ .tex sync workflow in README
