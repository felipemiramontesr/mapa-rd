
import re

file_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy:
# We know the structure of a card end and start.
# Card end is 5 closing divs? No, structure varies.
# Look at VEC-004 to VEC-005 transition in the viewed file (Step 412).
# Line 610: </div> (Closes Description Card)
# Line 609: </div> (Closes Vector Body)
# Line 610: </div> (Closes Vector Card VEC-004)
# Line 612: <div class="vector-card critical"> (Starts VEC-005)

# Pattern: 3 closing divs followed by whitespace followed by <div class="vector-card
# Let's be safer.
# Find all occurrences of `<div class="vector-card`
# Check what precedes it.
# If it's NOT `<div class="vector-slide">` (ignoring whitespace), then we are likely in a sibling situation.

# Actually, if I just replace `</div>\s*<div class="vector-card` with `</div></div><div class="vector-slide"><div class="vector-card`?
# That assumes the `</div>` before it was closing the previous CARD. which it is.
# So `</div>` (close card) -> `</div>` (close slide) -> `<div class="vector-slide">` (open slide) -> `<div class="vector-card">` (open card).
# But wait, if they are currently siblings, there is NO `vector-slide` to close between them.
# There is only ONE `vector-slide` wrapper.
# So I need: `</div>` (close card) -> `</div>` (close CURRENT shared slide) -> `<div class="vector-slide">` (open NEW slide) -> `<div class="vector-card`

# So the replacement is:
# FROM: `(</div>\s+)(<div class="vector-card)`
# TO:   `\1</div><div class="vector-slide">\n\2`

# We must be careful not to do this for the FIRST card in a slide.
# The first card is preceded by `<div class="vector-slide">`.
# So we use negative lookbehind? Or just check content.

pattern = r'(</div>\s+)(<div class="vector-card)'

def replacement(match):
    # Check context if possible, or just apply?
    # If the text immediately preceding the match group 1 is "vector-slide">", then DON'T replace.
    # But regex replace doesn't give us full context easily unless we capture it.
    return match.group(1) + '</div><div class="vector-slide">\n' + match.group(2)

# Only apply this transformation if we are NOT immediately following a vector-slide open.
# Regex: `(?<!<div class="vector-slide">)\s*(<div class="vector-card)`
# Python regex lookbehind requires fixed width.
# Let's iterate.

new_content = ""
last_pos = 0

# We restricting this logic to the Vectors Section only to be safe.
start_marker = '<div class="carousel-track" id="vectorsTrack">'
end_marker = '<!-- Close Track (Fixed Missing Div) -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find track boundaries.")
    exit()

pre_content = content[:start_idx]
track_content = content[start_idx:end_idx]
post_content = content[end_idx:]

# Process track content
# We want to insert `</div><div class="vector-slide">` between sibling cards.
# Identify sibling cards: `</div>` followed by `<div class="vector-card`
# But EXCLUDE `class="vector-slide">\s*<div class="vector-card`

# We can replace ALL `<div class="vector-card` with `</div><div class="vector-slide"><div class="vector-card`
# AND THEN cleanup the double slides at the beginning?
# Or smarter:
# specific regex for `</div>\s*<div class="vector-card`

fixed_track = re.sub(r'(</div>\s*)(<div class="vector-card)', r'\1</div>\n<div class="vector-slide">\n\2', track_content)

# This might mistakenly affect the FIRST card if it was preceded by a div closing (unlikely, usually slide open).
# Let's check the first card.
# The HTML is `<div class="vector-slide">\n<div class="vector-card` -> Matched? No, because it starts with vector-slide, not </div>.
# Wait, let's verify VEC-001.

# If VEC-001 is: `<div class="vector-slide"><div class="vector-card"` -> Regex `(</div>\s*)` will NOT match.
# If VEC-002 is sibling: `...</div>\n<div class="vector-card"` -> Regex WILL match `</div>\n` and replace.
# Result: `...</div>\n</div>\n<div class="vector-slide">\n<div class="vector-card"`
# This effectively closes the previous slide and opens a new one.

# What if VEC-002 was ALREADY in a slide?
# `...</div></div><div class="vector-slide"><div class="vector-card"`
# The regex `(</div>\s*)` might match the `</div>` before the slide div? No, because the next text is `<div class="vector-slide`.
# Our regex demands `<div class="vector-card` immediately after.
# So if the code is correct (already separated), it looks like:
# `</div>\n</div>\n<div class="vector-slide">\n<div class="vector-card ...`
# The match `</div>\s*<div class="vector-card` will NOT happen because `<div class="vector-slide">` interrupts it.

# So this regex implies: "Any vector card that follows a closing div implies it's a sibling, because if it were a new slide, there would be a slide tag in between."
# This logic is sound.

final_content = pre_content + fixed_track + post_content

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Fixed grouping for siblings.")
