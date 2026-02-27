import re, os

with open('/home/marcus/code/new/writings/easter/pascha-not-easter-booklet.txt', 'r') as f:
    raw = f.read()
with open('/home/marcus/code/new/writings/easter/cross-ornament-3.svg', 'r') as f:
    svg = f.read()

# Parse the document into structured sections
lines = raw.split('\n')

# Identify line types
def classify_lines(lines):
    """Walk through lines and classify them into structural elements"""
    elements = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            i += 1
            continue
        
        # ═══ separator lines
        if re.match(r'^═{10,}$', stripped):
            i += 1
            continue
        
        # ⸻ divider
        if stripped == '⸻':
            elements.append(('divider', ''))
            i += 1
            continue
        
        # Title page lines (centered with spaces)
        if i < 30 and line.startswith('         '):
            elements.append(('title_line', stripped))
            i += 1
            continue
        
        # PART headers
        m = re.match(r'^PART (I+)$', stripped)
        if m:
            i += 1
            # Next non-empty line is subtitle
            while i < len(lines) and not lines[i].strip():
                i += 1
            subtitle = lines[i].strip() if i < len(lines) else ''
            elements.append(('part_header', (m.group(1), subtitle)))
            i += 1
            continue
        
        # APPENDIX headers
        m = re.match(r'^APPENDIX (\d+)$', stripped)
        if m:
            num = m.group(1)
            i += 1
            # Next non-empty line(s) are the title
            while i < len(lines) and not lines[i].strip():
                i += 1
            title_lines = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^═{10,}$', lines[i].strip()):
                title_lines.append(lines[i].strip())
                i += 1
            title = ' '.join(title_lines)
            elements.append(('appendix_header', (num, title)))
            continue
        
        # Personal note header
        if stripped == 'A PERSONAL NOTE FROM THE AUTHOR':
            elements.append(('personal_header', ''))
            i += 1
            continue
        
        # PASCHA NOT EASTER header
        if stripped.startswith('PASCHA, NOT'):
            elements.append(('main_title', stripped))
            i += 1
            if i < len(lines) and lines[i].strip():
                elements.append(('main_subtitle', lines[i].strip()))
                i += 1
            continue
        
        # Reviewer boxes (┌─...─┐ to └─...─┘)
        if stripped.startswith('┌─'):
            box_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('└─'):
                raw_line = lines[i]
                # Remove box borders
                cleaned = re.sub(r'^\s*│\s?', '', raw_line)
                cleaned = re.sub(r'\s*│\s*$', '', cleaned)
                box_lines.append(cleaned)
                i += 1
            i += 1  # skip closing └─
            box_text = '\n'.join(box_lines)
            # Determine type
            if 'Why this matters' in box_text or 'A final word' in box_text or 'On Appendices 4, 5, and 6' in box_text or 'On the personal letter' in box_text:
                elements.append(('western_box', box_text))
            else:
                elements.append(('reviewer_box', box_text))
            continue
        
        # Section headers (short lines that are followed by blank lines and body text)
        # These are things like "Easter as a Germanic / English word vs Pascha"
        # Heuristic: non-empty line < 80 chars, next line is empty, not starting with common words
        if (len(stripped) < 100 and 
            not stripped.startswith('If ') and not stripped.startswith('The ') and
            not stripped.startswith('A ') and not stripped.startswith('This ') and
            not stripped.startswith('In ') and not stripped.startswith('It ') and
            not stripped.startswith('He ') and not stripped.startswith('That ') and
            not stripped.startswith('For ') and not stripped.startswith('One ') and
            not stripped.startswith('But ') and not stripped.startswith('And ') and
            not stripped.startswith('At ') and not stripped.startswith('My ') and
            not stripped.startswith('I ') and not stripped.startswith('We ') and
            not stripped.startswith('No ') and not stripped.startswith('So ') and
            not stripped.startswith('Seeing ') and not stripped.startswith('Over ') and
            not stripped.startswith('Scholars ') and not stripped.startswith('These ') and
            not stripped.startswith('Where ') and not stripped.startswith('Naming ') and
            not stripped.startswith('From ') and
            not stripped.startswith('INTRODUCTION') and
            not stripped.startswith('CONFIRMED') and not stripped.startswith('WHERE ') and
            not stripped.startswith('OVERALL') and
            i + 1 < len(lines) and not lines[i+1].strip()):
            
            # Check if previous element was a divider or header-ish
            is_header = False
            if elements and elements[-1][0] in ('divider', 'part_header', 'appendix_header', 'personal_header'):
                is_header = True
            # Also check if the line looks like a title (capitalized, or contains key phrases)
            if (is_header or
                stripped.startswith('"') or
                any(kw in stripped.lower() for kw in [
                    'easter', 'bishop', 'calendar', 'rhetoric', 'lineage', 'providence',
                    'power redirect', 'embodiment', 'constantine', 'messy conversion',
                    'judging by fruit', 'restrained', 'who am i', 'pagan religion',
                    'pagan culture', 'intra-christian', 'pastoral invective',
                    'schismatics', 'non-roman', 'ethnic stereotyping', 'imperial rhetoric',
                    'freedom of conscience', 'warning against', 'distinguishing gospel',
                    'unity without', 'spirit over', 'candid evangelical',
                    'preservation of life', 'these and those', 'warning against excessive',
                    'calendar authority', 'unity does not require uniformity',
                    'tradition is lived', 'excessive rigor', 'church applies',
                    'sacred time serves', 'torah was not given',
                ])):
                is_header = True
            
            if is_header:
                # Determine header level
                if any(kw in stripped.lower() for kw in [
                    'easter as a germanic', 'easter from', 'there is no real',
                    'bishop of jerusalem', 'anti-jewish', 'lineage, authority',
                    'providence, not', 'power redirected', 'why embodiment',
                    'constantine the great as', 'messy conversion', 'judging by fruit',
                    'restrained theological', 'who am i',
                    'introduction: what'
                ]):
                    elements.append(('h3', stripped))
                else:
                    elements.append(('h4', stripped))
                i += 1
                continue
        
        # Special: INTRODUCTION, CONFIRMED, WHERE, OVERALL headers
        if stripped.startswith('INTRODUCTION:'):
            elements.append(('h3', stripped))
            i += 1
            continue
        if stripped in ('CONFIRMED AS ACCURATE:', 'WHERE THE TEXT COULD BE STRONGER:', 'OVERALL ASSESSMENT:'):
            elements.append(('h4_bold', stripped))
            i += 1
            continue
        
        # Special: Scholar debate lists
        if stripped.startswith('Scholars do debate:') or stripped.startswith('Scholars do not seriously debate:'):
            elements.append(('h4_bold', stripped))
            i += 1
            continue
        
        # Bibliography-style entries with Status/Debate/Contribution/Relevance
        if re.match(r'^Status:\s', stripped) or re.match(r'^Debate level:\s', stripped):
            elements.append(('bib_meta', stripped))
            i += 1
            continue
        if re.match(r'^Contribution:', stripped) or re.match(r'^Relevance:', stripped):
            elements.append(('bib_label', stripped))
            i += 1
            continue
        
        # Indented list items (starting with -)
        if stripped.startswith('- ') or stripped.startswith('• '):
            list_items = [stripped[2:]]
            i += 1
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('• ')):
                list_items.append(lines[i].strip()[2:])
                i += 1
            elements.append(('list', list_items))
            continue
        
        # Numbered list items
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
                elif s and not s.startswith('═') and not s.startswith('┌'):
                    # continuation of previous item
                    list_items[-1] = (list_items[-1][0], list_items[-1][1] + ' ' + s)
                    i += 1
                else:
                    break
            elements.append(('ordered_list', list_items))
            continue
        
        # Indented block (citation block)
        if line.startswith('  ') and len(stripped) > 20:
            block_lines = [stripped]
            i += 1
            while i < len(lines) and (lines[i].startswith('  ') and lines[i].strip()):
                block_lines.append(lines[i].strip())
                i += 1
            block_text = ' '.join(block_lines)
            elements.append(('blockquote', block_text))
            continue
        
        # Regular paragraph
        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('┌─') and not lines[i].strip().startswith('═'):
            para_lines.append(lines[i].strip())
            i += 1
        elements.append(('paragraph', ' '.join(para_lines)))
    
    return elements

