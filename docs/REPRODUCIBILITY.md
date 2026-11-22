# Reproducibility and provenance

## What exists historically

The original 2020 repository contains **Supervised.docx** and **Unsupervised Learning.docx**. Their analyses were described as WEKA workflows. The unsupervised report explicitly mentions **WEKA 3.8.3**. The repository did not include the original UCI data files, ARFF/CSV conversions, pipeline scripts, WEKA experiments, or fully specified runtime settings.

The original Word files are left unchanged. The README, documentation, checks and Python code are later portfolio work.

## Reproducing the supervised study

Acquire the appropriately licensed historic UCI Echocardiogram revision; track file hashes, labels, missing-value handling, filtering, and WEKA classifier settings. Verify the distinction between **132 records**, **74 evaluated labels** and **58 unknown-class rows**. Investigate the presence of survival and status predictors from which the label is constructed; do not report inflated target-leakage scores as valid prognosis. Use independent validation and report class-appropriate metrics.

## Reproducing the unsupervised study

Record the exact Absenteeism at Work file version and WEKA settings. Check inclusion of ID and absenteeism hours, normalization, treatment of categorical codes, missing-value replacement and clustering method. Reassess the 12-cluster selection with stability measures, not a single training-set partition.

## What can be run here

Requires Python 3.11+, numpy and scikit-learn:

~~~bash
python -m pip install -r requirements-demo.txt
python -m examples.synthetic_demo all
python -m unittest discover -s tests -v
~~~

These programs **only generate fictional data** and are **not replications of the 2020 experiments**. The classification example uses preprocessing inside stratified cross-validation; clustering metrics are computed on artificial blobs with known generating labels.

The two Word files are validated structurally without extracting their text:

~~~bash
python tools/check_reports.py Supervised.docx "Unsupervised Learning.docx"
~~~
