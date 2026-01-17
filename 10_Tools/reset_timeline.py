
import os

def reset_timeline():
    target_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-V2-PRINT.html"
    
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    marker = "<!-- TIMELINE SLIDE 1 -->"
    
    if marker in content:
        parts = content.split(marker)
        # Keep the first part (everything before the timeline)
        clean_content = parts[0]
        
        # Ensure it closes properly if we cut off body/html (which were likely at the end)
        # The split removes the marker and everything after.
        # Check if </body> tags were in the removed part (yes they were).
        
        if "</body>" not in clean_content:
            clean_content += "\n</body>\n</html>"
            
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        print("Success: Timeline stripped.")
    else:
        print("Marker not found. Nothing to strip.")

if __name__ == "__main__":
    reset_timeline()
