import re, os

# Read raw source text
with open('/home/marcus/code/new/writings/easter/pascha-not-easter-booklet.txt', 'r') as f:
    raw = f.read()

# Read SVG
with open('/home/marcus/code/new/writings/easter/cross-ornament-3.svg', 'r') as f:
    svg = f.read()

# Build the HTML
html_parts = []

# --- CSS and HTML head ---
html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>On Calendar, Tradition, and Restraint</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --blue: #2c3e6b;
  --gold: #c4a35a;
  --burgundy: #7a2e3b;
  --bg: #fafaf7;
  --text: #2a2a2a;
  --light-blue-bg: #eef1f6;
  --light-gold-bg: #f8f4e8;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Crimson Text', Georgia, serif;
  font-size: 17px;
  line-height: 1.75;
  color: var(--text);
  background: var(--bg);
}
main {
  max-width: 680px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}
h1, h2, h3, h4 {
  font-family: 'Cormorant Garamond', 'Georgia', serif;
  color: var(--blue);
  line-height: 1.3;
}
h2.part-header {
  font-size: 28px;
  font-weight: 700;
  margin: 60px 0 8px;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--blue);
}
h2.part-subtitle {
  font-size: 18px;
  font-weight: 400;
  font-style: italic;
  text-align: center;
  color: var(--burgundy);
  margin-bottom: 40px;
}
h3 {
  font-size: 22px;
  margin: 48px 0 16px;
  color: var(--blue);
}
h4 {
  font-size: 18px;
  margin: 32px 0 12px;
  font-weight: 600;
}
p { margin: 0 0 16px; }
blockquote {
  margin: 24px 0;
  padding: 16px 24px;
  border-left: 3px solid var(--gold);
  background: var(--light-gold-bg);
  font-style: italic;
}
.title-page {
  text-align: center;
  padding: 60px 0 40px;
  border-bottom: 2px solid var(--gold);
  margin-bottom: 40px;
}
.title-page h1 {
  font-size: 34px;
  margin-bottom: 8px;
  color: var(--blue);
}
.title-page .subtitle {
  font-size: 18px;
  font-style: italic;
  color: var(--burgundy);
  margin-bottom: 24px;
}
.title-page .author {
  font-size: 16px;
  color: #555;
  margin-bottom: 6px;
}
.title-page .svg-container {
  max-width: 280px;
  margin: 30px auto;
}
.title-page .svg-container svg {
  width: 100%;
  height: auto;
}
.epigraph {
  max-width: 520px;
  margin: 40px auto;
  padding: 24px 32px;
  border-top: 1px solid var(--gold);
  border-bottom: 1px solid var(--gold);
  text-align: center;
  font-style: italic;
  font-size: 16px;
  line-height: 1.8;
  color: #555;
}
.section-rule {
  text-align: center;
  margin: 40px 0;
  color: var(--gold);
  font-size: 20px;
  letter-spacing: 8px;
}
.reviewer-box {
  margin: 24px 0;
  padding: 20px 24px;
  border-left: 4px solid #6b7fa0;
  background: var(--light-blue-bg);
  border-radius: 0 6px 6px 0;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  line-height: 1.65;
}
.reviewer-box .label {
  display: inline-block;
  background: var(--blue);
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}
.western-box {
  margin: 24px 0;
  padding: 20px 24px;
  border-left: 4px solid var(--gold);
  background: var(--light-gold-bg);
  border-radius: 0 6px 6px 0;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  line-height: 1.65;
}
.western-box .label {
  display: inline-block;
  background: var(--gold);
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}
.bib-entry {
  margin: 20px 0;
  padding-left: 16px;
}
.bib-entry .title { font-weight: 600; }
.bib-entry .meta { font-size: 14px; color: #666; }
.personal-letter {
  border: 1px solid var(--gold);
  padding: 32px;
  border-radius: 8px;
  background: #fdfcf8;
  margin: 40px 0;
}
ol, ul { margin: 0 0 16px 24px; }
li { margin-bottom: 6px; }
nav.toc {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
  overflow-y: auto;
  background: var(--blue);
  color: white;
  padding: 20px 16px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  z-index: 100;
}
nav.toc a {
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  display: block;
  padding: 4px 0;
  line-height: 1.4;
}
nav.toc a:hover { color: var(--gold); }
nav.toc .toc-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--gold);
  margin-bottom: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
}
nav.toc .toc-section {
  margin: 10px 0 4px;
  font-weight: 600;
  color: rgba(255,255,255,0.95);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
@media (max-width: 960px) {
  nav.toc { display: none; }
  main { margin-left: 0; }
}
@media (min-width: 961px) {
  main { margin-left: 240px; }
}
@media print {
  nav.toc { display: none !important; }
  main { margin: 0 auto; max-width: 100%; padding: 20px; }
  .title-page { page-break-after: always; }
  .epigraph { page-break-after: always; }
  h2.part-header { page-break-before: always; }
  .reviewer-box, .western-box { page-break-inside: avoid; }
  body { font-size: 11pt; }
}
</style>
</head>
<body>
''')

# --- TOC sidebar ---
html_parts.append('''<nav class="toc">
<div class="toc-title">Contents</div>
<a href="#title">Title</a>
<div class="toc-section">Part I</div>
<a href="#s-easter-word">Easter as Germanic Word</a>
<a href="#s-ishtar">Easter from Ishtar?</a>
<a href="#s-calendar">Biblical Calendar</a>
<a href="#s-bishop">Bishop of Jerusalem</a>
<div class="toc-section">Part II</div>
<a href="#s-rhetoric">Anti-Jewish Rhetoric</a>
<a href="#s-lineage">Lineage &amp; Authority</a>
<div class="toc-section">Part III</div>
<a href="#s-providence">Providence</a>
<a href="#s-power">Power Redirected</a>
<a href="#s-embodiment">Embodiment</a>
<a href="#s-constantine">Constantine as Instrument</a>
<a href="#s-messy">Messy Conversion</a>
<a href="#s-fruit">Judging by Fruit</a>
<a href="#s-restrained">Restrained Reading</a>
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
''')

# Now parse the raw text and convert to HTML sections
# We'll do this by splitting on the major markers

lines = raw.split('\n')

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def process_text_block(text):
    """Convert plain text to HTML paragraphs, handling special chars"""
    text = text.strip()
    if not text:
        return ''
    # Handle em dashes
    text = text.replace(' — ', ' &mdash; ')
    text = text.replace('— ', '&mdash; ')
    text = text.replace(' —', ' &mdash;')
    # Handle quotes
    text = text.replace('"', '&ldquo;').replace('"', '&rdquo;')
    text = text.replace(''', '&rsquo;').replace(''', '&lsquo;')
    # Split into paragraphs by double newlines
    paras = re.split(r'\n\s*\n', text)
    result = []
    for p in paras:
        p = p.strip()
        if p:
            # Keep line breaks within paragraphs
            p = p.replace('\n', ' ')
            result.append(f'<p>{p}</p>')
    return '\n'.join(result)

# We'll build the HTML by walking through the source and identifying sections
# This is a large task - let's parse the structure

# Find major sections
content = raw

# Title page
html_parts.append(f'''<main>
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
''')

# Epigraph
html_parts.append('''<div class="epigraph">
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

# Now extract the actual body content between the structural markers
# We need to find content sections and reviewer boxes

# Helper: extract reviewer boxes from text
def find_and_render_boxes(text):
    """Find reviewer note boxes and render them as HTML"""
    result = text
    # Pattern for reviewer boxes with the box-drawing chars
    box_pattern = r'┌─+┐\s*\n(.*?)└─+┘'
    matches = list(re.finditer(box_pattern, result, re.DOTALL))
    for m in reversed(matches):
        box_content = m.group(1)
        # Clean up the box borders
        box_lines = box_content.split('\n')
        clean_lines = []
        for line in box_lines:
            line = re.sub(r'^\s*│\s?', '', line)
            line = re.sub(r'\s*│\s*$', '', line)
            clean_lines.append(line.strip())
        box_text = '\n'.join(clean_lines).strip()
        
        # Determine box type
        if 'Why this matters' in box_text or 'A final word' in box_text or 'On Appendices 4, 5, and 6' in box_text:
            box_class = 'western-box'
            label = 'WHY THIS MATTERS'
        else:
            box_class = 'reviewer-box'
            label = 'AI REVIEW'
        
        # Process the text
        box_text = box_text.replace(' — ', ' &mdash; ')
        box_text = box_text.replace('— ', '&mdash; ')
        box_text = box_text.replace(' —', ' &mdash;')
        box_text = box_text.replace('"', '&ldquo;').replace('"', '&rdquo;')
        box_text = box_text.replace(''', '&rsquo;').replace(''', '&lsquo;')
        
        # Split into paragraphs
        paras = re.split(r'\n\s*\n', box_text)
        box_html = f'<div class="{box_class}">\n<span class="label">{label}</span>\n'
        for p in paras:
            p = p.strip()
            if p:
                p = p.replace('\n', ' ')
                box_html += f'<p>{p}</p>\n'
        box_html += '</div>\n'
        
        result = result[:m.start()] + box_html + result[m.end():]
    
    return result

# Extract sections between structural markers
# Split on the ═══ lines and ⸻ lines

# Let's process the content after the epigraph
# Find "PASCHA, NOT" 
intro_start = content.find('PASCHA, NOT')
if intro_start == -1:
    intro_start = 0

# Everything from PASCHA onwards
body = content[intro_start:]

# Replace structural markers with HTML
# First, handle the PART headers
body = re.sub(
    r'═+\s*\n\s*PART I\s*\n\s*THE SPECIFIC CLAIMS, EXAMINED\s*\n═+',
    '<h2 class="part-header" id="part1">Part I</h2>\n<h2 class="part-subtitle">The Specific Claims, Examined</h2>',
    body
)
body = re.sub(
    r'═+\s*\n\s*PART II\s*\n\s*THE HISTORICAL CONTEXT\s*\n═+',
    '<h2 class="part-header" id="part2">Part II</h2>\n<h2 class="part-subtitle">The Historical Context</h2>',
    body
)
body = re.sub(
    r'═+\s*\n\s*PART III\s*\n\s*THE LARGER FRAME: WHY IT MATTERS\s*\n═+',
    '<h2 class="part-header" id="part3">Part III</h2>\n<h2 class="part-subtitle">The Larger Frame: Why It Matters</h2>',
    body
)

# Appendix headers
for i in range(1, 7):
    body = re.sub(
        rf'═+\s*\n\s*APPENDIX {i}\s*\n(.*?)\n═+',
        lambda m, num=i: f'<h2 class="part-header" id="app{num}">Appendix {num}</h2>\n<h2 class="part-subtitle">{m.group(1).strip()}</h2>',
        body
    )

# Personal note header
body = re.sub(
    r'═+\s*\n\s*A PERSONAL NOTE FROM THE AUTHOR\s*\n═+',
    '<h2 class="part-header" id="letter">A Personal Note from the Author</h2>',
    body
)

# Handle section dividers (⸻)
body = body.replace('⸻', '<div class="section-rule">&bull; &bull; &bull;</div>')

# Handle introduction
body = body.replace(
    'PASCHA, NOT "EASTER"\nConstantine, Nicaea, and the Claims That Don\'t Hold Up',
    '<h2 class="part-header" id="intro">Pascha, Not &ldquo;Easter&rdquo;</h2>\n<h2 class="part-subtitle">Constantine, Nicaea, and the Claims That Don&rsquo;t Hold Up</h2>'
)

# Section headings - find lines that are section titles
section_ids = {
    'INTRODUCTION: What is actually being claimed?': ('intro-what', 's-intro'),
    'Easter as a Germanic / English word vs Pascha': ('s-easter-word', 's-easter-word'),
    '"Easter" from Asherah / Ishtar does not hold up': ('s-ishtar', 's-ishtar'),
    'There is no real "back to" the biblical calendar': ('s-calendar', 's-calendar'),
    'The Bishop of Jerusalem was not excluded from Nicaea': ('s-bishop', 's-bishop'),
    'Why "anti-Jewish" rhetoric reads differently to us than it did then': ('s-rhetoric', 's-rhetoric'),
    'Lineage, authority, and the men who shaped Nicaea': ('s-lineage', 's-lineage'),
    'Providence, not coincidence': ('s-providence', 's-providence'),
    'Power redirected, not sanctified': ('s-power', 's-power'),
    'Why embodiment mattered for survival': ('s-embodiment', 's-embodiment'),
    'Constantine the Great as instrument, not ideal': ('s-constantine', 's-constantine'),
    'Messy conversion is exactly what history predicts': ('s-messy', 's-messy'),
    'Judging by fruit, not fantasy': ('s-fruit', 's-fruit'),
    'A restrained theological reading': ('s-restrained', 's-restrained'),
    'Who am I to care about these things?': ('s-who', 's-who'),
}

for title, (id_val, _) in section_ids.items():
    escaped = re.escape(title)
    body = re.sub(
        rf'\n{escaped}\s*\n',
        f'\n<h3 id="{id_val}">{title}</h3>\n',
        body
    )

# Appendix subsection headings
app_subsections = [
    'Pagan religion', 'Pagan culture ridiculed', 'Intra-Christian polemic',
    'Pastoral invective', 'Schismatics and coercion', 'Non-Roman peoples',
    'Ethnic stereotyping', 'Imperial rhetoric', 'Representative Rabbinic',
    'Representative Orthodox', 'Representative evangelical',
    'Freedom of conscience', 'Warning against returning', 'Distinguishing gospel',
    'Unity without enforced', 'The Spirit over technique',
    'A candid evangelical limitation',
]

# Now handle the reviewer boxes
body = find_and_render_boxes(body)

# Handle the indented block quote in the introduction
body = re.sub(
    r'  Constantine the Great, driven by antisemitism.*?reclaim it\.',
    lambda m: '<blockquote>' + m.group(0).strip() + '</blockquote>',
    body,
    flags=re.DOTALL
)

# Convert remaining plain text blocks to paragraphs
# Split on double newlines, wrap in <p> tags
sections = body.split('\n\n')
final_parts = []
for section in sections:
    s = section.strip()
    if not s:
        continue
    # Skip if already HTML
    if s.startswith('<'):
        final_parts.append(s)
        continue
    # Check if it's a list-like block (starts with spaces indicating indentation)
    if s.startswith('  ') and not s.startswith('   '):
        # Could be an indented block
        lines_s = s.split('\n')
        items = [l.strip() for l in lines_s if l.strip()]
        if len(items) > 1 and all(l.strip().startswith('-') or l.strip().startswith('•') for l in items):
            final_parts.append('<ul>')
            for item in items:
                item = re.sub(r'^[-•]\s*', '', item)
                final_parts.append(f'<li>{item}</li>')
            final_parts.append('</ul>')
            continue
    # Otherwise wrap in <p>
    s = s.replace('\n', ' ')
    # Handle em dashes
    s = s.replace(' — ', ' &mdash; ')
    s = s.replace('— ', '&mdash; ')
    s = s.replace(' —', ' &mdash;')
    final_parts.append(f'<p>{s}</p>')

body = '\n'.join(final_parts)

html_parts.append(body)
html_parts.append('\n</main>\n</body>\n</html>')

full_html = '\n'.join(html_parts)

# Write the file
out_path = '/home/marcus/code/new/writings/easter/pascha-not-easter-modern.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"HTML written: {os.path.getsize(out_path)} bytes")
