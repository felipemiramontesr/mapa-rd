"""
MAPA-RD: Intelligence Data Deduplicator
---------------------------------------
Author: Antigravity AI / Senior Python standards
Version: 2.1.0 (Pro)

Purpose:
    Ensures data integrity by filtering out redundant events captured during 
    multi-source intelligence gathering.

Technique:
    Uses a 'Seen IDs' set for O(1) lookup time, resulting in O(n) total 
    complexity. This is the gold standard for large-scale OSINT datasets.
"""

import logging
from typing import List, Dict, Any, Set

# Local logger setup
logger = logging.getLogger(__name__)

class Deduper:
    """Removes redundant information from scanned data.
    
    Ensures that each unique indicator is only processed once in the pipeline,
    preventing duplicate alerts and cleaning up the final report.
    """

    def deduplicate(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out findings with duplicate IDs based on finding_id.
        
        This method preserves the original order of findings (First-seen wins).
        
        Args:
            findings: A list of normalized finding dictionaries.
            
        Returns:
            A list containing only the first occurrence of each unique finding.
        """
        # ---------------------------------------------------------
        # INITIALIZATION
        # We use a Set for 'seen_ids' because lookups are nearly instantaneous.
        # ---------------------------------------------------------
        seen_ids: Set[str] = set()
        unique_findings: List[Dict[str, Any]] = []
        
        initial_count = len(findings)
        logger.debug(f"Starting deduplication of {initial_count} items.")
        
        # ---------------------------------------------------------
        # PROCESSING LOOP
        # ---------------------------------------------------------
        for finding in findings:
            # Finding ID is a SHA-256 determined by Normalizer
            fid = finding.get('finding_id')
            
            # Logic: If we haven't seen this ID, it's new. Track and Keep.
            if fid and fid not in seen_ids:
                seen_ids.add(fid)
                unique_findings.append(finding)
            else:
                # Log redundancy for debugging if needed
                pass
                
        final_count = len(unique_findings)
        logger.info(f"Deduplication finished. Removed {initial_count - final_count} redundant findings.")
        
        return unique_findings
