# Ethics, privacy, and methodological limitations

This historical portfolio includes medical-outcome classification and workplace-absence clustering. These are sensitive domains, and neither the original reports nor the new demonstration should be deployed for clinical or employment decisions.

## Medical classification

- The historic results are not evidence of independently validated prognosis, diagnosis or treatment.
- The one-year survival label is derived from fields also listed among inputs. **Target leakage** must be ruled out by reviewing the original WEKA settings.
- Distinguish **132 total rows**, **74 evaluated known-class rows** and **58 ignored unknown-class rows**.
- Missing values, sample selection, small evaluated sample and lack of external validation limit accuracy claims.
- Any name/personal identifiers must be removed from public modeling features and restricted where required.

## Workplace clustering

- The 12 historical clusters are exploratory groupings, not worker ratings or forecasts.
- Employee **ID** should not be used as a numerical clustering variable.
- Using absenteeism-hours as an input undermines interpreting cluster assignment as a prediction of that same quantity.
- ICD and other categorical codes require suitable treatment rather than assuming continuous Euclidean distances.
- Check cluster stability and fairness before any group-level interpretation; do not profile individuals.

## Permissions and provenance

The public Word documents contain historical coursework metadata and discuss externally sourced datasets. Review the documents for academic identifiers, third-party rights, and reproduction restrictions. Public availability does not equal permission to redistribute sensitive underlying records. This update distributes **no original patient or employee dataset**, and it assigns no new license to the 2020 reports.

The Python examples are solely **educational synthetic-data workflows**.
