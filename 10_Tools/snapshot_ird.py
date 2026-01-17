from playwright.sync_api import sync_playwright
import os

def snapshot_ird():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "report_engine", "out", "MAPA-RD-Template.html")
    output_path = os.path.join(base_dir, "04_Data", "reports", "ird_proof.png")
    
    html_uri = f"file:///{html_path.replace(os.sep, '/')}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Go to page
        page.goto(html_uri, wait_until="networkidle")
        
        # Emulate print media to trigger our CSS fixes
        page.emulate_media(media="print")
        
        # Locate the IRD section. It might be .ird-page or #ird-page depending on template.
        # Based on report.css, it is .ird-page
        # We will take a screenshot of that element or the viewport showing it.
        # Since margins are 0 and it's full screen, we can just find it.
        
        locator = page.locator(".ird-page")
        
        if locator.count() > 0:
            # Scroll to it just in case
            locator.first.scroll_into_view_if_needed()
            # Take screenshot of the element
            locator.first.screenshot(path=output_path)
            print(f"[SUCCESS] Screenshot saved to: {output_path}")
        else:
            print("[ERROR] .ird-page not found")
        
        browser.close()

if __name__ == "__main__":
    snapshot_ird()
