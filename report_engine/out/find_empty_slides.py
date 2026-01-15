
from html.parser import HTMLParser

class EmptySlideHunter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_slide = False
        self.slide_index = 0
        self.has_card = False
        self.empty_indices = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()
        
        if 'vector-slide' in classes:
            self.in_slide = True
            self.slide_index += 1
            self.has_card = False
        
        if self.in_slide and 'vector-card' in classes:
            self.has_card = True

    def handle_endtag(self, tag):
        pass 
        # Ideally we'd detect slide close, but logic is simpler:
        # Upon finding NEXT slide start or track end, check if previous had card.
        # But this streaming parser is limited. 
        # Let's assume standard formatting: <div class="vector-slide"> ... <div class="vector-card">

# Let's use string analysis instead for robustness against broken HTML
with open(r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html", 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Regex to find slide content
# <div class="vector-slide">(.*?)<div class="vector-slide" or end of track
# This is tricky because of nesting.

# Simple line scanner
current_slide = 0
has_card = False
empty_slides = []

lines = text.splitlines()
in_track = False

for i, line in enumerate(lines):
    if 'id="vectorsTrack"' in line:
        in_track = True
        continue
    
    if not in_track: continue
    if '<!-- Close Track' in line: break

    if '<div class="vector-slide">' in line:
        # check previous
        if current_slide > 0 and not has_card:
            empty_slides.append(current_slide)
        
        current_slide += 1
        has_card = False # reset for new slide
    
    if 'class="vector-card' in line:
        has_card = True

# Check last one
if current_slide > 0 and not has_card:
    empty_slides.append(current_slide)

print(f"Total Slides Scanned: {current_slide}")
print(f"Empty Slides Indices (1-based): {empty_slides}")
