# Study 2 — Unsupervised Learning

**Primary evidence:** [Unsupervised Learning.docx](../Unsupervised%20Learning.docx). The figures below describe the historical WEKA output.

## Dataset

The report uses UCI **Absenteeism at Work** data to explore grouping of absence records. The WEKA result lists **740 instances** and **21 attributes**, including an employee ID, reason for absence (ICD categories where applicable), calendar features, commute details, demographics, workload, and **absenteeism hours**.

## Methods and results

The report describes preprocessing using **WEKA 3.8.3** and replacement of missing values with the most common value. It discusses **K-means**, **expectation maximization (EM)** and **hierarchical clustering**. A hierarchical model was selected with **12 clusters**. The reported scheme is:

~~~text
weka.clusterers.HierarchicalClusterer -N 12 -L MEAN -P -A "weka.core.EuclideanDistance -R first-last"
~~~

The run states **evaluation on training data**. The original counts are:

| Cluster | Records | Cluster | Records |
|---:|---:|---:|---:|
| 0 | 44 | 6 | 58 |
| 1 | 21 | 7 | 87 |
| 2 | 154 | 8 | 107 |
| 3 | 63 | 9 | 22 |
| 4 | 28 | 10 | 71 |
| 5 | 58 | 11 | 27 |

The counts sum to **740**, matching the reported instances. These are historical cluster sizes, not newly evaluated metrics.

## Interpretation and limitations

The original discussion associates some clusters with ICD-coded absence reasons. It should not be read as a causal statement that any medical condition determines all absence behavior.

The attributes include **ID** and **Absenteeism_time_in_hours**, and the WEKA distance range is **first-last**. If all were included, these variables may have directly influenced the clustering. It therefore cannot be described as a validated forecast of future absenteeism. Numeric ICD or other category codes also do not necessarily define meaningful continuous Euclidean distances. No independent cluster stability evaluation was included.

The new [synthetic Python clustering demo](../examples/synthetic_demo.py) has completely separate generated inputs and does not reproduce these reported clusters.
