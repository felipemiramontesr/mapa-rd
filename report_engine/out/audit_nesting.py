
from html.parser import HTMLParser

class NestingAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_section = False
        self.in_container = False
        self.in_track = False
        self.in_slide = False
        self.track_open_count = 0
        self.slide_count = 0
        self.cards_inside_track = 0
        self.cards_outside_track = 0
        self.slides_inside_track = 0
        self.slides_outside_track = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')
        id_name = attrs_dict.get('id', '')

        if id_name == 'vectors-section':
            self.in_section = True
            print("Section START")
        
        if self.in_section:
            if 'carousel-track' in class_name or id_name == 'vectorsTrack':
                self.in_track = True
                print("Track START")
            
            if 'vector-slide' in class_name:
                self.slide_count += 1
                if self.in_track:
                    self.slides_inside_track += 1
                else:
                    self.slides_outside_track += 1
                    print(f"WARNING: Slide {self.slide_count} is OUTSIDE track!")

            if 'vector-card' in class_name:
                if self.in_track:
                    self.cards_inside_track += 1
                else:
                    self.cards_outside_track += 1
                    print(f"WARNING: Card found OUTSIDE track!")

    def handle_endtag(self, tag):
        if tag == 'div':
            # This is hard to track without a stack, but we can infer closure if we encounter tags outside.
            # Simplified: Since we can't easily track exact div closures in a streaming parser without strict stack
            # We will rely on the "status" flags which is hard.
            pass

# Since strict parsing is hard with flawed HTML, let's stick to a simpler line-based state machine
# that counts depth.

print("--- auditing indentation ---")
depth = 0
in_track = False
track_depth = -1
cards_in = 0
cards_out = 0

with open(r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html", 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        clean = line.strip()
        
        # Track Depth
        # Count <div> and </div> tokens roughly
        open_divs = line.count('<div')
        close_divs = line.count('</div>')
        
        # Check for Track Start
        if 'id="vectorsTrack"' in line:
            in_track = True
            track_depth = depth # The depth at which track started (before current line increments)
            print(f"Track starts at Line {line_num}, Depth {depth}")
            
        # Update Depth
        depth += (open_divs - close_divs)
        
        # Check for Card
        if '<div class="vector-card' in line:
            if in_track:
                cards_in += 1
                print(f"Card at {line_num} is INSIDE. Depth: {depth}")
            else:
                cards_out += 1
                print(f"CRITICAL: Card at {line_num} is OUTSIDE track! Depth: {depth}")

        # Check closing of track
        if in_track and depth <= track_depth:
            print(f"Track potentially closed at Line {line_num}. Depth dropped to {depth}")
            in_track = False

print(f"Cards Inside: {cards_in}")
print(f"Cards Outside: {cards_out}")
