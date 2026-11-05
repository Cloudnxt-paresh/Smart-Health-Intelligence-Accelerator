# Security

Do not commit real patient data, credentials, tenant IDs, connection strings, access tokens, or exported production reports.

This accelerator contains synthetic data only. For production deployments:

- Use Microsoft Entra ID and least-privilege Fabric workspace roles.
- Apply Power BI row-level security using an authorized user-to-patient mapping.
- Store diagnostic documents in governed storage and expose time-limited access only.
- Configure Microsoft Purview lineage, sensitivity labels, retention, and audit logging.
- Conduct a formal assessment for India's Digital Personal Data Protection Act, 2023 and applicable healthcare obligations.
- Require qualified clinical review for interpretations.

Report vulnerabilities privately to the repository owner. Do not create a public issue containing secrets or sensitive data.
