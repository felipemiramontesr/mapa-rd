
path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-Template.html"

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_line = 345 # <div class="carousel-track" id="vectorsTrack"> (0-indexed roughly 344)
end_line = 1375  # </div> <!-- Close Track --> (0-indexed 1374)

# find real indices
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'id="vectorsTrack"' in line:
        start_idx = i
    if '<!-- Close Track -->' in line:
        end_idx = i
        break

print(f"Track Range: {start_idx} to {end_idx}")

segment = lines[start_idx+1 : end_idx] # Exclude start tag line, exclude closing

open_tags = 0
close_tags = 0

for line in segment:
    open_tags += line.count('<div')
    close_tags += line.count('</div>')

print(f"Opens: {open_tags}")
print(f"Closes: {close_tags}")
print(f"Balance: {open_tags - close_tags}")
