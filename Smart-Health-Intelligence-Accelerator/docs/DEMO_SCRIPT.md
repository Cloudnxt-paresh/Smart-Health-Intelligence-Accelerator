# 90-second Demo Script

This is Smart Health Intelligence, a Microsoft Fabric proof of concept for preventive healthcare screening.

Diagnostic information is often fragmented across blood tests, cardiac reports, imaging findings, and multiple screening dates. The solution creates a governed analytical path in Microsoft Fabric. Synthetic data lands in OneLake and a Fabric Lakehouse, then moves through Bronze, Silver, and Gold Delta layers. Silver independently validates each result against the reference range supplied with that laboratory record. In this demo, all 576 imported statuses passed validation.

Power BI provides an interactive patient view through a Direct Lake semantic model. For Aarav Sharma's synthetic October 2026 screening, 32 parameters are available: 29 within the supplied ranges, 2 high, and 1 low. The platform also supports longitudinal analysis, with synthetic HbA1c values of 5.3, 5.8, and 6.2 percent across three screenings.

The next phase adds Azure AI Document Intelligence for reports and a governed AI assistant with source traceability and clinical safeguards. All information is synthetic and not intended for clinical decision-making.
