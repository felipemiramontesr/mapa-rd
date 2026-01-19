
import os

html_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-V2-PRINT.html"
css_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\theme\report.print.css"

inaction_html = """
    <!-- PAGE: INACTION SCENARIO (Latency Trap) -->
    <div class="pdf-page inaction-page">

        <div class="vector-global-header">
            <h2>Escenario de Inacción</h2>
            <p>La Trampa de Latencia: Por qué "no ha pasado nada" no significa seguridad</p>
        </div>

        <div class="inaction-container">
            <!-- Timeline Flow -->
            <div class="inaction-grid">

                <!-- PHASE 1: THE PAST (Luck) -->
                <div class="inaction-card phrase-past">
                    <div class="inaction-header">
                        <div class="inaction-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <circle cx="12" cy="12" r="14" />
                                <polyline points="12 6 12 12 16 14" />
                            </svg>
                        </div>
                        <div class="inaction-title">DEUDA HISTÓRICA</div>
                    </div>
                    <div class="inaction-body">
                        <h4 class="highlight-text">"14 años sin incidentes"</h4>
                        <p>Esto no es seguridad, es <strong>Suerte Operativa</strong>. La seguridad por oscuridad
                            funcionaba cuando los ataques eran manuales y dirigidos.</p>
                    </div>
                    <div class="inaction-footer">
                        <span>Estado:</span> <span class="status-badge status-luck">OBSOLETO</span>
                    </div>
                </div>

                <!-- ARROW CONNECTOR -->
                <div class="inaction-connector">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                </div>

                <!-- PHASE 2: THE PRESENT (Visibility) -->
                <div class="inaction-card phrase-present">
                    <div class="inaction-header">
                        <div class="inaction-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                <circle cx="12" cy="12" r="3" />
                            </svg>
                        </div>
                        <div class="inaction-title">NUEVA VISIBILIDAD</div>
                    </div>
                    <div class="inaction-body">
                        <h4 class="highlight-text">Automatización & IA</h4>
                        <p>Hoy, escáneres masivos y bots de IA encuentran vulnerabilidades en segundos. Lo que antes era
                            invisible, ahora es un <strong>blanco automático</strong>.</p>
                    </div>
                    <div class="inaction-footer">
                        <span>Estado:</span> <span class="status-badge status-warning">EXPUESTO</span>
                    </div>
                </div>

                <!-- ARROW CONNECTOR -->
                <div class="inaction-connector">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                </div>

                <!-- PHASE 3: THE FUTURE (Collapse) -->
                <div class="inaction-card phrase-future">
                    <div class="inaction-header">
                        <div class="inaction-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path
                                    d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                                <line x1="12" y1="9" x2="12" y2="13" />
                                <line x1="12" y1="17" x2="12.01" y2="17" />
                            </svg>
                        </div>
                        <div class="inaction-title">COLAPSO INEVITABLE</div>
                    </div>
                    <div class="inaction-body">
                        <h4 class="highlight-text">Costo Exponencial</h4>
                        <p>Sistemas legados sin soporte no se pueden parchar. Una brecha hoy obliga a una
                            <strong>reconstrucción total</strong> (10x costo) en lugar de remediación.
                        </p>
                    </div>
                    <div class="inaction-footer">
                        <span>Estado:</span> <span class="status-badge status-critical">CRÍTICO</span>
                    </div>
                </div>

            </div>
        </div>

        <!-- Manual Footer -->
        <div
            style="position: absolute; bottom: 1.0cm; left: 1.0cm; font-size: 10px; color: rgba(255, 255, 255, 0.4); font-family: 'Inter', sans-serif;">
            Sin auditorías genéricas. Sin promesas vacías.
        </div>
    </div>
"""

inaction_css = """
/* --- INACTION SCENARIO (LATENCY TRAP) --- */
.inaction-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    height: 100vh;
    page-break-after: always;
}

.inaction-container {
    width: 100%;
    max-width: 1000px;
    margin-top: 5rem;
    display: flex;
    justify-content: center;
}

.inaction-grid {
    display: flex;
    flex-direction: row;
    align-items: stretch; /* EQUAL HEIGHT FIXED HERE */
    justify-content: space-between;
    width: 100%;
    gap: 1.5rem;
}

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
}

.inaction-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 1.5rem;
    min-height: 160px;
    justify-content: flex-start;
}

.inaction-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    border: 3px solid;
    background: rgba(0, 0, 0, 0.3);
}

.inaction-icon svg {
    width: 40px;
    height: 40px;
}

.inaction-title {
    font-size: 0.9rem;
    font-weight: 800;
    text-transform: none;
    letter-spacing: 0.15em;
    color: rgba(255,255,255,0.9);
    text-align: center;
    white-space: nowrap;
}

.inaction-body {
    flex: 1;
    width: 100%;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 1rem;
}

.inaction-body h4.highlight-text {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    line-height: 1.3;
    width: 100%;
    min-height: 3.9rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.inaction-body p {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.85);
    line-height: 1.6;
    max-width: 90%;
}

.inaction-footer {
    width: 100%;
    margin-top: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
    padding-top: 1rem;
    padding-bottom: 0.5rem;
    gap: 0.5rem;
    min-height: 50px;
}

.status-badge {
    padding: 0.4rem 1rem;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.8rem;
    color: #000;
}

/* PHASES styling */
.phrase-past { border-top: 4px solid #facc15; }
.phrase-past .inaction-icon { color: #facc15; border-color: #facc15; box-shadow: 0 0 15px rgba(250, 204, 21, 0.2); }
.phrase-past .highlight-text { color: #facc15; }
.status-luck { background: #facc15; }

.phrase-present { border-top: 4px solid #fb923c; }
.phrase-present .inaction-icon { color: #fb923c; border-color: #fb923c; box-shadow: 0 0 15px rgba(251, 146, 60, 0.2); }
.phrase-present .highlight-text { color: #fb923c; }
.status-warning { background: #fb923c; }

.phrase-future { border-top: 4px solid #ef4444; }
.phrase-future .inaction-icon { color: #ef4444; border-color: #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.2); }
.phrase-future .highlight-text { color: #ef4444; }
.status-critical { background: #ef4444; color: #fff; }

.inaction-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.3);
    width: 50px;
}
.inaction-connector svg {
    width: 32px;
    height: 32px;
}
"""

# Apply HTML Patch
try:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if "Escenario de Inacción" in html_content:
        print("HTML already contains Inaction section. Skipping append.")
    else:
        # Insert before </body>
        if "</body>" in html_content:
            new_html = html_content.replace("</body>", inaction_html + "\n</body>")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print("HTML Inaction section appended.")
        else:
            print("Could not find </body> tag in HTML.")
            
except Exception as e:
    print(f"Error HTML: {e}")

# Apply CSS Patch
try:
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
        
    # Check if we need to append. 
    # Since we saw it had messy definitions, maybe appending is risky if precedence is an issue.
    # But usually last rule wins.
    
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write("\n" + inaction_css)
    print("CSS Inaction styles appended.")
        
except Exception as e:
    print(f"Error CSS: {e}")
