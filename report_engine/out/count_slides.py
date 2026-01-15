
from html.parser import HTMLParser

class TrackChildCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_track = False
        self.track_children = 0
        self.track_depth = 0
        self.current_depth = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Track depth
        if tag == "div":
            self.current_depth += 1
            
        # Detect Track
        if attrs_dict.get('id') == 'vectorsTrack':
            self.in_track = True
            self.track_depth = self.current_depth
            print("Track Found")
            return

        if self.in_track:
            # Direct child check:
            # If current depth is track_depth + 1, it is a direct child
            if self.current_depth == self.track_depth + 1:
                if tag == "div":
                    # Check if it has vector-slide class
                    classes = attrs_dict.get('class', '').split()
                    if 'vector-slide' in classes:
                        self.track_children += 1
                        print(f"Slide found! Count: {self.track_children}")
                    else:
                        print(f"Non-slide direct child found: {tag} class={classes}")

    def handle_endtag(self, tag):
        if tag == "div":
            self.current_depth -= 1
            if self.in_track and self.current_depth < self.track_depth:
                self.in_track = False
                print("Track Closed")

counter = TrackChildCounter()
with open(r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html", 'r', encoding='utf-8') as f:
    counter.feed(f.read())

print(f"Total Slides detected: {counter.track_children}")
