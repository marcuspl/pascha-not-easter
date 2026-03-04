import re, os

with open('/home/marcus/code/new/writings/easter/manuscript.txt', 'r') as f:
    raw = f.read()
with open('/home/marcus/code/new/writings/easter/cross-ornament-3.svg', 'r') as f:
    svg = f.read()

lines = raw.split('\n')

def classify_lines(lines):
    elements = []
    i = 0
    seen_main_title = False
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            i += 1
            continue
        
        if not seen_main_title:
            if stripped.startswith('PASCHA, NOT'):
                seen_main_title = True
                elements.append(('main_title', stripped))
                i += 1
                if i < len(lines) and lines[i].strip():
                    elements.append(('main_subtitle', lines[i].strip()))
                    i += 1
            else:
                i += 1
            continue
        
        if re.match(r'^═{10,}$', stripped):
            i += 1
            continue
        
        if stripped == '⸻':
            elements.append(('divider', ''))
            i += 1
            continue
        
        m = re.match(r'^PART (I+)$', stripped)
        if m:
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            subtitle = lines[i].strip() if i < len(lines) else ''
            elements.append(('part_header', (m.group(1), subtitle)))
            i += 1
            continue
        
        m = re.match(r'^APPENDIX (\d+)$', stripped)
        if m:
            num = m.group(1)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            title_lines = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^═{10,}$', lines[i].strip()):
                title_lines.append(lines[i].strip())
                i += 1
            title = ' '.join(title_lines)
            elements.append(('appendix_header', (num, title)))
            continue
        
        if stripped == 'A PERSONAL NOTE FROM THE AUTHOR':
            elements.append(('personal_header', ''))
            i += 1
            continue
        
        # Reviewer boxes
        if stripped.startswith('┌─'):
            box_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('└─'):
                raw_line = lines[i]
                cleaned = re.sub(r'^\s*│\s?', '', raw_line)
                cleaned = re.sub(r'\s*│\s*$', '', cleaned)
                box_lines.append(cleaned)
                i += 1
            i += 1
            box_text = '\n'.join(box_lines).strip()
            
            if 'Second opinion' in box_text or 'GPT' in box_text:
                elements.append(('gpt_box', box_text))
            elif 'Why this matters' in box_text or 'A final word' in box_text or 'On Appendices 4, 5, and 6' in box_text or 'On the personal letter' in box_text:
                elements.append(('western_box', box_text))
            else:
                elements.append(('reviewer_box', box_text))
            continue
        
        # Section headers
        section_keywords = [
            'introduction: what', 'easter as a germanic', '"easter" from asherah', 
            'rabbits, eggs, and other', 'there is no real', 'bishop of jerusalem', 
            'the quartodeciman controversy', 'what nicaea actually decided', 'anti-jewish', 
            'lineage, authority', 'providence, not', 'power redirected', 'why embodiment',
            'constantine the great as', 'messy conversion', 'judging by fruit',
            'restrained theological', 'who am i', 'on the format', "on gpt's contributions",
            'where i would still push back', 'on the bigger picture', "on claude's assessment",
            "on claude's gentle pushback", 'on the broader project', 'the end of historical asymmetry',
            "the refiner's fire", 'computation vs. communion'
        ]
        subsection_keywords = [
            'pagan religion', 'pagan culture', 'intra-christian', 'pastoral invective',
            'schismatics and', 'non-roman', 'ethnic stereotyping', 'imperial rhetoric',
            'freedom of conscience', 'warning against returning', 'distinguishing gospel',
            'unity without enforced', 'spirit over technique', 'candid evangelical',
            'torah was not given', 'preservation of life', 'these and those',
            'warning against excessive', 'calendar authority', 'unity does not require',
            'tradition is lived', 'excessive rigor', 'church applies', 'sacred time serves',
            'representative rabbinic', 'representative orthodox', 'representative evangelical',
            'the ishtar question', 'the calendar', "constantine's letter",
            'evangelicalism', 'cassian', 'postscript',
            '1. late-antique rhetoric', '2. anti-judaism vs', '3. intra-christian polemic',
            '4. roman imperial rhetoric', '5. constantine & nicaea', '6. where real debate',
            'original greek', 'aramaic peshitta', 'hebrew translations', 'latin vulgate',
            'classic english translations', 'major modern translations', 'notable paraphrases',
            'messianic / jewish-oriented', 'other notable renderings', 'translation notes'
        ]
        
        is_main_section = any(kw in stripped.lower() for kw in section_keywords)
        is_subsection = any(kw in stripped.lower() for kw in subsection_keywords)
        
        if (is_main_section or is_subsection) and len(stripped) < 100:
            if i + 1 < len(lines) and not lines[i+1].strip():
                if is_main_section:
                    elements.append(('h3', stripped))
                else:
                    elements.append(('h4', stripped))
                i += 1
                continue
        
        # Special bold headers
        if stripped in ('CONFIRMED AS ACCURATE:', 'WHERE THE TEXT COULD BE STRONGER:', 'OVERALL ASSESSMENT:'):
            elements.append(('h4_bold', stripped))
            i += 1
            continue
        if stripped.startswith('Scholars do debate:') or stripped.startswith('Scholars do not seriously debate:'):
            elements.append(('h4_bold', stripped))
            i += 1
            continue
        
        # Bib metadata
        if re.match(r'^\s*Status:\s', stripped) or re.match(r'^\s*Debate level:\s', stripped):
            elements.append(('bib_meta', stripped))
            i += 1
            continue
        if re.match(r'^\s*Contribution:', stripped) or re.match(r'^\s*Relevance:', stripped):
            elements.append(('bib_label', stripped))
            i += 1
            continue
        
        # List items
        if stripped.startswith('- ') or stripped.startswith('• '):
            list_items = [stripped[2:]]
            i += 1
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('• ')):
                list_items.append(lines[i].strip()[2:])
                i += 1
            elements.append(('list', list_items))
            continue
        
        # Numbered list
        m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if m:
            list_items = [(m.group(1), m.group(2))]
            i += 1
            while i < len(lines):
                s = lines[i].strip()
                m2 = re.match(r'^(\d+)\.\s+(.+)$', s)
                if m2:
                    list_items.append((m2.group(1), m2.group(2)))
                    i += 1
                elif s and not s.startswith('═') and not s.startswith('┌') and not s.startswith('⸻'):
                    list_items[-1] = (list_items[-1][0], list_items[-1][1] + ' ' + s)
                    i += 1
                else:
                    break
            elements.append(('ordered_list', list_items))
            continue
            
        # Handle markdown tables simply for the appendix
        if stripped.startswith('|'):
            if '|---' in stripped:
                i += 1
                continue # Skip separator lines
            
            # Use split and handle empty leading/trailing cells
            cells_raw = stripped.split('|')
            # Remove the first and last empty cells if the line starts/ends with a pipe
            if len(cells_raw) > 0 and cells_raw[0].strip() == '':
                cells_raw = cells_raw[1:]
            if len(cells_raw) > 0 and cells_raw[-1].strip() == '':
                cells_raw = cells_raw[:-1]
                
            cells = [c.strip() for c in cells_raw]
            
            if len(cells) > 1:
                # If it's a header row
                if 'Greek' in cells[0] or 'Syriac' in cells[0] or 'Hebrew' in cells[0]:
                    elements.append(('table_start', cells))
                else:
                    elements.append(('table_row', cells))
                
                # Check if next line is not a table line to close the table
                if i + 1 >= len(lines) or not lines[i+1].strip().startswith('|'):
                    elements.append(('table_end', ''))
            i += 1
            continue

        # Check for QR code in the blockquote
        if '[QR code: marcus_rydberg@strike.me]' in stripped:
            elements.append(('qr_code', ''))
            i += 1
            continue
        if line.startswith('  ') and len(stripped) > 20:
            block_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                block_lines.append(lines[i].strip())
                i += 1
            elements.append(('blockquote', ' '.join(block_lines)))
            continue
        
        # Regular paragraph
        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('┌─') and not lines[i].strip().startswith('═') and not lines[i].strip() == '⸻':
            para_lines.append(lines[i].strip())
            i += 1
        elements.append(('paragraph', ' '.join(para_lines)))
    
    return elements

