param env string = 'dev'

// The env parameter will be passed in from the CLI when the deployment is run on the pipeline. 
@description('Load storage account configurations from YAML file depending on the environment')
var env_values = [env == 'dev' ? loadYamlContent('./dev_values.yml'): env == 'test' ? loadYamlContent('./test_values.yml'): env == 'stage' ? loadYamlContent('./stage_values.yml'): env == 'prod' ? loadYamlContent('./prod_values.yml'): env]


module storageAccounts '../template.bicep' = [for sa in env_values: {
  name: '${sa.name}-${uniqueString(resourceGroup().id)}'
  params: {
    name: sa.name
    location: sa.location
    sku: sa.sku
    kind: sa.kind
    accessTier: sa.accessTier
  }
}]
