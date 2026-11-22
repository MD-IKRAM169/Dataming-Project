# Study 1 — Supervised Learning

**Primary evidence:** [Supervised.docx](../Supervised.docx). This document summarizes the original coursework, not a new model or a clinical evaluation.

## Dataset and objective

The UCI **Echocardiogram** dataset was used in WEKA for a classification exercise involving one-year survival after heart attack. The source report gives **132 instances**, **13 attributes**, and missing values. It defines the label **alive_at_1** using survival duration and patient status. Features described include age, pericardial effusion, fractional shortening, E-point septal separation, left-ventricular dimensions, wall-motion metrics, and metadata fields.

## Historical comparison

The report lists five WEKA classifiers: **Naive Bayes**, **LMT (Logistic Model Trees)**, **AttributeSelectedClassifier**, **LWL (Locally Weighted Learning)**, and **VotedPerceptron**. The output reports **10-fold cross-validation**, and the final discussion selects AttributeSelectedClassifier, citing **97.3%** correctly classified instances. This score is a historical claim; the original experiment has not been independently reproduced here.

The output shows **74 known-label evaluated cases** and **58 unknown-class cases excluded from evaluation** out of 132. For example, Naive Bayes is reported at **71/74 (95.9459%)**, and VotedPerceptron at **69/74 (93.2432%)**. Do not present headline accuracy as the result for all 132 rows.

## Possible target leakage

The label **alive_at_1** is derived from survival and life-status fields. Those fields appear in the input attribute listing. If used as predictors, they could supply target-defining information to the learner. The exact AttributeSelectedClassifier settings and excluded predictors have not been independently verified; this is a **risk requiring inspection**, not proof that the experiment was rerun incorrectly.

Missing data, limited known-label sample size, selection bias, and absent external testing also constrain interpretation. These figures are **not** clinically validated survival predictions.

## Reproducibility

A faithful rerun needs the historic dataset and label conventions, original WEKA version/configuration, complete preprocessing settings, exact fold assignments, and a leakage-safe feature definition. See [Reproducibility](REPRODUCIBILITY.md). The [new Python demo](../examples/synthetic_demo.py) operates on completely generated data and is **not** that rerun.
