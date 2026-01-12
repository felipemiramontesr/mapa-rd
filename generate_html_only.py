
import json
import os
import sys
from report_engine.render_html import HTMLRenderer

# Hardcode the path to ensure we target the right file and use the forced 'EXE' type logic manually if needed
INPUT_PATH = "report_engine/sample_data/baseline_sample.report.json"
OUTPUT_DIR = "report_engine/out"

def main():
    print("Loading data...")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Force EXE type for filename consistency (as previously requested)
    client_safe = data['meta']['client_name'].replace(" ", "")
    rtype = "EXE" 
    date = data['meta']['report_date'].replace("-", "")
    ver = data['meta']['report_version'].replace(".", "")
    rid = data['meta']['report_id']

    filename = f"MAPA-RD_{client_safe}{rtype}{date}v{ver}{rid}.html"
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Use the User's target filename logic if different, but based on previous turns:
    # "MAPA-RD_ACMECorpEXE20260111v10RPT-2026-001.html" was forced copy.
    # The new filename based on new client name will be different.
    # User said: "El nombre debe ir completo... Felipe...".
    # This will change the filename if we generate a new one.
    # BUT user said earlier: "Force existing filename".
    # Let's generate the NEW correct filename first, then COPY it to the Legacy filename 
    # so the user doesn't lose their view if they are attached to the old one.
    
    print(f"Rendering HTML to {output_path}...")
    
    renderer = HTMLRenderer(template_dir="report_engine/templates")
    renderer.render(data, output_path=output_path)
    
    # Also overwrite the "Legacy" viewer path just in case
    legacy_path = os.path.join(OUTPUT_DIR, "MAPA-RD_ACMECorpEXE20260111v10RPT-2026-001.html")
    with open(output_path, 'r', encoding='utf-8') as src:
        content = src.read()
    with open(legacy_path, 'w', encoding='utf-8') as dst:
        dst.write(content)
        
    print(f"Updated Legacy View: {legacy_path}")

if __name__ == "__main__":
    main()
