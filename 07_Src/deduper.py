class Deduper:
    def __init__(self):
        pass

    def deduplicate(self, findings):
        """
        Removes duplicate findings based on finding_id.
        """
        seen_ids = set()
        unique_findings = []
        
        for finding in findings:
            fid = finding.get('finding_id')
            if fid not in seen_ids:
                seen_ids.add(fid)
                unique_findings.append(finding)
                
        return unique_findings