def sq(text):
    text = text.replace(' — ', ' &mdash; ')
    text = text.replace('— ', '&mdash; ')
    text = text.replace(' —', ' &mdash;')
    text = re.sub(r'(\d)–(\d)', r'\1&ndash;\2', text)
    text = text.replace('\u201c', '&ldquo;').replace('\u201d', '&rdquo;')
    text = text.replace('\u2018', '&lsquo;').replace('\u2019', '&rsquo;')
    return text

def render_box(box_text, box_class, label):
    box_text = sq(box_text.strip())
    # Split into paragraphs by blank lines or by distinct content blocks
    raw_lines = box_text.split('\n')
    paras = []
    current = []
    for line in raw_lines:
        if not line.strip():
            if current:
                paras.append(' '.join(current))
                current = []
        else:
            current.append(line.strip())
    if current:
        paras.append(' '.join(current))
    
    html = f'<div class="{box_class}">\n<span class="label">{label}</span>\n'
    for p in paras:
        if p:
            html += f'<p>{p}</p>\n'
    html += '</div>\n'
    return html

elements = classify_lines(lines)

html = []
html.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>On Calendar, Tradition, and Restraint</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --blue: #2c3e6b; --gold: #c4a35a; --burgundy: #7a2e3b;
  --bg: #fafaf7; --text: #2a2a2a;
  --light-blue-bg: #eef1f6; --light-gold-bg: #f8f4e8; --light-green-bg: #eef3ee;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; background: var(--bg); }}
