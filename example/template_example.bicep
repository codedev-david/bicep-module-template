param env string = 'main'

// The env parameter will be passed in from the CLI when the deployment is run on the pipeline. 
@description('Load storage account configurations from YAML file depending on the environment')
var env_values = env == 'dev' ? loadYamlContent('./dev_values.yml'): env == 'test' ? loadYamlContent('./test_values.yml'): env == 'stage' ? loadYamlContent('./stage_values.yml'): env == 'prod' ? loadYamlContent('./prod_values.yml'): env == 'main' ? loadYamlContent('./main_values.yml'): env

//this is fundamental breakthrough because the yml now can be 
//structured if multiple resources need to be created with an outer array name 
//below in the loop shows how to refer to the outer and inner arrays. 

module storageAccounts '../template.bicep' = [for sa in env_values.sa_array: {
  name: '${sa.name}${uniqueString(resourceGroup().id)}'
  params: {
    name: sa.name
    location: sa.location
    sku: sa.sku
    kind: sa.kind
    accessTier: sa.accessTier
  }
}]


output storageAccountName array = env_values.sa_array
