
import os

file_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_vectors = False
slide_open = False
first_card_seen = False

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # 1. Detect start of Vectors Section
    if 'id="vectors-section"' in line:
        in_vectors = True
    
    # 2. Detect end of Vectors Section (approximate, relying on Timeline start or specific marker)
    if in_vectors and ('id="timeline-section"' in line or 'class="timeline-section-wrapper"' in line):
        in_vectors = False
        # If a slide was open, close it before section ends?
        # Note: The section currently ends with controls and script, so strictly speaking matching 'section' end is handled below.

    # 3. Handle Vector Cards
    if in_vectors and '<div class="vector-card' in line:
        # Check if this card is ALREADY wrapped by a slide (look at immediate previous meaningful line)
        # We need to look back in 'new_lines'
        
        # Simple heuristic: If the previous line added was '<div class="vector-slide">', it's wrapped.
        prev_line = new_lines[-1].strip() if new_lines else ""
        
        if 'vector-slide' in prev_line:
            # Already wrapped (like VEC-001, VEC-002, VEC-003 might be)
            # Just append the line
            new_lines.append(line)
            slide_open = True # A slide is active
        else:
            # NOT wrapped. This is a loose card (VEC-007, etc) or one I missed.
            # We need to:
            # a) Close the previous slide? 
            #    If VEC-006 ended, it might not have closed the slide div if I didn't add it.
            #    Actually, in my manual edit I added "</div></div>" BEFORE the new slide.
            #    So if I see a loose card, it implies the previous block just ended with "</div>".
            
            # Strategy: Always inject closing/opening transition for loose cards.
            # But wait, VEC-001 is definitely wrapped.
            # VEC-007 is loose.
            
            # I will inject:
            # </div> <!-- Close previous card container? No, previous card closed itself -->
            # </div> <!-- Close previous slide -->
            # <div class="vector-slide"> <!-- Open new slide -->
            
            # BUT: I need to be careful not to close the Container/Track prematurely.
            # The structure I want is:
            # <div class="vector-slide"> <div class="card"> ... </div> </div>
            
            # If I encounter a loose card:
            # It means the previous content was just a card closing.
            # So I should Append: </div> (close previous slide) + <div class="vector-slide">
            
            # EXCEPT for the very first one?
            # VEC-001 is at the top. It IS wrapped.
            # VEC-002 was wrapped by my replace.
            
            # So this logic applies to VEC-007+.
            # I will insert the wrapper.
            
            new_lines.append('        </div> <!-- Close Previous Slide (Injected) -->\n') 
            new_lines.append('        <div class="vector-slide">\n')
            new_lines.append(line)
            slide_open = True

    # 4. Handle Closing of a Card?
    # It's hard to track DOM depth line-by-line.
    # Instead, I will assume the structure is:
    # <div class="vector-slide">
    #    <div class="vector-card"> ... </div>
    # </div>
    
    # If I just inject the "Open Slide" before the card, I need to make sure I "Close Slide" after the card.
    # OR, I leave the "Close Slide" to be inserted *before* the NEXT card.
    # This works for the chain (Link 1-2, Link 2-3...).
    # But what about the LAST card (VEC-016)?
    # It needs a closing div.
    
    else:
        new_lines.append(line)

# Post-processing:
# The loop strategy above inserts "Close Previous / Open New" BEFORE every loose card.
# This fixes the separation.
# But it adds a stray "</div>" before VEC-007 (closing VEC-006's slide, which presumably wasn't open? OR was it?).
# If VEC-006 *wasn't* wrapped in a slide, then adding "</div>" closes... the Track?
# That would be bad. the Track must stay open.

# This is risky.
# Let's fix specific lines based on the content I saw.
# I saw VEC-007 is loose.
# I will use a simple string replace on the FULL CONTENT.

content = "".join(lines)

# Fix VEC-007
# It is preceded by a closing div of VEC-006.
# I'll look for the VEC-007 signature.
# "VEC-007" is unique.
# I will find the block around it.

# Logic: replace '<div class="vector-card critical">\n\s*<div class="vector-header">\n\s*<div class="vector-id">VEC-(\d+)</div>'
# with '</div></div><div class="vector-slide"><div class="vector-card critical">...'
# But I have to be careful with regex.

import re

def replacer(match):
    # match.group(0) is the whole card start
    # We wrap it.
    original = match.group(0)
    # Check if we are VEC-001 (don't wrap)
    if "VEC-001" in original:
        return original
    
    # Check if VEC-002, 003 (already wrapped by my edit)
    # My edit added "</div></div><div class='vector-slide'>" before them.
    # So if I wrap again, I get double slides.
    
    # Simple check: Does the file ALREADY contain the wrapper before this specific ID?
    # I can't check context easily in regex replacer function.
    
    # Let's target strictly VEC-007 to VEC-016
    vec_id = match.group(2) # "007"
    if int(vec_id) >= 7 and int(vec_id) <= 16:
        # These are the broken ones.
        # But wait, what about the Class? "critical" vs "high".
        # match.group(1) is class.
        return f'</div></div>\n<div class="vector-slide">\n<div class="vector-card {match.group(1)}">\n    <div class="vector-header">\n        <div class="vector-id">VEC-{vec_id}</div>'
    
    return original

# Pattern:
# <div class="vector-card (class)"> \n ... \n <div class="vector-id">VEC-(ID)</div>
# We need to match across lines.
pattern = r'<div class="vector-card ([a-z]+)">\s*<div class="vector-header">\s*<div class="vector-id">VEC-(\d+)</div>'

new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Now check the END of VEC-016.
# It needs to close the slide.
# Currently VEC-016 closes with </div>.
# My replacer added a "</div>" before VEC-016 (closing VEC-015).
# VEC-016 opens a slide.
# VEC-016 ends. We need to close its slide.
# And close track.
# The file defines controls and script after VEC-016 card close.
# <div class="carousel-btn prev" ...
# I need to ensure there is a closing div for VEC-016's slide before that.

# I'll search for the gap between VEC-016 end and controls.
# VEC-016 ends... then "<!-- Controls -->" or "<div class='carousel-btn prev'"
# I added "<!-- Controls -->" in my manual edit step 220.

final_fix_pattern = r'(VEC-016.*?</div>\s*</div>)(\s*<!-- Controls -->)'
# Group 1: VEC-016 content ending.
# Group 2: Controls start.
# Insert "</div>" in between.

def end_replacer(match):
    return match.group(1) + '\n</div> <!-- Close VEC-016 Slide -->\n' + match.group(2)

new_content = re.sub(final_fix_pattern, end_replacer, new_content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
