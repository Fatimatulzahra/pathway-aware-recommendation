import unittest

from recommend import OpportunityRecommender


class RecommendationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Small controlled examples with clearly different subjects.
        cls.model = OpportunityRecommender([
            {
                "id": "hardware",
                "title": "Embedded Firmware Intern",
                "org": "Example Hardware",
                "description": "Program microcontrollers and FPGA hardware.",
                "requirements": "C++ and electronics",
            },
            {
                "id": "design",
                "title": "UX Research Intern",
                "org": "Example Design",
                "description": "Study usability and interaction design.",
                "requirements": "User research and accessibility",
            },
            {
                "id": "data",
                "title": "Data Analyst Intern",
                "org": "Example Analytics",
                "description": "Analyze statistics and build dashboards.",
                "requirements": "SQL and visualization",
            },
        ])

    def test_relevant_opportunity_ranks_first(self):
        cases = [
            ("firmware microcontrollers FPGA", "hardware"),
            ("usability accessibility", "design"),
            ("SQL statistics", "data"),
        ]
        for method in ["keyword", "tfidf"]:
            for query, expected_id in cases:
                with self.subTest(method=method, query=query):
                    results = self.model.recommend(query, method, k=3)
                    self.assertEqual(results[0]["id"], expected_id)

    def test_unknown_terms_return_no_matches(self):
        for method in ["keyword", "tfidf"]:
            self.assertEqual(
                self.model.recommend("zzzxxyy", method),
                [],
            )

    def test_empty_query_is_rejected(self):
        for method in ["keyword", "tfidf"]:
            with self.assertRaises(ValueError):
                self.model.recommend("the and", method)

    def test_k_limits_results(self):
        for method in ["keyword", "tfidf"]:
            results = self.model.recommend("intern", method, k=2)
            self.assertEqual(len(results), 2)
            self.assertEqual(len({r["id"] for r in results}), 2)

    def test_results_are_repeatable(self):
        for method in ["keyword", "tfidf"]:
            first = self.model.recommend("intern", method)
            second = self.model.recommend("intern", method)
            self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()