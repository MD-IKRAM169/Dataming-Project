"""Tests for independent generated-data examples, not historical WEKA models."""
from __future__ import annotations

import unittest
from examples.synthetic_demo import supervised_example, unsupervised_example


class SyntheticDataDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.supervised = supervised_example()
        cls.unsupervised = unsupervised_example()

    def test_supervised_has_expected_shape(self) -> None:
        item = self.supervised
        self.assertEqual(item["rows"], 240)
        self.assertEqual(item["features"], 12)
        self.assertEqual(item["cv_folds"], 5)
        self.assertIn("synthetic", item["disclaimer"].lower())

    def test_supervised_metrics_are_bounded(self) -> None:
        models = self.supervised["models"]
        self.assertEqual(set(models), {"GaussianNB", "LogisticRegression"})
        for scores in models.values():
            for score in scores.values():
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)

    def test_unsupervised_compares_three_algorithms(self) -> None:
        models = self.unsupervised["models"]
        self.assertEqual(
            set(models), {"KMeans", "GaussianMixture", "HierarchicalAverage"}
        )
        for metrics in models.values():
            self.assertEqual(metrics["clusters"], 3)
            self.assertGreaterEqual(metrics["silhouette"], -1)
            self.assertLessEqual(metrics["silhouette"], 1)
            self.assertGreaterEqual(metrics["adjusted_rand_index"], -1)
            self.assertLessEqual(metrics["adjusted_rand_index"], 1)

    def test_only_synthetic_data_used(self) -> None:
        self.assertIn("generated", self.supervised["data"])
        self.assertIn("generated", self.unsupervised["data"])
        self.assertNotIn("echocardiogram", str(self.supervised).lower())
        self.assertNotIn("absenteeism", str(self.unsupervised).lower())
