import os
from playwright.sync_api import sync_playwright

def render_pdf():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "report_engine", "out", "MAPA-RD-Template.html")
    output_path = os.path.join(base_dir, "04_Data", "reports", "MAPA-RD_V2.pdf")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html_uri = f"file:///{html_path.replace(os.sep, '/')}"

    print(f"Rendering PDF from: {html_uri}")
    print(f"Target Output: {output_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load the HTML file
        page.goto(html_uri, wait_until="networkidle")
        
        # Render PDF
        page.pdf(
            path=output_path,
            width="11in",   # Explicit Letter Landscape Width @ 96DPI
            height="8.5in", # Explicit Letter Landscape Height
            print_background=True,
            display_header_footer=False, # Disable Browser UI to remove margins
            margin={
                "top": "0px",
                "right": "0px",
                "bottom": "0px", 
                "left": "0px"
            }
        )
        
        browser.close()
        print(f"[SUCCESS] PDF Generated Successfully: {output_path}")

if __name__ == "__main__":
    render_pdf()
