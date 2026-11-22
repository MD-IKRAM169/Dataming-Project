"""Independent modern demos on generated data; NOT the historical WEKA studies.

Run with:
    python -m examples.synthetic_demo supervised
    python -m examples.synthetic_demo unsupervised
    python -m examples.synthetic_demo all

No patient, medical, employee, or identifying data are loaded or saved.
"""
from __future__ import annotations

import argparse
import json
from typing import Any

import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_classification
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.mixture import GaussianMixture
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42


def supervised_example() -> dict[str, Any]:
    """Illustrate leakage-conscious preprocessing within stratified cross-validation."""
    X, y = make_classification(
        n_samples=240, n_features=12, n_informative=6, n_redundant=2,
        n_classes=2, weights=[0.65, 0.35], class_sep=0.9, random_state=SEED,
    )
    rng = np.random.default_rng(SEED)
    X = X.copy()
    X[rng.random(X.shape) < 0.04] = np.nan
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    estimators = {
        "GaussianNB": GaussianNB(),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=SEED),
    }
    models = {}
    for name, estimator in estimators.items():
        # Imputation and scaling are FIT inside each train fold, not globally.
        pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), estimator)
        evaluation = cross_validate(
            pipeline, X, y, cv=folds,
            scoring={"balanced_accuracy": "balanced_accuracy", "f1": "f1"},
            n_jobs=1,
        )
        models[name] = {
            "mean_balanced_accuracy": round(
                float(np.mean(evaluation["test_balanced_accuracy"])), 4
            ),
            "mean_f1": round(float(np.mean(evaluation["test_f1"])), 4),
        }
    return {
        "data": "generated classification data only",
        "rows": len(X), "features": X.shape[1], "cv_folds": 5,
        "models": models,
        "disclaimer": "Educational synthetic demo; not a clinical or historical result",
    }


def unsupervised_example() -> dict[str, Any]:
    """Compare three clustering algorithms on generated blobs with known reference labels."""
    X, generating_labels = make_blobs(
        n_samples=300, n_features=5, centers=3, cluster_std=1.15,
        random_state=SEED,
    )
    scaled = StandardScaler().fit_transform(X)
    algorithms = {
        "KMeans": KMeans(n_clusters=3, n_init=10, random_state=SEED),
        "GaussianMixture": GaussianMixture(n_components=3, random_state=SEED),
        "HierarchicalAverage": AgglomerativeClustering(
            n_clusters=3, linkage="average"
        ),
    }
    models = {}
    for name, algorithm in algorithms.items():
        assigned = algorithm.fit_predict(scaled)
        models[name] = {
            "clusters": len(np.unique(assigned)),
            "silhouette": round(float(silhouette_score(scaled, assigned)), 4),
            "adjusted_rand_index": round(
                float(adjusted_rand_score(generating_labels, assigned)), 4
            ),
        }
    return {
        "data": "generated blobs with artificial reference groups",
        "rows": len(X), "features": X.shape[1],
        "models": models,
        "disclaimer": (
            "ARI is available only because artificial generating labels are known; "
            "not historical WEKA results or workplace evaluations"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode", nargs="?", choices=["supervised", "unsupervised", "all"],
        default="all",
    )
    args = parser.parse_args(argv)
    output: dict[str, Any] = {
        "note": "All data are synthetic; results do not reproduce coursework."
    }
    if args.mode in ("supervised", "all"):
        output["supervised"] = supervised_example()
    if args.mode in ("unsupervised", "all"):
        output["unsupervised"] = unsupervised_example()
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