body {{
  font-family: 'Crimson Text', Georgia, serif;
  font-size: 17px; line-height: 1.75; color: var(--text);
  background: var(--bg);
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}
main {{ max-width: 680px; margin: 0 auto; padding: 40px 24px 80px; }}
h1,h2,h3,h4 {{ font-family: 'Cormorant Garamond', Georgia, serif; color: var(--blue); line-height: 1.3; }}
h2.part-header {{
  font-size: 28px; font-weight: 700; margin: 60px 0 8px;
  text-align: center; text-transform: uppercase; letter-spacing: 2px;
  color: var(--blue); page-break-before: always;
}}
h2.part-subtitle {{
  font-size: 18px; font-weight: 400; font-style: italic;
  text-align: center; color: var(--burgundy); margin-bottom: 40px;
}}
h2.appendix-header {{
  font-size: 24px; font-weight: 700; margin: 60px 0 6px;
  text-align: center; text-transform: uppercase; letter-spacing: 2px;
  color: var(--blue); page-break-before: always;
}}
h2.appendix-subtitle {{
  font-size: 16px; font-weight: 400; font-style: italic;
  text-align: center; color: var(--burgundy); margin-bottom: 36px;
}}
h3 {{
  font-size: 22px; margin: 48px 0 16px; color: var(--blue);
  border-bottom: 1px solid rgba(196,163,90,0.3); padding-bottom: 8px;
}}
h4 {{ font-size: 18px; margin: 32px 0 12px; font-weight: 600; }}
h4.bold-header {{ font-size: 17px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 32px 0 12px; }}
p {{ margin: 0 0 16px; }}
blockquote {{
  margin: 24px 0; padding: 16px 24px;
  border-left: 3px solid var(--gold); background: var(--light-gold-bg); font-style: italic;
}}
.title-page {{
  text-align: center; padding: 60px 0 40px;
  border-bottom: 2px solid var(--gold); margin-bottom: 40px; page-break-after: always;
}}
.title-page h1 {{ font-size: 34px; margin-bottom: 8px; color: var(--blue); }}
.title-page .subtitle {{ font-size: 18px; font-style: italic; color: var(--burgundy); margin-bottom: 24px; }}
.title-page .author {{ font-size: 16px; color: #555; margin-bottom: 6px; }}
.title-page .svg-container {{ max-width: 280px; margin: 30px auto; }}
.title-page .svg-container svg {{ width: 100%; height: auto; }}
.epigraph {{
  max-width: 520px; margin: 40px auto; padding: 24px 32px;
  border-top: 1px solid var(--gold); border-bottom: 1px solid var(--gold);
  text-align: center; font-style: italic; font-size: 16px; line-height: 1.8; color: #555;
  page-break-after: always;
}}
.section-rule {{ text-align: center; margin: 36px 0; color: var(--gold); font-size: 14px; letter-spacing: 12px; }}
.reviewer-box {{
  margin: 24px 0; padding: 20px 24px;
  border-left: 4px solid #6b7fa0; background: var(--light-blue-bg);
  border-radius: 0 6px 6px 0;
  font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1.65;
  page-break-inside: avoid;
}}
.reviewer-box .label {{
  display: inline-block; background: var(--blue); color: white;
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 3px;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
}}
.western-box {{
  margin: 24px 0; padding: 20px 24px;
  border-left: 4px solid var(--gold); background: var(--light-gold-bg);
  border-radius: 0 6px 6px 0;
  font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1.65;
  page-break-inside: avoid;
}}
.western-box .label {{
  display: inline-block; background: var(--gold); color: white;
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 3px;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
}}
.gpt-box {{
  margin: 24px 0; padding: 20px 24px;
  border-left: 4px solid #5a7a5a; background: var(--light-green-bg);
  border-radius: 0 6px 6px 0;
  font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1.65;
  page-break-inside: avoid;
}}
.gpt-box .label {{
  display: inline-block; background: #5a7a5a; color: white;
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 3px;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
}}
.bib-meta {{ font-size: 14px; color: #777; font-family: 'Inter', sans-serif; margin: 4px 0 8px; padding-left: 12px; border-left: 2px solid #ddd; }}
.bib-label {{ font-weight: 600; font-size: 15px; margin: 12px 0 4px; color: var(--blue); }}
.personal-letter {{ border: 1px solid var(--gold); padding: 32px; border-radius: 8px; background: #fdfcf8; margin: 40px 0; }}
ol, ul {{ margin: 0 0 16px 24px; }}
li {{ margin-bottom: 8px; }}
nav.toc {{
  position: fixed; left: 0; top: 0; width: 220px; height: 100vh;
  overflow-y: auto; background: var(--blue); color: white;
  padding: 20px 16px; font-family: 'Inter', sans-serif; font-size: 12px; z-index: 100;
}}
nav.toc a {{ color: rgba(255,255,255,0.8); text-decoration: none; display: block; padding: 4px 0; line-height: 1.4; }}
nav.toc a:hover {{ color: var(--gold); }}
nav.toc .toc-title {{ font-size: 14px; font-weight: 600; color: var(--gold); margin-bottom: 12px; letter-spacing: 1px; text-transform: uppercase; }}
nav.toc .toc-section {{ margin: 10px 0 4px; font-weight: 600; color: rgba(255,255,255,0.95); font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }}
@media (max-width: 960px) {{ nav.toc {{ display: none; }} main {{ margin-left: 0; }} }}
@media (min-width: 961px) {{ main {{ margin-left: 240px; }} }}
@media print {{
  nav.toc {{ display: none !important; }}
  main {{ margin: 0 auto; max-width: 100%; padding: 20px; }}
  body {{ font-size: 11pt; }}
  h2.part-header, h2.appendix-header {{ page-break-before: always; }}
  .reviewer-box, .western-box, .gpt-box {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<nav class="toc">
<div class="toc-title">Contents</div>
<a href="#title">Title</a>
<div class="toc-section">Part I</div>
<a href="#s1">Introduction</a>
<a href="#s2">Easter as Germanic Word</a>
<a href="#s3">Easter from Ishtar?</a>
<a href="#s4">Rabbits and Eggs</a>
<a href="#s5">Biblical Calendar</a>
<a href="#s6">Bishop of Jerusalem</a>
<a href="#s7">Quartodeciman Controversy</a>
<a href="#s8">What Nicaea Decided</a>
<div class="toc-section">Part II</div>
<a href="#s9">Anti-Jewish Rhetoric</a>
<a href="#s10">Lineage &amp; Authority</a>
<div class="toc-section">Part III</div>
<a href="#s11">Providence</a>
<a href="#s12">Power Redirected</a>
<a href="#s13">Embodiment</a>
<a href="#s14">Constantine as Instrument</a>
<a href="#s15">Messy Conversion</a>
<a href="#s16">Judging by Fruit</a>
<a href="#s17">Restrained Reading</a>
<div class="toc-section">Appendices</div>
<a href="#app1">1. Rhetoric</a>
<a href="#app2">2. Scholars</a>
<a href="#app3">3. Assessment</a>
<a href="#app4">4. Rabbinic</a>
<a href="#app5">5. Orthodox</a>
<a href="#app6">6. Evangelical</a>
<div class="toc-section">&nbsp;</div>
<a href="#letter">Personal Note</a>
<div class="toc-section">&nbsp;</div>
<a href="#app7">7. Claude&rsquo;s Remarks</a>
<a href="#app8">8. GPT&rsquo;s Remarks</a>
<a href="#app9">9. Gemini&rsquo;s Remarks</a>
<a href="#app10">10. Glossary</a>
<a href="#app11">11. John 8:32</a>
</nav>
<main>
<div class="title-page" id="title">
<div class="svg-container">
{svg}
</div>
<h1>On Calendar, Tradition, and Restraint</h1>
<p class="subtitle">Collected for clarity, not controversy</p>
<p class="author">Compiled by brother Marcus R.,<br>a layperson and householder,<br>very broken and very blessed.</p>
<p style="margin: 20px 0; font-style: italic; color: var(--burgundy);">&ldquo;Blessed are the peacemakers.&rdquo;</p>
<p class="author">These notes are offered as context,<br>not correction.</p>
<p class="author" style="margin-top: 20px;">Houston, Texas<br>Lent 2026</p>
<div style="margin-top: 40px;">
  <a href="pascha-not-easter-booklet.pdf" style="display: inline-block; padding: 12px 24px; background: var(--blue); color: white; text-decoration: none; border-radius: 4px; font-weight: 600; font-family: 'Inter', sans-serif; letter-spacing: 1px; font-size: 14px;">DOWNLOAD PDF</a>
</div>
</div>
<div class="epigraph">
Tradition is not preserved by repetition alone,
but by faithful reception in every generation.
As Orthodox theologian Vladimir Lossky insisted,
the life of the Church is the life of the Spirit,
and fidelity requires discernment, humility,
and renewal. If this generation has a task,
it is not to invent new paths, but to clear
the old ones where they have become obscured.
</div>
''')

section_counter = 0
in_personal_letter = False

for etype, edata in elements:
    if etype == 'title_line':
        continue
    elif etype == 'main_title':
        html.append(f'<h2 class="part-header" id="intro">{sq(edata)}</h2>')
    elif etype == 'main_subtitle':
        html.append(f'<h2 class="part-subtitle">{sq(edata)}</h2>')
    elif etype == 'part_header':
        pn, sub = edata
        html.append(f'<h2 class="part-header" id="part{pn}">Part {pn}</h2>')
        html.append(f'<h2 class="part-subtitle">{sq(sub)}</h2>')
    elif etype == 'appendix_header':
        num, title = edata
        html.append(f'<h2 class="appendix-header" id="app{num}">Appendix {num}</h2>')
        html.append(f'<h2 class="appendix-subtitle">{sq(title)}</h2>')
    elif etype == 'personal_header':
        in_personal_letter = True
        html.append('<h2 class="part-header" id="letter">A Personal Note from the Author</h2>')
        html.append('<div class="personal-letter">')
    elif etype == 'h3':
        section_counter += 1
        html.append(f'<h3 id="s{section_counter}">{sq(edata)}</h3>')
    elif etype == 'h4':
        html.append(f'<h4>{sq(edata)}</h4>')
    elif etype == 'h4_bold':
        html.append(f'<h4 class="bold-header">{sq(edata)}</h4>')
    elif etype == 'divider':
        html.append('<div class="section-rule">&bull; &bull; &bull;</div>')
    elif etype == 'paragraph':
        html.append(f'<p>{sq(edata)}</p>')
    elif etype == 'blockquote':
        # Check for QR code in the blockquote
        if '[QR code: marcus_rydberg@strike.me]' in edata:
            html.append('<div style="text-align: center; margin: 30px 0;">')
            html.append('<img src="lightning-qr.png" alt="Lightning QR Code" style="max-width: 150px; border-radius: 8px; border: 1px solid var(--gold); padding: 10px; background: white;">')
            html.append('</div>')
            # Don't append the text version
            continue
            
        html.append(f'<blockquote>{sq(edata)}</blockquote>')
    elif etype == 'reviewer_box':
        html.append(render_box(edata, 'reviewer-box', 'AI REVIEW &mdash; CLAUDE OPUS 4.6'))
    elif etype == 'western_box':
        html.append(render_box(edata, 'western-box', 'WHY THIS MATTERS'))
    elif etype == 'gpt_box':
        html.append(render_box(edata, 'gpt-box', 'SECOND OPINION &mdash; GPT 5.2'))
    elif etype == 'list':
        html.append('<ul>')
        for item in edata:
            html.append(f'<li>{sq(item)}</li>')
        html.append('</ul>')
    elif etype == 'ordered_list':
        html.append('<ol>')
        for _, item in edata:
            html.append(f'<li>{sq(item)}</li>')
        html.append('</ol>')
    elif etype == 'table_start':
        html.append('<div style="overflow-x: auto; margin-bottom: 24px;">')
        html.append('<table style="width: 100%; border-collapse: collapse; font-family: \'Inter\', sans-serif; font-size: 14px; text-align: left;">')
        html.append('<tr style="background: var(--light-blue-bg); border-bottom: 2px solid var(--blue);">')
        for cell in edata:
            html.append(f'<th style="padding: 10px 14px; font-weight: 600; color: var(--blue);">{sq(cell)}</th>')
        html.append('</tr>')
    elif etype == 'table_row':
        html.append('<tr style="border-bottom: 1px solid #eee;">')
        for cell in edata:
            html.append(f'<td style="padding: 10px 14px;">{sq(cell)}</td>')
        html.append('</tr>')
    elif etype == 'table_end':
        html.append('</table>\n</div>')
    elif etype == 'qr_code':
        html.append('<div style="text-align: center; margin: 30px 0;">')
        html.append('<img src="lightning-qr.png" alt="Lightning QR Code" style="max-width: 150px; border-radius: 8px; border: 1px solid var(--gold); padding: 10px; background: white;">')
        html.append('</div>')
    elif etype == 'bib_meta':
        html.append(f'<p class="bib-meta">{sq(edata)}</p>')
    elif etype == 'bib_label':
        html.append(f'<p class="bib-label">{sq(edata)}</p>')

if in_personal_letter:
    html.append('</div>')

html.append('</main>\n</body>\n</html>')

out = '/home/marcus/code/new/writings/easter/docs/index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))
print(f"Written: {os.path.getsize(out)} bytes")
