import os
import sys
from pdf_renderer import PDFRenderer

def main():
    # Define paths
    base_dir = os.path.dirname(__file__)
    html_path = os.path.join(base_dir, "out", "MAPA-RD-V2-PRINT.html")
    pdf_path = os.path.join(base_dir, "out", "MAPA-RD_V2.pdf")

    print(f"Generating PDF from: {html_path}")
    print(f"Output to: {pdf_path}")

    if not os.path.exists(html_path):
        print("ERROR: HTML file not found!")
        sys.exit(1)

    try:
        renderer = PDFRenderer()
        renderer.render_from_html_file(html_path, pdf_path)
        print("SUCCESS: PDF Generated Successfully.")
    except Exception as e:
        print(f"ERROR: Failed to generate PDF. {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
