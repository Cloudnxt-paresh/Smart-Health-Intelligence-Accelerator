# Optional Azure Infrastructure

The core POC runs in Microsoft Fabric and does not require this template.

The Bicep template optionally creates Azure AI Document Intelligence for a later PDF/scanned-report ingestion phase.

```bash
az group create --name rg-smart-health-intelligence-dev --location centralindia
az deployment group create \
  --resource-group rg-smart-health-intelligence-dev \
  --template-file infra/main.bicep \
  --parameters environmentName=dev deployDocumentIntelligence=true
```
