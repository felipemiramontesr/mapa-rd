class Clusterer:
    def __init__(self):
        pass

    def cluster_by_category(self, findings):
        clusters = {}
        for finding in findings:
            cat = finding.get('category', 'Uncategorized')
            if cat not in clusters:
                clusters[cat] = []
            clusters[cat].append(finding)
        return clusters

    def cluster_by_entity_type(self, findings):
        clusters = {}
        for finding in findings:
            etype = finding.get('entity', 'Unknown')
            if etype not in clusters:
                clusters[etype] = []
            clusters[etype].append(finding)
        return clusters
