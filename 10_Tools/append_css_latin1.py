
css_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\theme\report.print.css"

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

try:
    with open(css_path, 'a', encoding='latin-1') as f:
        f.write("\n" + inaction_css)
    print("CSS Inaction styles appended successfully (Latin-1).")
        
except Exception as e:
    print(f"Error CSS: {e}")
