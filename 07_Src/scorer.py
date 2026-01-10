import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'scoring_rules_v1.json')

class Scorer:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self):
        if not os.path.exists(CONFIG_PATH):
            # Fallback simple rules if file missing
            return {"rules": []}
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)

    def calculate_score(self, finding):
        """
        Determines P0-P3 score based on specific production-grade risk logic.
        """
        category = finding.get('category')
        entity = finding.get('entity')
        data = str(finding.get('value', '')).lower()
        
        # Default
        score = "P3"
        rationale = "Información pública de bajo impacto."

        # Category/Entity Overrides
        if category == "Data Leak" or entity == "Compromised Credentials":
            score = "P0"
            rationale = "CRÍTICO: Credenciales o datos privados expuestos en filtración."
        elif category == "Threat":
            score = "P1"
            rationale = "ALTO: Asociación con infraestructura maliciosa o listas negras."
        elif entity == "Squatted/Similar Domain":
            score = "P2"
            rationale = "MEDIO: Posible campaña de suplantación detected."
            
        # Contextual/Keyword Overrides (Critical Value)
        if "banorte" in data:
            score = "P0"
            rationale = f"CRÍTICO: Hallazgo vinculado a Institución Financiera (Banorte). Valor: {data[:30]}..."
        elif "password" in data or "contraseña" in data:
            score = "P0"
            rationale = "CRÍTICO: Palabra clave sensible detected (Password/Contraseña)."

        finding['risk_score'] = score
        finding['risk_rationale'] = rationale
        return finding

        finding['risk_score'] = score
        finding['risk_rationale'] = rationale
        return finding
        
    def score_findings(self, findings):
        scored = []
        for f in findings:
            scored.append(self.calculate_score(f))
        return scored
