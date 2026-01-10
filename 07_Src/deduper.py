from typing import List, Dict, Any, Set

class Deduper:
    """Removes redundant information from scanned data.
    
    Ensures that each unique indicator is only processed once in the pipeline,
    preventing duplicate alerts and cleaning up the final report.
    """

    def deduplicate(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out findings with duplicate IDs.
        
        Args:
            findings: A list of normalized finding dictionaries.
            
        Returns:
            A list containing only the first occurrence of each unique finding.
        """
        seen_ids: Set[str] = set()
        unique_findings: List[Dict[str, Any]] = []
        
        for finding in findings:
            fid = finding.get('finding_id')
            if fid and fid not in seen_ids:
                seen_ids.add(fid)
                unique_findings.append(finding)
                
        return unique_findings
