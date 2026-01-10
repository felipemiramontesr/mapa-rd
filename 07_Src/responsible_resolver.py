class ResponsibleResolver:
    def __init__(self):
        # Database of known entities
        self.responsibles = {
            "Google": {
                "name": "Google México, S. de R.L. de C.V.",
                "address": "Montes Urales 445, Lomas de Chapultepec, CDMX",
                "email": "arco@google.com" # Placeholder
            },
            "LinkedIn": {
                "name": "LinkedIn Corporation",
                "address": "Sunnyvale, CA, USA (Representation in MX via Microsoft)",
                "email": "privacy@linkedin.com"
            },
            "Facebook": {
                "name": "Meta Platforms, Inc.",
                "address": "Menlo Park, CA",
                "email": "privacy@facebook.com"
            }
        }

    def resolve(self, finding):
        source = finding.get('source_name')
        # Simple lookup
        responsible = self.responsibles.get(source, {
            "name": "Unknown Entity",
            "address": "Unknown Address",
            "email": "contact@domain.com"
        })
        
        finding['responsible_party'] = responsible
        return finding

    def resolve_findings(self, findings):
        resolved = []
        for f in findings:
            resolved.append(self.resolve(f))
        return resolved
