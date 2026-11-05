targetScope = 'resourceGroup'

@description('Azure region for the optional document extraction extension.')
param location string = resourceGroup().location

@description('Short environment name.')
@allowed(['dev', 'test', 'prod'])
param environmentName string = 'dev'

@description('Deploy optional Azure AI Document Intelligence.')
param deployDocumentIntelligence bool = false

var suffix = uniqueString(resourceGroup().id)
var documentIntelligenceName = 'doc-shi-${environmentName}-${suffix}'

resource documentIntelligence 'Microsoft.CognitiveServices/accounts@2024-10-01' = if (deployDocumentIntelligence) {
  name: documentIntelligenceName
  location: location
  kind: 'FormRecognizer'
  sku: {
    name: 'S0'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
  }
}

output documentIntelligenceEndpoint string = deployDocumentIntelligence ? documentIntelligence.properties.endpoint : ''
