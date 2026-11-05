# Governed Health Assistant: Future Phase

## Supported intents

- Explain a parameter in simple language
- Show results outside supplied laboratory ranges
- Compare current and previous results
- Summarize an imaging observation using source wording
- Identify findings to discuss with a qualified healthcare professional

## Mandatory guardrails

- Authenticate the user.
- Resolve authorized PatientID values before querying data.
- Return source report, screening date, parameter, value, unit, and supplied range.
- Never diagnose, prescribe, change medication, or invent missing values.
- Label extracted observations separately from validated clinical interpretation.
- Include an appropriate clinical-review statement.
