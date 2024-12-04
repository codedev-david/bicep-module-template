@description('Load storage account configurations from YAML file.')
var sa_array = loadYamlContent('test_values.yml').sa_array


module storageAccounts '../template.bicep' = [for sa in sa_array: {
  name: '${sa.name}-${uniqueString(resourceGroup().id)}'
  params: {
    name: sa.name
    location: sa.location
    sku: sa.sku
    kind: sa.kind
    accessTier: sa.accessTier
  }
}]
