import json
import os

def generate_html():
    base_dir = r"c:\Felipe\Projects\Mapa-rd"
    json_path = os.path.join(base_dir, "report_engine", "sample_data", "baseline_sample.report.json")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    vectors = data.get("vectors", [])
    
    # Template string (based on VEC-001 approved design)
    template = """
    <!-- PAGE {page_num}: VECTOR SLIDE ({vec_id}) -->
    <div class="pdf-page vector-page">
        
        <div class="vector-global-header">
            <h2>Vectores de Vulnerabilidad</h2>
            <p>Evidencia Técnica y Ruta de Cierre Priorizada</p>
        </div>

        <div class="vector-main-card">
            
            <!-- ROW 1: HEADER -->
            <div class="vec-row-header">
                <div class="vec-id">{vec_id}</div>
                <div class="vec-title">{title}</div>
                <div class="vec-badge">
                    <span>{score}</span>
                    <span>{level_upper}</span>
                </div>
            </div>

            <!-- ROW 2: METADATA -->
            <div class="vec-row-meta">
                <div class="vec-meta-box">
                    <span class="vec-meta-label">ACTIVO:</span>
                    <span class="vec-meta-val">{asset}</span>
                </div>
                <div class="vec-meta-box">
                    <span class="vec-meta-label">TIPO:</span>
                    <span class="vec-meta-val">{asset_type}</span>
                </div>
                <div class="vec-meta-box">
                    <span class="vec-meta-label">EXPOSICIÓN:</span>
                    <span class="vec-meta-val">{exposure}</span>
                </div>
            </div>

            <!-- ROW 3: SPLIT DETAILS -->
            <div class="vec-row-details">
                <!-- RUTA DE CIERRE (Ordered List) -->
                <div class="vec-detail-col">
                    <div class="vec-col-header">RUTA DE CIERRE</div>
                    <ol class="vec-list numbered">
                        {remediation_items}
                    </ol>
                </div>

                <!-- IMPACTO (Unordered List) -->
                <div class="vec-detail-col">
                    <div class="vec-col-header">IMPACTO</div>
                    <ul class="vec-list">
                        {impact_items}
                    </ul>
                </div>
            </div>

            <!-- ROW 4: DESCRIPTION -->
            <div class="vec-row-desc">
                <div class="vec-desc-header">DESCRIPCIÓN DEL EVENTO</div>
                <div class="vec-desc-text">
                    {description}
                </div>
            </div>

        </div>

        <!-- Manual Footer (Page {page_num}) -->
        <div style="position: absolute; bottom: 1.0cm; left: 1.0cm; font-size: 10px; color: rgba(255, 255, 255, 0.4); font-family: 'Inter', sans-serif;">
            Sin auditorías genéricas. Sin promesas vacías.
        </div>
    </div>
    """
    
    full_html = ""
    
    # Start from index 1 (VEC-002) because VEC-001 is already manually added as Page 3
    # Actually, to be clean, let's generate ALL of them. 
    # BUT, Page 3 is already there. So I should generate VEC-002 to VEC-016.
    # Page numbering starts at 4 for VEC-002.
    
    page_counter = 4
    
    for i, vec in enumerate(vectors):
        if vec['id'] == "VEC-001":
            continue # Skip VEC-001
            
        # Build list items
        remediation_html = ""
        for step in vec.get('remediation_steps', []):
            remediation_html += f"<li>{step}</li>\n                        "
            
        impact_html = ""
        for bullet in vec.get('impact_bullets', []):
            impact_html += f"<li>{bullet}</li>\n                        "
            
        html_chunk = template.format(
            page_num=page_counter,
            vec_id=vec['id'],
            title=vec['title'],
            score=vec['irv_score'],
            level_upper=str(vec['irv_level']).upper(),
            asset=vec['asset'],
            asset_type=vec['asset_type'],
            exposure=vec['exposure_type'],
            remediation_items=remediation_html,
            impact_items=impact_html,
            description=vec['description']
        )
        
        full_html += html_chunk +("\n\n")
        page_counter += 1
    # Read target file
    target_path = os.path.join(base_dir, "report_engine", "out", "MAPA-RD-V2-PRINT.html")
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Insert before </body>
    if "</body>" in content:
        new_content = content.replace("</body>", full_html + "\n</body>")
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Success: Appended vectors to HTML.")
    else:
        print("Error: Could not find </body> tag.")

if __name__ == "__main__":
    generate_html()
