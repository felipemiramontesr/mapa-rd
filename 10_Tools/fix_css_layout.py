import os

css_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\theme\report.print.css"
search_grid = """
.inaction-grid {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 1rem;
}
"""

replace_grid = """
.inaction-grid {
    display: flex;
    flex-direction: row;
    align-items: stretch; /* EQUAL HEIGHT */
    justify-content: space-between;
    width: 100%;
    gap: 1.5rem;
}
"""

search_card = """
/* CARDS */
.inaction-card {
    background: rgba(13, 17, 34, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 2.5rem;
    display: flex !important;
    flex-direction: column !important;
    align-items: center;
    width: 30%; 
    height: 520px;
    min-height: 520px;
    backdrop-filter: blur(12px);
"""

replace_card = """
/* CARDS */
.inaction-card {
    background: rgba(13, 17, 34, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    display: flex !important;
    flex-direction: column !important;
    align-items: center;
    width: 30%; 
    height: auto !important; /* Flex stretch */
    min-height: 580px; /* Safe minimum */
    backdrop-filter: blur(12px);
"""

try:
    with open(css_path, 'r', encoding='latin-1') as f:
        content = f.read()
    
    # Normalize line endings just in case
    # content = content.replace('\r\n', '\n') 
    
    # We might not find exact matches if spaces differ, so let's try a simpler replace or regex if needed.
    # For now, let's try direct replace of the blocks we saw in view_file.
    
    # Replace Grid
    # Removing exact textual match relying on what I saw earlier.
    # If exact match fails, I will use a more robust regex approach in next step.
    
    # Let's try to just append the overrides at the end, BUT I verified earlier that appending caused issues if there are multiple.
    # Best way: Read, Regex Replace, Write.
    
    import re
    
    # Regex for Grid
    grid_pattern = re.compile(r'\.inaction-grid\s*\{[^}]*align-items:\s*center;[^}]*\}', re.DOTALL)
    if grid_pattern.search(content):
        print("Found Grid pattern, replacing...")
        content = grid_pattern.sub(replace_grid.strip(), content)
    else:
        print("Grid pattern not found, might have been changed already.")

    # Regex for Card (The 520px version)
    card_pattern = re.compile(r'\.inaction-card\s*\{[^}]*height:\s*520px[^}]*\}', re.DOTALL)
    if card_pattern.search(content):
        print("Found Card pattern, replacing...")
        content = card_pattern.sub(replace_card.strip(), content)
    else:
        print("Card pattern (520px) not found.")

    # Write back
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("CSS updated successfully.")

except Exception as e:
    print(f"Error: {e}")
