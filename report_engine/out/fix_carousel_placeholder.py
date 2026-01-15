import re

path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_vectors = False
vector_count = 0

# We'll identify the vectors section range roughly
# But actually, we can just process the whole file and look for "vector-card"

for i, line in enumerate(lines):
    # Detect Vectors Section Start
    if 'id="vectors-section"' in line:
        in_vectors = True
    
    # Detect Vectors Section End
    if in_vectors and '</section>' in line:
        # We might need to handle the closing carefully, but let's assume section closes at the end of the block
        # Actually, we rely on the specific card class presence
        pass

    # Check for Vector Card
    if in_vectors and '<div class="vector-card' in line:
        vector_count += 1
        
        # Check if already wrapped
        # Look back 1 or 2 lines for "vector-slide"
        is_wrapped = False
        if i > 0 and 'vector-slide' in new_lines[-1]:
            is_wrapped = True
        elif i > 1 and 'vector-slide' in new_lines[-2]:
            is_wrapped = True
            
        if not is_wrapped:
            # If not wrapped, we need to wrap it.
            # But wait, if this is VEC-002+ (orphans), we need to close the previous slide first?
            # Or if it's the start of a loose card.
            
            # Special case: VEC-001 is wrapped. VEC-002 is wrapped (from my previous edit).
            # VEC-007 is NOT wrapped.
            
            # If I insert "</div></div><div class='vector-slide'>", I assume the previous one was open.
            # But the problematic file state might have weird nesting.
            
            # Robust approach:
            # 1. Ensure "vector-slide" opens before "vector-card".
            # 2. Ensure "vector-slide" closes after "vector-card" closes.
            
            # Actually, simply injecting the wrapper structure BEFORE the card line sounds safer
            # provided we closed the PREVIOUS one.
            
            # Let's decide based on specific IDs if we can.
            pass
            
            # Since I can't easily parse full DOM, I'll rely on the fact that orphan cards result in strictly sequential div blocks.
            # I will just inject the slide wrapper immediately before the card div, 
            # AND inject the closing divs immediately after the card div closes? No, detecting close is hard.
            
            # Alternative:
            # Just fixing the start:
            # If line has "vector-card", and not wrapped:
            # new_lines.append('<div class="vector-slide">\n')
            
            # But we need to close the previous one?
            # My previous manual edits added "</div></div>" before the slide start.
    
    new_lines.append(line)

# This script is too passive. I need to be aggressive.
# I will read the file string, find all vector-cards, and restructure them.

content = "".join(lines)

# Find all vector cards
# Pattern: <div class="vector-card (.*?)">
matches = list(re.finditer(r'<div class="vector-card (.*?)">', content))

# We want to ensure every match is wrapped in <div class="vector-slide">...</div>
# The "..." extends to the matching </div>.
# Parsing matching div is hard with regex.

# Better Strategy using string replacement on specific IDs?
# I know the IDs are VEC-001 to VEC-016.

# Let's use specific replacement for the lines I know are broken.
# VEC-007 to VEC-016.
# I will find the line index for each VEC-ID and insert wrappers around it.

pass
