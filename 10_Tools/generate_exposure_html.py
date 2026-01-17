
import json
import os
import locale

def generate_exposure():
    base_dir = r"c:\Felipe\Projects\Mapa-rd"
    json_path = os.path.join(base_dir, "report_engine", "sample_data", "baseline_sample.report.json")
    target_path = os.path.join(base_dir, "report_engine", "out", "MAPA-RD-V2-PRINT.html")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    vectors = data.get("vectors", [])
    
    # Pricing Logic (Hypothetical Dark Web Average 2025)
    TIERS = {
        "High": {"price": 50, "desc": "Datos Financieros/Identidad Crítica"},
        "Med": {"price": 15, "desc": "Credenciales Corporativas/Personales"},
        "Low": {"price": 5, "desc": "Datos de Perfil/Huella Digital"}
    }
    
    # Tally
    counts = {"High": 0, "Med": 0, "Low": 0}
    
    for vec in vectors:
        score = vec.get('irv_score', 0)
        # Use Score as proxy for value category
        if score >= 80:
            counts["High"] += 1
        elif score >= 50:
            counts["Med"] += 1
        else:
            counts["Low"] += 1
            
    # Calculate Totals
    rows_html = ""
    grand_total = 0
    
    for tier, info in TIERS.items():
        qty = counts[tier]
        if qty == 0: continue
        
        subtotal = qty * info['price']
        grand_total += subtotal
        
        rows_html += f"""
        <tr>
            <td>{info['desc']}</td>
            <td>{qty}</td>
            <td>${info['price']} USD</td>
            <td class="amount">${subtotal:,.2f}</td>
        </tr>
        """
        
    # Formatting Grand Total
    # locale.setlocale(locale.LC_ALL, '') # Rely on manual format for consistency
    total_str = f"${grand_total:,.2f} USD"
    
    # HTML Template
    slide_html = f"""
    <!-- PAGE: EXPOSURE VALUE -->
    <div class="pdf-page exposure-page">
        <div class="vector-global-header">
            <h2>Valor de Exposición</h2>
            <p>Estimación de Impacto Financiero en Mercado Negro</p>
        </div>
        
        <div class="exposure-content">
            
            <!-- LEFT: INVOICE -->
            <div class="invoice-card">
                <table class="invoice-table">
                    <thead>
                        <tr>
                            <th>CONCEPTO</th>
                            <th>CANTIDAD</th>
                            <th>PRECIO UNIT.</th>
                            <th style="text-align: right;">SUBTOTAL</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                        <tr class="invoice-total-row">
                            <td colspan="3">TOTAL ESTIMADO</td>
                            <td class="amount">{total_str}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- RIGHT: BIG NUMBER -->
            <div class="total-display">
                <div class="total-label">Valor Total en Mercado:</div>
                <div class="total-value-huge">{total_str}</div>
                <div class="total-disclaimer">
                    *Esta cifra representa el valor potencial de reventa de sus activos comprometidos en foros de cibercrimen, basado en índices de precios promedios de 2025. No refleja el costo de remediación empresarial.
                </div>
            </div>
            
        </div>
        
        <!-- Footer -->
        <div style="position: absolute; bottom: 1.0cm; left: 1.0cm; font-size: 10px; color: rgba(255, 255, 255, 0.4); font-family: 'Inter', sans-serif;">
            Sin auditorías genéricas. Sin promesas vacías.
        </div>
    </div>
    """

    # Inject
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "</body>" in content:
        new_content = content.replace("</body>", slide_html + "\n</body>")
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Success: Appended Exposure Value Page.")
    else:
        print("Error: Body tag not found.")

if __name__ == "__main__":
    generate_exposure()