def smart_quotes(text):
    """Convert text to use HTML entities for smart typography"""
    # Em dashes
    text = text.replace(' — ', ' &mdash; ')
    text = text.replace('— ', '&mdash; ')
    text = text.replace(' —', ' &mdash;')
    # En dashes for ranges
    text = re.sub(r'(\d)–(\d)', r'\1&ndash;\2', text)
    # Curly quotes - handle unicode ones
    text = text.replace('\u201c', '&ldquo;')  # "
    text = text.replace('\u201d', '&rdquo;')  # "
    text = text.replace('\u2018', '&lsquo;')  # '
    text = text.replace('\u2019', '&rsquo;')  # '
    # Handle straight quotes approximately
    # Don't touch since most are already unicode
    return text

def render_box(box_text, box_class, label):
    """Render a reviewer box"""
    box_text = smart_quotes(box_text.strip())
    paras = re.split(r'\n\s*\n', box_text)
    if len(paras) <= 1:
        paras = [p.strip() for p in box_text.split('\n') if p.strip()]
        # Merge consecutive lines into paragraphs (separated by empty-ish content)
        merged = []
        current = []
        for p in paras:
            if not p:
                if current:
                    merged.append(' '.join(current))
                    current = []
            else:
                current.append(p)
        if current:
            merged.append(' '.join(current))
        paras = merged if merged else paras
    
    html = f'<div class="{box_class}">\n<span class="label">{label}</span>\n'
    for p in paras:
        p = p.strip()
        if p:
            p = p.replace('\n', ' ')
            html += f'<p>{p}</p>\n'
    html += '</div>\n'
    return html

