import argparse
import json
import os
import sys
import jsonschema
from render_html import HTMLRenderer
from pdf_renderer import PDFRenderer

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schemas", "report.schema.json")

def load_schema():
    if not os.path.exists(SCHEMA_PATH):
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(1)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_data(data):
    """
    Validate data against the strict schema.
    Fast Fail: Exit immediately on error.
    """
    try:
        schema = load_schema()
        jsonschema.validate(instance=data, schema=schema)
        
        # Additional Asset Validation
        logo_path = data.get("assets", {}).get("logo_path")
        if logo_path and not os.path.exists(logo_path):
             print(f"ERROR: Asset missing: {logo_path}")
             sys.exit(1)
             
    except jsonschema.ValidationError as e:
        print(f"ERROR: Schema Validation Failed: {e.message}")
        print(f"Path: {list(e.path)}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected validation error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate strict corporate PDF report.")
    parser.add_argument("input_json", help="Path to the input JSON report data.")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_json)
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    # 1. Load Data
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Invalid JSON file: {e}")
        sys.exit(1)

    # 2. Validate
    print("Validating data...")
    validate_data(data)

    # 3. Setup Paths
    output_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(output_dir, exist_ok=True)
    
    # Filename: MAPA-RD_<CLIENT><TYPE><YYYYMMDD>v<VER><ID>.pdf
    # Sanitizing mostly for safety
    client = data['meta']['client_name'].replace(" ", "")
    rtype = "EXE" # Forced to maintain filename consistency per user request
    date = data['meta']['report_date'].replace("-", "")
    ver = data['meta']['report_version'].replace(".", "")
    rid = data['meta']['report_id']
    
    filename = f"MAPA-RD_{client}{rtype}{date}v{ver}{rid}.pdf"
    html_filename = filename.replace(".pdf", ".html")
    
    pdf_output_path = os.path.join(output_dir, filename)
    html_output_path = os.path.join(output_dir, html_filename)

    # 4. Render HTML
    print("Rendering HTML...")
    renderer = HTMLRenderer(template_dir=os.path.join(os.path.dirname(__file__), "templates"))
    html_content = renderer.render(data, output_path=html_output_path)

    # 5. Render PDF
    # print(f"Generating PDF at {pdf_output_path}...")
    # pdf_gen = PDFRenderer()
    # pdf_gen.render_from_html_file(html_output_path, pdf_output_path)

    print("SUCCESS: HTML generated (PDF skipped).")
    # print(f"PDF: {pdf_output_path}")

if __name__ == "__main__":
    main()
