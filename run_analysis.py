import sys
import os
import json
import requests
import time
from datetime import datetime
import re

# Add paths for report engine components
sys.path.append(r'c:\Felipe\Projects\Mapa-rd\05_Build\report_engine')
sys.path.append(r'c:\Felipe\Projects\Mapa-rd\07_Src')

from pdf_renderer import PDFRenderer
from client_manager import ClientManager

# API Configuration
HIBP_API_KEY = "344ba3142e664cf29effcebea34e9f3e"
TEMPLATE_PATH = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-MASTER-TEMPLATE.html"

class ReportOrchestrator:
    def __init__(self):
        self.client_manager = ClientManager()
        self.pdf_renderer = PDFRenderer()

    def fetch_hibp_data(self, email):
        """Fetches data from HIBP API with rate limit safety."""
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
        headers = {
            "hibp-api-key": HIBP_API_KEY,
            "user-agent": "MAPA-RD-Orchestrator"
        }
        
        print(f"[*] Fetching breaches for: {email}")
        try:
            time.sleep(1.6) # Safe HIBP delay
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # Sort by date (descending) as priority
                return sorted(data, key=lambda x: x['BreachDate'], reverse=True)
            elif response.status_code == 404:
                return []
            else:
                print(f"[!] HIBP Error {response.status_code}")
                return []
        except Exception as e:
            print(f"[!] Connection Error: {e}")
            return []

    def calculate_metrics(self, breaches):
        """Calculates digital risk indicators."""
        if not breaches:
            return {
                "ird_score": 5, "ird_label": "BAJO", "ird_color": "#2ecc71",
                "latency_years": 0, "exposure_total": "$0.00",
                "earliest_year": datetime.now().year,
                "ird_context_description": "Postura de seguridad sólida. No se detectaron exposiciones activas en bases de datos monetizadas."
            }

        # 1. Latency Calculation
        oldest_date_str = breaches[-1]['BreachDate']
        oldest_year = int(oldest_date_str.split('-')[0])
        current_year = datetime.now().year
        latency = current_year - oldest_year

        # 2. IRD Scoring (Logarithmic/Weighted feel)
        score = min(25 + (len(breaches) * 6), 98)
        
        label, color, risk_text, action = "BAJO", "#2ecc71", "Riesgo Controlado", "Monitoreo"
        if score > 40: label, color, risk_text, action = "MEDIO", "#ffeaa7", "Riesgo Latente", "Revisión"
        if score > 70: label, color, risk_text, action = "ALTO", "#ff9f43", "Alto riesgo", "Cambio prioritario"
        if score > 85: label, color, risk_text, action = "CRÍTICO", "#ff7675", "Compromiso de identidad", "Acción inmediata"
        if score > 95: label, color, risk_text, action = "MÁXIMO", "#a29bfe", "Máximo riesgo sistémico", "Contención de emergencia"

        context_desc = f"<strong>Urgencia Inmediata:</strong> Un IRD de {score} señala un <strong>{risk_text}</strong>. Se identificaron múltiples vectores de acceso real. Se requiere <strong>{action}</strong> para mitigar un posible fraude inminente."

        # 3. Exposure Valuation (Dark Web Pricing Estimate)
        total_val = 0
        for b in breaches:
            val = 5 # Entry price
            if "Passwords" in b["DataClasses"]: val += 15
            if any(k in str(b["DataClasses"]) for k in ["Bank", "Credit", "Financial"]): val += 50
            total_val += val
        
        return {
            "ird_score": score,
            "ird_label": label,
            "ird_color": color,
            "latency_years": latency,
            "exposure_total": f"${total_val:,.2f} USD",
            "ird_context_description": context_desc
        }

    def generate_vector_html(self, breaches):
        """Generates the detailed Vector slides. Design-safe to prevent overflows."""
        html = ""
        for i, b in enumerate(breaches):
            # Severity logic per card
            severity = 50
            badge, color = "ALTO", "#ff9f43"
            if "Passwords" in b["DataClasses"]: 
                severity = 80
                badge, color = "CRÍTICO", "#ff7675"
            
            # Truncate description for design safety (300 chars max)
            desc_clean = re.sub('<[^<]+?>', '', b['Description'])
            if len(desc_clean) > 300:
                desc_clean = desc_clean[:297] + "..."
            
            pwn_count = f"{b['PwnCount']:,}"
            data_str = ", ".join(b['DataClasses'][:3]) # Keep it brief

            # Template-literal style construction (No double-braces in Python code)
            slide = f"""
            <div class="pdf-page vector-page">
                <div class="vector-global-header">
                    <h2>Vectores de Vulnerabilidad</h2>
                    <p>Evidencia Técnica y Ruta de Cierre Priorizada</p>
                </div>

                <div class="vector-main-card" style="--risk-color: {color};">
                    <div class="vec-row-header">
                        <div class="vec-id">VEC-{i+1:03d}</div>
                        <div class="vec-title">{b['Name']}</div>
                        <div class="vec-badge">
                            <span>{severity}</span>
                            <span>{badge}</span>
                        </div>
                    </div>

                    <div class="vec-row-meta">
                        <div class="vec-meta-box">
                            <span class="vec-meta-label">Fecha:</span>
                            <span class="vec-meta-val">{b['BreachDate']}</span>
                        </div>
                        <div class="vec-meta-box">
                            <span class="vec-meta-label">Registros:</span>
                            <span class="vec-meta-val">{pwn_count}</span>
                        </div>
                        <div class="vec-meta-box">
                            <span class="vec-meta-label">Datos:</span>
                            <span class="vec-meta-val">{data_str}</span>
                        </div>
                    </div>

                    <div class="vec-row-details">
                        <div class="vec-detail-col">
                            <div class="vec-col-header">Ruta de cierre</div>
                            <ol class="vec-list numbered">
                                <li>Cambiar contraseñas asociadas a este servicio.</li>
                                <li>Habilitar 2FA (Tokens App).</li>
                                <li>Terminar sesiones activas.</li>
                            </ol>
                        </div>
                        <div class="vec-detail-col">
                            <div class="vec-col-header">Impacto</div>
                            <ul class="vec-list">
                                <li>Exposición de credenciales operativas.</li>
                                <li>Riesgo de suplantación ARCO.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="vec-row-desc">
                        <div class="vec-desc-header">Descripción</div>
                        <div class="vec-desc-text">{desc_clean}</div>
                    </div>
                </div>
            </div>
            """
            html += slide
        return html

    def generate_timeline_html(self, breaches):
        """Generates a high-fidelity Timeline using the CSS axis structure."""
        if not breaches: return ""
        
        # Group by year
        year_groups = {}
        for b in breaches:
            year = b['BreachDate'].split('-')[0]
            if year not in year_groups: year_groups[year] = []
            year_groups[year].append(b['Name'])
        
        sorted_years = sorted(year_groups.keys(), reverse=True)
        
        items_html = ""
        for year in sorted_years:
            names = ", ".join(year_groups[year][:3])
            count = len(year_groups[year])
            names_text = names + (f" y {count-3} más" if count > 3 else "")
            
            item = f"""
            <div class="timeline-event" style="margin-bottom: 2.5rem; display: flex; align-items: flex-start; gap: 2rem;">
                <div class="timeline-year-label" style="font-family:'Space Grotesk'; font-size: 1.5rem; font-weight: 700; color: #a29bfe; width: 80px; text-align: right;">{year}</div>
                <div class="timeline-indicator" style="position: relative; margin-top: 0.5rem;">
                    <div class="timeline-dot" style="width: 12px; height: 12px; border-radius: 50%; background: #6c5ce7; box-shadow: 0 0 10px #6c5ce7;"></div>
                </div>
                <div class="timeline-card-lite" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; flex-grow: 1;">
                    <div class="tl-title" style="font-weight: 700; color: #fff; margin-bottom: 0.3rem;">{count} Incidentes Detectados</div>
                    <div class="tl-names" style="font-size: 0.8rem; color: #94a3b8;">{names_text}</div>
                </div>
            </div>
            """
            items_html += item

        return f"""
        <div class="pdf-page timeline-page">
            <div class="vector-global-header">
                <h2>Horizonte de Exposición</h2>
                <p>Cronología Técnica de Incidentes Identificados</p>
            </div>
            <div class="timeline-master-container" style="position: relative; padding: 2rem 5rem;">
                <div class="timeline-axis-line" style="position: absolute; left: 104px; top: 0; bottom: 0; width: 2px; background: rgba(162, 155, 254, 0.1);"></div>
                <div class="timeline-scroll-area">
                    {items_html}
                </div>
            </div>
        </div>
        """

    def generate_invoice_html(self, breaches):
        """Generates dynamic Dark Web Invoice rows."""
        rows = ""
        totals = {"pass": 0, "fin": 0, "id": 0}
        for b in breaches:
            dc = str(b["DataClasses"]).lower()
            if "password" in dc: totals["pass"] += 1
            if any(x in dc for x in ["bank", "credit", "financial"]): totals["fin"] += 1
            if any(x in dc for x in ["name", "email", "username"]): totals["id"] += 1
            
        if totals["fin"]: rows += f"<tr><td>Datos Financieros/Bancarios</td><td>{totals['fin']}</td><td>$50.00</td><td class='amount'>${totals['fin']*50:,.2f}</td></tr>"
        if totals["pass"]: rows += f"<tr><td>Credenciales y Accesos</td><td>{totals['pass']}</td><td>$15.00</td><td class='amount'>${totals['pass']*15:,.2f}</td></tr>"
        if totals["id"]: rows += f"<tr><td>Identidades Básicas</td><td>{totals['id']}</td><td>$1.00</td><td class='amount'>${totals['id']*1:,.2f}</td></tr>"
        return rows

    def run_analysis(self, name, email):
        print(f"[*] Starting MAPA-RD Analysis for {name}")
        
        # 1. Onboarding
        cid = self.client_manager.create_client(name, email)
        report_dir = self.client_manager.create_report(cid)
        
        # 2. Strict Filename Setup
        # dir format: MAPA-RD-[Name]-[CID]-[RID]-[Date]
        dir_basename = os.path.basename(report_dir)
        parts = dir_basename.split('-')
        rid = parts[-4] # R001
        cid_code = parts[-5] # C001
        norm_name = "-".join(parts[2:-5])
        iso_date = "-".join(parts[-3:]) # YYYY-MM-DD
        
        # Requested Format: MAPA-RD-[Name]-[CID]-[Date]-[RID]
        base_filename = f"MAPA-RD-{norm_name}-{cid_code}-{iso_date}-{rid}"
        
        # 3. Data Extraction
        breaches = self.fetch_hibp_data(email)
        metrics = self.calculate_metrics(breaches)
        
        # 4. HTML Preparation
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Dynamic Content Blocks
        content = content.replace("{{ client_name }}", name)
        content = content.replace("{{ report_id }}", f"{cid_code}-{rid}")
        content = content.replace("{{ report_date }}", iso_date)
        content = content.replace("{{ ird_score }}", str(metrics["ird_score"]))
        content = content.replace("{{ ird_label }}", metrics["ird_label"])
        content = content.replace("{{ ird_color }}", metrics["ird_color"])
        content = content.replace("{{ ird_color|default('#fff') }}", metrics["ird_color"])
        content = content.replace("{{ ird_context_description }}", metrics["ird_context_description"])
        content = content.replace("{{ latency_years }}", str(metrics["latency_years"]))
        
        content = content.replace("{{ vector_pages_html }}", self.generate_vector_html(breaches))
        content = content.replace("{{ timeline_pages_html }}", self.generate_timeline_html(breaches))
        content = content.replace("{{ exposure_invoice_rows }}", self.generate_invoice_html(breaches))
        content = content.replace("{{ exposure_grand_total }}", metrics["exposure_total"])
        
        # Adaptive Dossier Evidence
        ev1 = breaches[0]['Name'] if len(breaches) > 0 else "Análisis Google"
        ev2 = breaches[1]['Name'] if len(breaches) > 1 else "Malware Intelligence"
        content = content.replace("{{ dossier_source_1 }}", ev1)
        content = content.replace("{{ dossier_source_2 }}", ev2)
        
        # Static placeholders for Phase labels
        content = content.replace("{{ closing_phase_1_label }}", "24 Horas")
        content = content.replace("{{ closing_phase_2_label }}", "72 Horas")
        content = content.replace("{{ closing_phase_3_label }}", "30 Días")
        content = content.replace("{{ password_example }}", "K3yp@ss#2026!")

        # 5. Saving (Raw Parity)
        raw_path = os.path.join(report_dir, "raw", f"{base_filename}.html")
        pdf_path = os.path.join(report_dir, "PDF", f"{base_filename}.pdf")
        
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] RAW HTML saved: {raw_path}")

        # 6. PDF Rendering
        print("[*] Rendering PDF...")
        self.pdf_renderer.render_from_html_file(raw_path, pdf_path)
        print(f"[+] FINAL PDF generated: {pdf_path}")

if __name__ == "__main__":
    orchestrator = ReportOrchestrator()
    orchestrator.run_analysis("Felipe de Jesus Miramontes Romero", "felipemiramontesr@gmail.com")