# Parse
elements = classify_lines(lines)

# Build HTML
html = []

# Head
html.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>On Calendar, Tradition, and Restraint</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --blue: #2c3e6b;
  --gold: #c4a35a;
  --burgundy: #7a2e3b;
  --bg: #fafaf7;
  --text: #2a2a2a;
  --light-blue-bg: #eef1f6;
  --light-gold-bg: #f8f4e8;
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
h1, h2, h3, h4 {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  color: var(--blue); line-height: 1.3;
}}
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
  border-left: 3px solid var(--gold); background: var(--light-gold-bg);
  font-style: italic;
}}
.title-page {{
  text-align: center; padding: 60px 0 40px;
  border-bottom: 2px solid var(--gold); margin-bottom: 40px;
  page-break-after: always;
}}
.title-page h1 {{ font-size: 34px; margin-bottom: 8px; color: var(--blue); }}
.title-page .subtitle {{
  font-size: 18px; font-style: italic; color: var(--burgundy); margin-bottom: 24px;
}}
.title-page .author {{ font-size: 16px; color: #555; margin-bottom: 6px; }}
.title-page .svg-container {{ max-width: 280px; margin: 30px auto; }}
.title-page .svg-container svg {{ width: 100%; height: auto; }}
.epigraph {{
  max-width: 520px; margin: 40px auto; padding: 24px 32px;
  border-top: 1px solid var(--gold); border-bottom: 1px solid var(--gold);
  text-align: center; font-style: italic; font-size: 16px;
  line-height: 1.8; color: #555; page-break-after: always;
}}
.section-rule {{
  text-align: center; margin: 36px 0; color: var(--gold);
  font-size: 14px; letter-spacing: 12px;
}}
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
.bib-meta {{
  font-size: 14px; color: #777; font-family: 'Inter', sans-serif;
  margin: 4px 0 8px; padding-left: 12px; border-left: 2px solid #ddd;
}}
.bib-label {{ font-weight: 600; font-size: 15px; margin: 12px 0 4px; color: var(--blue); }}
.personal-letter {{
  border: 1px solid var(--gold); padding: 32px; border-radius: 8px;
  background: #fdfcf8; margin: 40px 0;
}}
ol, ul {{ margin: 0 0 16px 24px; }}
li {{ margin-bottom: 8px; }}
nav.toc {{
  position: fixed; left: 0; top: 0; width: 220px; height: 100vh;
  overflow-y: auto; background: var(--blue); color: white;
  padding: 20px 16px; font-family: 'Inter', sans-serif; font-size: 12px; z-index: 100;
}}
nav.toc a {{
  color: rgba(255,255,255,0.8); text-decoration: none;
  display: block; padding: 4px 0; line-height: 1.4;
}}
nav.toc a:hover {{ color: var(--gold); }}
nav.toc .toc-title {{
  font-size: 14px; font-weight: 600; color: var(--gold);
  margin-bottom: 12px; letter-spacing: 1px; text-transform: uppercase;
}}
nav.toc .toc-section {{
  margin: 10px 0 4px; font-weight: 600; color: rgba(255,255,255,0.95);
  font-size: 11px; text-transform: uppercase; letter-spacing: 1px;
}}
@media (max-width: 960px) {{ nav.toc {{ display: none; }} main {{ margin-left: 0; }} }}
@media (min-width: 961px) {{ main {{ margin-left: 240px; }} }}
@media print {{
  nav.toc {{ display: none !important; }}
  main {{ margin: 0 auto; max-width: 100%; padding: 20px; }}
  body {{ font-size: 11pt; }}
  h2.part-header, h2.appendix-header {{ page-break-before: always; }}
  .reviewer-box, .western-box {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<nav class="toc">
<div class="toc-title">Contents</div>
<a href="#title">Title</a>
<div class="toc-section">Part I</div>
<a href="#s1">Easter as Germanic Word</a>
<a href="#s2">Easter from Ishtar?</a>
<a href="#s3">Biblical Calendar</a>
<a href="#s4">Bishop of Jerusalem</a>
<div class="toc-section">Part II</div>
<a href="#s5">Anti-Jewish Rhetoric</a>
<a href="#s6">Lineage &amp; Authority</a>
<div class="toc-section">Part III</div>
<a href="#s7">Providence</a>
<a href="#s8">Power Redirected</a>
<a href="#s9">Embodiment</a>
<a href="#s10">Constantine as Instrument</a>
<a href="#s11">Messy Conversion</a>
<a href="#s12">Judging by Fruit</a>
<a href="#s13">Restrained Reading</a>
<div class="toc-section">Appendices</div>
<a href="#app1">1. Rhetoric</a>
<a href="#app2">2. Scholars</a>
<a href="#app3">3. Assessment</a>
<a href="#app4">4. Rabbinic</a>
<a href="#app5">5. Orthodox</a>
<a href="#app6">6. Evangelical</a>
<div class="toc-section">&nbsp;</div>
<a href="#letter">Personal Note</a>
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
<p class="author" style="margin-top: 20px;">Houston, Texas<br>Winter 2026</p>
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

# Now render each element
section_counter = 0
in_personal_letter = False

for etype, edata in elements:
    # Skip title-page elements (already rendered)
    if etype == 'title_line':
        continue
    
    if etype == 'main_title':
        html.append(f'<h2 class="part-header" id="intro">{smart_quotes(edata)}</h2>')
    elif etype == 'main_subtitle':
        html.append(f'<h2 class="part-subtitle">{smart_quotes(edata)}</h2>')
    elif etype == 'part_header':
        part_num, subtitle = edata
        html.append(f'<h2 class="part-header" id="part{part_num}">Part {part_num}</h2>')
        html.append(f'<h2 class="part-subtitle">{smart_quotes(subtitle)}</h2>')
    elif etype == 'appendix_header':
        num, title = edata
        html.append(f'<h2 class="appendix-header" id="app{num}">Appendix {num}</h2>')
        html.append(f'<h2 class="appendix-subtitle">{smart_quotes(title)}</h2>')
    elif etype == 'personal_header':
        in_personal_letter = True
        html.append(f'<h2 class="part-header" id="letter">A Personal Note from the Author</h2>')
        html.append('<div class="personal-letter">')
    elif etype == 'h3':
        section_counter += 1
        html.append(f'<h3 id="s{section_counter}">{smart_quotes(edata)}</h3>')
    elif etype == 'h4':
        html.append(f'<h4>{smart_quotes(edata)}</h4>')
    elif etype == 'h4_bold':
        html.append(f'<h4 class="bold-header">{smart_quotes(edata)}</h4>')
    elif etype == 'divider':
        html.append('<div class="section-rule">&bull; &bull; &bull;</div>')
    elif etype == 'paragraph':
        text = smart_quotes(edata)
        # Check for "If you want secondary scholarship" or similar list intros
        html.append(f'<p>{text}</p>')
    elif etype == 'blockquote':
        html.append(f'<blockquote>{smart_quotes(edata)}</blockquote>')
    elif etype == 'reviewer_box':
        html.append(render_box(edata, 'reviewer-box', 'AI REVIEW'))
    elif etype == 'western_box':
        html.append(render_box(edata, 'western-box', 'WHY THIS MATTERS'))
    elif etype == 'list':
        html.append('<ul>')
        for item in edata:
            html.append(f'<li>{smart_quotes(item)}</li>')
        html.append('</ul>')
    elif etype == 'ordered_list':
        html.append('<ol>')
        for num, item in edata:
            html.append(f'<li>{smart_quotes(item)}</li>')
        html.append('</ol>')
    elif etype == 'bib_meta':
        html.append(f'<p class="bib-meta">{smart_quotes(edata)}</p>')
    elif etype == 'bib_label':
        html.append(f'<p class="bib-label">{smart_quotes(edata)}</p>')

# Close personal letter div if open
if in_personal_letter:
    html.append('</div>')

html.append('</main>\n</body>\n</html>')

full_html = '\n'.join(html)

out_path = '/home/marcus/code/new/writings/easter/pascha-not-easter-modern.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Modern HTML written: {os.path.getsize(out_path)} bytes")
