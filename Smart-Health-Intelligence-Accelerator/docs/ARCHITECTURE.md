# Reference Architecture

## Structured path

1. Synthetic CSV / Excel / JSON
2. Fabric Lakehouse `Files/bronze`
3. Bronze managed Delta tables
4. Silver standardization and deterministic status validation
5. Gold patient-result, screening-summary, and clinical-observation tables
6. SQL analytics endpoint
7. Direct Lake Power BI semantic model
8. Patient health overview and historical trends

## Document path: future phase

1. User uploads PDF or scanned diagnostic report
2. Entra-authorized application stores the document
3. Azure AI Document Intelligence extracts fields and narrative observations
4. Extraction output lands as JSON in the Bronze layer
5. Human validation is applied where required
6. Fabric processing continues through Silver and Gold

## AI path: future phase

A Copilot Studio or Fabric agent experience must:

- use only authorized patient data;
- cite the relevant source report and parameter;
- distinguish extracted facts from interpretation;
- never invent missing values;
- never diagnose or prescribe;
- recommend qualified clinical review for concerning findings.
