import json
import os
from typing import List, Dict, Any, Optional

# Configuration path for scoring rules
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '03_Config', 'scoring_rules.json')

class Scorer:
    """Evaluates the risk level of normalized findings.
    
    Assigns a priority score (P0 to P3) based on category, entity type,
    and sensitive keywords found in the data values.
    """

    def __init__(self, rules_path: str = CONFIG_PATH):
        """Initialize the Scorer with specific risk rules."""
        self.rules: Dict[str, Any] = self._load_rules(rules_path)

    def _load_rules(self, path: str) -> Dict[str, Any]:
        """Load external scoring rules or use internal defaults."""
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"rules": []}

    def calculate_score(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the P0-P3 risk score for a single finding.
        
        Logic:
            P0 (Critical): Identity theft, data leaks, or financial links.
            P1 (High): Malicious associations or infrastructure threats.
            P2 (Medium): Impersonation risks (Squatting).
            P3 (Low): General public footprint.
            
        Args:
            finding: A normalized finding dictionary.
            
        Returns:
            The finding dictionary updated with risk_score and risk_rationale.
        """
        category = finding.get('category')
        entity = finding.get('entity')
        value_lower = str(finding.get('value', '')).lower()
        
        # 1. Default Baseline (Low Risk)
        score = "P3"
        rationale = "Información pública de bajo impacto."

        # 2. Category/Entity Logic
        if category == "Data Leak" or entity == "Compromised Credentials":
            score = "P0"
            rationale = "CRÍTICO: Credenciales o datos privados expuestos en filtración."
        elif category == "Threat":
            score = "P1"
            rationale = "ALTO: Asociación con infraestructura maliciosa o listas negras."
        elif entity == "Squatted/Similar Domain":
            score = "P2"
            rationale = "MEDIO: Posible campaña de suplantación detectada."
            
        # 3. Contextual Keyword Sensitivity (Financial/Security focus)
        critical_keywords = ["banorte", "bbva", "santander", "password", "contraseña", "token", "cvv"]
        for kw in critical_keywords:
            if kw in value_lower:
                score = "P0"
                rationale = f"CRÍTICO: Palabra clave sensible o vínculo financiero detectado ({kw})."
                break

        finding['risk_score'] = score
        finding['risk_rationale'] = rationale
        return finding
        
    def score_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of findings through the scoring engine.
        
        Args:
            findings: List of normalized findings.
            
        Returns:
            List of scored findings.
        """
        return [self.calculate_score(f) for f in findings if f]
