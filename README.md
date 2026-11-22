# Data Mining Coursework — Supervised & Unsupervised Learning

[![Validation and examples](https://github.com/MD-IKRAM169/Dataming-Project/actions/workflows/verify.yml/badge.svg)](https://github.com/MD-IKRAM169/Dataming-Project/actions/workflows/verify.yml)

**WEKA · Classification · Clustering · UCI Machine Learning Repository · Research documentation**

This repository presents two original academic data-mining reports from 2020: supervised analysis of the **Echocardiogram** dataset and unsupervised analysis of the **Absenteeism at Work** dataset. The reports are preserved unchanged. New documentation, quality checks and synthetic-data Python demonstrations make the work easier to understand without claiming to reproduce its historic results.

> **Provenance:** The Word documents are the original academic deliverables. The Python code, tests and documentation are **new portfolio improvements**, not original WEKA implementations. No original patient or employee records are included.

## Original coursework

| Report | Dataset | WEKA methods | Historical scope |
|---|---|---|---|
| [Supervised learning](Supervised.docx) | UCI Echocardiogram | Naive Bayes, LMT, AttributeSelectedClassifier, LWL, VotedPerceptron | 132 rows; 13 fields; 74 evaluated known class labels |
| [Unsupervised learning](Unsupervised%20Learning.docx) | UCI Absenteeism at Work | K-means, EM, HierarchicalClusterer | 740 records; 21 attributes; 12 reported clusters |

Read the detailed [supervised study](docs/SUPERVISED_STUDY.md), [unsupervised study](docs/UNSUPERVISED_STUDY.md), [data sources](docs/DATA_SOURCES.md), and [research limitations](docs/ETHICS_AND_LIMITATIONS.md).

## Reported findings — interpreted carefully

**Supervised:** The report identifies **AttributeSelectedClassifier** as its strongest model, claiming approximately **97.3% correctly classified instances** in WEKA ten-fold cross-validation. However, the outputs show **74 evaluated records** and **58 ignored unknown-class records** out of 132 total, so the percentage is **not** a verified result for all 132 patients. Additionally, the target is derived from survival-related fields listed among the attributes; these may create **target leakage** if included as predictors. No model has been independently rerun or clinically validated.

**Unsupervised:** The report describes preprocessing in WEKA 3.8.3, comparing K-means, expectation maximization, and hierarchical clustering, with a chosen **12-cluster** hierarchical solution. The run lists 740 instances, 21 attributes and training-data evaluation. Identifier and absenteeism-duration features may influence the distances, so the clusters should not be described as predictions of future absence or as personnel evaluation tools.

## Study workflow

- **Echocardiogram:** UCI dataset → WEKA supervised classification → five classifier comparisons → reported 10-fold CV results.
- **Absenteeism at Work:** UCI dataset → WEKA missing-value preprocessing → three clustering approaches → reported 12 clusters.
- **New Python examples (separate):** generated classification/blobs data → modern sklearn pipelines and clustering metrics → isolated tests.

## Reproduce the independent synthetic examples

Requirements: Python 3.11 or newer. These demonstrations **never load patient or employee data**.

~~~bash
python -m pip install -r requirements-demo.txt
python -m examples.synthetic_demo supervised
python -m examples.synthetic_demo unsupervised
python -m examples.synthetic_demo all
python -m unittest discover -s tests -v
~~~

Verify the two historical Word documents (read-only):

~~~bash
python tools/check_reports.py Supervised.docx "Unsupervised Learning.docx"
~~~

[GitHub Actions](.github/workflows/verify.yml) runs the checks on every pull request. The synthetic results are **not replications** of the historical WEKA outputs.

## Repository structure

~~~text
├── Supervised.docx                   # Original report, unchanged
├── Unsupervised Learning.docx        # Original report, unchanged
├── README.md
├── docs/
│   ├── SUPERVISED_STUDY.md
│   ├── UNSUPERVISED_STUDY.md
│   ├── DATA_SOURCES.md
│   ├── REPRODUCIBILITY.md
│   ├── ETHICS_AND_LIMITATIONS.md
│   └── PORTFOLIO_CHECKLIST.md
├── examples/synthetic_demo.py       # NEW synthetic-data demonstration
├── tools/check_reports.py           # Read-only DOCX inspection
├── tests/                            # Ten unit tests
├── requirements-demo.txt
└── .github/workflows/verify.yml
~~~

## Responsible use and attribution

The supervised report analyzes a sensitive medical outcome and is **not** a clinical prediction or decision-support tool. Workplace clustering is **not** appropriate for scoring individual workers. Check the original documents for personal academic identifiers and third-party redistribution conditions before sharing publicly. No license has been assigned to the historical reports.

**Maintainer:** [MD-IKRAM169](https://github.com/MD-IKRAM169)
