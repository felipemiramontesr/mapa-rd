import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Src'))

from clusterer import Clusterer
from responsible_resolver import ResponsibleResolver
from arco_generator import ArcoGenerator

class TestClusterer(unittest.TestCase):
    def test_cluster_by_category(self):
        findings = [
            {"category": "Leak", "id": 1},
            {"category": "Leak", "id": 2},
            {"category": "Threat", "id": 3}
        ]
        results = Clusterer().cluster_by_category(findings)
        self.assertEqual(len(results["Leak"]), 2)
        self.assertEqual(len(results["Threat"]), 1)

class TestResponsibleResolver(unittest.TestCase):
    def test_resolve_known(self):
        resolver = ResponsibleResolver()
        finding = {"source_name": "Facebook", "value": "test"}
        enriched = resolver.resolve(finding)
        self.assertEqual(enriched['responsible_party']['name'], "Meta Platforms, Inc.")

    def test_resolve_unknown(self):
        resolver = ResponsibleResolver()
        finding = {"source_name": "UnknownSource", "value": "test"}
        enriched = resolver.resolve(finding)
        self.assertEqual(enriched['responsible_party']['name'], "Unknown Entity")

class TestArcoGenerator(unittest.TestCase):
    def setUp(self):
        # We need to mock the template loading since it reads a file
        # Or ensure the template file exists. 
        # Given the previous context, we know templates exist in 08_Templates.
        pass

    def test_init_loads_template(self):
        # This test acts as an integration test verifying the template exists
        try:
            gen = ArcoGenerator()
            self.assertTrue(len(gen.template) > 0)
        except Exception as e:
            self.fail(f"ArcoGenerator init failed: {e}")

if __name__ == '__main__':
    unittest.main()
