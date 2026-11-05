# Deployment Guide

## Prerequisites

- Microsoft Fabric workspace backed by Fabric capacity or trial
- Contributor or higher workspace access
- Lakehouse support
- Power BI semantic-model and report-creation permissions
- Azure subscription only if enabling the future Document Intelligence extension

## Fabric deployment

1. Create workspace `Healthcare-Intelligence-Demo`.
2. Create Lakehouse `HealthcareIntelligenceLH`.
3. Create `Files/bronze`.
4. Upload the five CSV files from `samples/data`.
5. Create notebook `NB_Healthcare_Bronze_Load` and attach the Lakehouse as default.
6. Run notebook sources in numeric order.
7. Confirm all expected row counts.
8. Create a semantic model containing only the three Gold tables.
9. Add relationships and measures from `fabric/power-bi`.
10. Build the two report pages.
