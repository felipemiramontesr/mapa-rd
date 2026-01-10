import os
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

# Paths
INPUT_SVG = r'assets/svg/dq.svg'
TEMP_SVG = r'assets/svg/logo-navy.svg'
OUTPUT_PDF = r'assets/logo-mapa-rd.pdf'

# Palette Map
COLOR_MAP = {
    r'#31A7E0': '#002060', # All Source Colors -> Single Navy
    r'#1E92D3': '#002060',
    r'#198DCF': '#002060',
    r'#198DD0': '#002060',
    r'#1084CA': '#002060',
}

def hex_to_rgb(hex_color):
    """Simple converter for debug if needed, logic is purely string replace."""
    pass

def process_logo():
    print(f"Reading {INPUT_SVG}...")
    try:
        with open(INPUT_SVG, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Replace Colors
        new_content = content
        for old_color, new_color in COLOR_MAP.items():
            # Use case-insensitive replace? SVG usually lowercase or uppercase hex.
            # We'll try regex to be safe.
            pattern = re.compile(re.escape(old_color), re.IGNORECASE)
            new_content = pattern.sub(new_color, new_content)
            print(f"  Replaced {old_color} -> {new_color}")
            
        # 2. Save Intermediate
        with open(TEMP_SVG, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Saved recolored SVG to {TEMP_SVG}")
        
        # 3. Convert to PDF
        print("Converting to PDF...")
        drawing = svg2rlg(TEMP_SVG)
        if drawing:
            renderPDF.drawToFile(drawing, OUTPUT_PDF)
            print(f"SUCCESS: Logo saved to {OUTPUT_PDF}")
        else:
            print("ERROR: svglib failed to parse SVG.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    process_logo()
