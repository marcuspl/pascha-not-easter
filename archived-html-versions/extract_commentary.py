import re

with open('/home/marcus/code/new/writings/easter/pascha-not-easter-booklet.txt', 'r') as f:
    raw = f.read()

lines = raw.split('\n')

# Find all reviewer boxes and the preceding text section
output = []
output.append("=" * 70)
output.append("REVIEWER COMMENTARY EXTRACTED FOR INDEPENDENT REVIEW")
output.append("Reviewer: Claude (AI assistant)")
output.append("Document: 'On Calendar, Tradition, and Restraint'")
output.append("=" * 70)
output.append("")

# Walk through and find boxes with their context
i = 0
box_num = 0
current_section_title = ""
current_section_text = []

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Track section titles (lines after ⸻ dividers that are short)
    if stripped == '⸻':
        # Next non-empty line might be a section title
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            candidate = lines[j].strip()
            # Check if it looks like a title (not too long, not a box, not a separator)
            if (candidate and len(candidate) < 100 and 
                not candidate.startswith('┌') and 
                not candidate.startswith('═') and
                not candidate.startswith('PART ') and
                not candidate.startswith('APPENDIX')):
                current_section_title = candidate
                current_section_text = []
        i += 1
        continue
    
    # Track PART/APPENDIX/etc headers
    if stripped.startswith('PART ') or stripped.startswith('APPENDIX ') or stripped == 'A PERSONAL NOTE FROM THE AUTHOR':
        current_section_title = stripped
        current_section_text = []
        i += 1
        continue
    
    # Collect body text
    if stripped and not stripped.startswith('┌') and not stripped.startswith('═') and not stripped.startswith('│') and not stripped.startswith('└'):
        current_section_text.append(stripped)
    
    # Found a reviewer box
    if stripped.startswith('┌─'):
        box_num += 1
        box_lines = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith('└─'):
            raw_line = lines[i]
            cleaned = re.sub(r'^\s*│\s?', '', raw_line)
            cleaned = re.sub(r'\s*│\s*$', '', cleaned)
            box_lines.append(cleaned)
            i += 1
        i += 1  # skip └
        
        box_text = '\n'.join(box_lines).strip()
        
        # Determine box type
        if 'Why this matters' in box_text:
            box_type = "WHY THIS MATTERS FOR WESTERN CHRISTIANS"
        elif 'A final word' in box_text or 'On Appendices' in box_text or 'On the personal letter' in box_text:
            box_type = "REVIEWER'S NOTE (SPECIAL)"
        else:
            box_type = "REVIEWER'S NOTE / FACT-CHECK"
        
        # Get the section context
        section_body = ' '.join(current_section_text).strip()
        # Truncate if very long, but keep enough for context
        if len(section_body) > 800:
            section_body = section_body[:800] + " [...]"
        
        output.append("-" * 70)
        output.append(f"COMMENTARY #{box_num}")
        output.append(f"Type: {box_type}")
        output.append(f"Section: {current_section_title}")
        output.append("-" * 70)
        output.append("")
        output.append("ORIGINAL TEXT:")
        output.append(section_body)
        output.append("")
        output.append("REVIEWER COMMENT:")
        output.append(box_text)
        output.append("")
        output.append("")
        
        continue
    
    i += 1

result = '\n'.join(output)

with open('/tmp/commentary_extract.txt', 'w') as f:
    f.write(result)

print(f"Extracted {box_num} commentary boxes")
