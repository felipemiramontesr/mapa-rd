
import os

def reset_full():
    target_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-V2-PRINT.html"
    
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
       
    # We want to keep Page 1 (Cover) and Page 2 (IRD)
    # The Vector slides start after Page 2.
    # We can look for the "PAGE 3" comment or just "Vectores de Vulnerabilidad" header IF it's consistent.
    # But since Page 3 was manually appended originally, and then we appended rest...
    # It's safer to find the IRD closing div or "PAGE 3" marker if present.
    
    # In the current file, we manually added "<!-- PAGE 3... -->" originally.
    
    marker = "<!-- PAGE 3: VECTOR SLIDE"
    
    if marker in content:
        parts = content.split(marker)
        clean_content = parts[0]
        
        if "</body>" not in clean_content:
            clean_content += "\n</body>\n</html>"
            
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        print("Success: Stripped Pages 3+.")
    else:
        # Fallback if marker changed
        # Try finding the manual footer of page 2 and cutting after it?
        # Or look for class "vector-page" and cut before first occurence.
        # Let's try splitting by class "vector-page"
        if 'class="pdf-page vector-page"' in content:
            marker_alt = '<div class="pdf-page vector-page">'
            parts = content.split(marker_alt)
            # The first part is Cover + IRD.
            # But the marker is inside the split... wait.
            # split removes the separator.
            # We want to keep everything BEFORE the first vector page.
            clean_content = parts[0]
             # Check if we broke standard closing tags? 
             # Usually vector page starts with <!-- commment --> then <div...
            
            if "</body>" not in clean_content:
                clean_content += "\n</body>\n</html>"
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            print("Success: Stripped Pages 3+ (via class check).")
        else:
            print("Marker not found. Nothing to strip.")

if __name__ == "__main__":
    reset_full()
