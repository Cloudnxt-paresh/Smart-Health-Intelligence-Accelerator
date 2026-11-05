# Power BI Build Guide

## Semantic model

Include only:

- `gold_patient_results`
- `gold_screening_summary`
- `gold_clinical_observations`

Create relationships:

1. `gold_screening_summary[ScreeningID]` (1) -> `gold_patient_results[ScreeningID]` (*)
2. `gold_screening_summary[ScreeningID]` (1) -> `gold_clinical_observations[ScreeningID]` (*)

Use single-direction filtering from summary to detail and keep both relationships active.

## Page 1: Patient Health Overview

Slicers:

- `gold_screening_summary[PatientName]`
- `gold_screening_summary[ScreeningDate]`

Cards:

- Total Parameters
- Within Range
- High Results
- Low Results

Abnormal results table:

- ParameterName
- MeasuredValue
- Unit
- ReferenceLow
- ReferenceHigh
- StatusDisplay

Visual filter: `IsOutsideRange = 1`.

Category chart:

- Axis: TestCategory
- Value: Count of ParameterCode

## Page 2: Historical Health Trends

- Patient slicer: PatientName
- Parameter slicer: ParameterName
- Line chart: TestDate by Average of MeasuredValue
- Example: Aarav Sharma, HbA1c = 5.3 -> 5.8 -> 6.2
