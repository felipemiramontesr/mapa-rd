
import json
import os
import re
from collections import defaultdict

def parse_year(exposure_string):
    """Extracts year from strings like 'Filtración Masiva (2019)'."""
    match = re.search(r'\((\d{4})\)', exposure_string)
    if match:
        return int(match.group(1))
    return 9999 # Fallback for unknown years

def generate_timeline():
    base_dir = r"c:\Felipe\Projects\Mapa-rd"
    json_path = os.path.join(base_dir, "report_engine", "sample_data", "baseline_sample.report.json")
    target_path = os.path.join(base_dir, "report_engine", "out", "MAPA-RD-V2-PRINT.html")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    vectors = data.get("vectors", [])
    
    # Group by Year
    years_map = defaultdict(list)
    for vec in vectors:
        year = parse_year(vec.get('exposure_type', ''))
        years_map[year].append(vec)
        
    sorted_years = sorted(years_map.keys())
    
    # Chunk years (e.g., 6 years per slide)
    CHUNK_SIZE = 6
    year_chunks = [sorted_years[i:i + CHUNK_SIZE] for i in range(0, len(sorted_years), CHUNK_SIZE)]
    
    full_html = ""
    
    for page_idx, chunk in enumerate(year_chunks):
        
        # Build Grid HTML
        grid_html = ""
        for year in chunk:
            vectors_in_year = years_map[year]
            
            # Split into Top/Bottom stacks to balance visual load
            # Simple logic: Alternating or based on count? 
            # Let's simple split: first half bottom, second half top? 
            # Or just stack them all bottom? 
            # BETTER: All Bottom is cleaner for "Timeline", but "Horizon" implies centered.
            # Let's put them ALL in Bottom Stack for now, unless > 2.
            # If > 2, split.
            
            top_stack_html = ""
            bottom_stack_html = ""
            
            mid_point = len(vectors_in_year) // 2
            
            for i, vec in enumerate(vectors_in_year):
                # Create Pip HTML
                is_critical = vec['irv_level'] in ['Crítico', 'Máximo']
                crit_class = "critical" if is_critical else ""
                
                # Parse App Name (Everything before first colon)
                raw_title = vec.get('title', 'Unknown')
                if ':' in raw_title:
                    app_name = raw_title.split(':')[0].strip()
                else:
                    app_name = raw_title

                pip_html = f"""
                <div class="event-pip {crit_class}">
                    <div class="pip-title">{app_name}</div>
                    <div class="pip-meta">{vec['id']}</div>
                </div>
                """
                
                # Distribute
                if i < mid_point:
                    top_stack_html += pip_html
                else:
                    bottom_stack_html += pip_html

            # Column HTML
            col_html = f"""
            <div class="year-column">
                <div class="event-stack-top">
                    {top_stack_html}
                </div>
                
                <div class="year-marker"></div>
                
                <div class="year-label">{year if year != 9999 else 'N/A'}</div>
                
                <div class="event-stack-bottom">
                    {bottom_stack_html}
                </div>
            </div>
            """
            grid_html += col_html

        # Slide Template
        title_suffix = f" ({page_idx + 1}/{len(year_chunks)})" if len(year_chunks) > 1 else ""
        
        slide_html = f"""
        <!-- TIMELINE SLIDE {page_idx + 1} -->
        <div class="pdf-page timeline-page">
            <div class="vector-global-header">
                <h2>Horizonte de Exposición</h2>
                <p>Cronología de Incidentes Identificados{title_suffix}</p>
            </div>
            
            <div class="timeline-container">
                <div class="timeline-axis"></div>
                <div class="timeline-grid">
                    {grid_html}
                </div>
            </div>
            
            <!-- Footer -->
            <div style="position: absolute; bottom: 1.0cm; left: 1.0cm; font-size: 10px; color: rgba(255, 255, 255, 0.4); font-family: 'Inter', sans-serif;">
                Sin auditorías genéricas. Sin promesas vacías.
            </div>
        </div>
        """
        full_html += slide_html + "\n"

    # Inject
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "</body>" in content:
        # We append AFTER the last vector page. 
        # But wait, we just appended vectors. We should append at the end again.
        new_content = content.replace("</body>", full_html + "\n</body>")
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Success: Appended Timeline.")
    else:
        print("Error: Body tag not found.")

if __name__ == "__main__":
    generate_timeline()
