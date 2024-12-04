
// ***PARAMETERS***//
// at the most basic level, bicep parameters should have a name, type, and description. 

@description('The name of the application')
param name string

@description('The location of the storage account.')
param location string

@description('The SKU of the storage account.')
param sku string

@description('The kind of the storage account.')
param kind string

@description('The access tier of the storage account.')
param accessTier string


// ***RESOURCES***//
// ALL required properties as well as optional values we currently use in MSI should be parameterized.

resource storageAccounts 'Microsoft.Storage/storageAccounts@2023-05-01' =  {
  name: '${name}-${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: sku
  }
  kind: kind
  properties: {
    accessTier: accessTier
  }
}



// ***OUTPUTS***//
// Outputs are used to return information about the resources that were created.
output storageAccountName string = storageAccounts.name
output storageAccountId string = storageAccounts.id
output primaryEndpoints object = storageAccounts.properties.primaryEndpoints
output primaryBlobEndpoint string = storageAccounts.properties.primaryEndpoints.blob
output provisioningState string = storageAccounts.properties.provisioningState
output resourceLocation string = storageAccounts.location

