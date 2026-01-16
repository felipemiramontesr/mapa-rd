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
            format="Letter",
            landscape=True,
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=True, 
            footer_template="""
                <style>
                    * { margin: 0 !important; padding: 0 !important; box-sizing: border-box !important; }
                </style>
                <div style="width: 100%; height: 100%; position: relative; background-color: #0a0e27; -webkit-print-color-adjust: exact;">
                    <div style="position: absolute; right: 1.0cm; bottom: 1.0cm; font-size: 12px; line-height: 1; font-family: 'Arial Narrow', sans-serif; color: rgba(255, 255, 255, 0.5); white-space: nowrap;">
                        Página <span class="pageNumber"></span> de <span class="totalPages"></span>
                    </div>
                </div>
            """,
            margin={
                "top": "0px",
                "right": "0px",
                "bottom": "1.5cm", # Safe Zone guarantees no overlap
                "left": "0px"
            }
        )
        
        browser.close()
        print(f"[SUCCESS] PDF Generated Successfully: {output_path}")

if __name__ == "__main__":
    render_pdf()
