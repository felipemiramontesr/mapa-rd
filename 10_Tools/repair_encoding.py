import os

files = [
    r"c:\Felipe\Projects\Mapa-rd\report_engine\theme\report.print.css",
    r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-V2-PRINT.html"
]

def repair_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Heuristic fix: The content looks like UTF-8 bytes decoded as Latin-1.
        # We try to reverse this: output = content.encode('latin-1').decode('utf-8')
        # However, we must be careful not to break characters that ARE correct.
        # But since the whole file was likely read/written wrong, the whole file should be consistent.
        
        # Let's test a known marker.
        if "Ã­" in content or "â€¢" in content:
            print(f"Repairing {os.path.basename(path)}...")
            try:
                fixed_content = content.encode('iso-8859-1').decode('utf-8')
                
                # Check if it looks better
                if "í" in fixed_content and "Ã­" not in fixed_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    print("Success.")
                else:
                    print("Repair check failed (patterns not fixed). Saving manually verified replacements if simple flip fails.")
                    # Fallback matches
                    # content = content.replace("Ã­", "í").replace("â€¢", "•").replace("â†’", "→")
                    # ... simple replace might be safer if encode/decode fails.
            except UnicodeError:
                print("Encoding reversal failed. Attempting manual replacement.")
                content = content.replace("Ã­", "í")
                content = content.replace("â€¢", "•")
                content = content.replace("â†’", "→")
                content = content.replace("Ã±", "ñ")
                content = content.replace("Ã³", "ó")
                content = content.replace("Ã¡", "á")
                content = content.replace("Ã©", "é")
                content = content.replace("Ãº", "ú")
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("Manual repair done.")
        else:
            print(f"{os.path.basename(path)} seems clean or unknown corruption.")

    except Exception as e:
        print(f"Error processing {path}: {e}")

for p in files:
    repair_file(p)
