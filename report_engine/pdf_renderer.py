import os
from playwright.sync_api import sync_playwright

class PDFRenderer:
    def __init__(self):
        pass
        
    def render_from_html_file(self, html_path, output_path):
        """
        Render a PDF from an existing local HTML file using Playwright.
        
        Args:
            html_path (str): Absolute path to the HTML file.
            output_path (str): Absolute path for the output PDF.
        """
        html_uri = f"file:///{html_path.replace(os.sep, '/')}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the local file
            page.goto(html_uri, wait_until="networkidle")
            
            # Strict PDF Options
            page.pdf(
                path=output_path,
                format="Letter",
                landscape=False,
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=False,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"} # CSS handles margins
            )
            browser.close()
            
    def render_from_string(self, html_string, output_path, base_url=None):
        """
        Render a PDF from an HTML string. 
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Load content
            if base_url:
                 page.set_content(html_string, wait_until="networkidle", base_url=base_url)
            else:
                 page.set_content(html_string, wait_until="networkidle")

            # Strict PDF Options
            page.pdf(
                path=output_path,
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=False
            )
            browser.close()

if __name__ == "__main__":
    pass
