# bicep-module-template Module Documentation

## Resources
- storageAccounts: Microsoft.Storage/storageAccounts@2023-05-01

## Parameters
| Name          | Type   |
|---------------|--------|
| name | string |
| location | string |
| sku | string |
| kind | string |
| accessTier | string |

## Outputs
| Name                   | Type   | Value                                    |
|------------------------|--------|------------------------------------------|
| storageAccountName        | string | storageAccounts.name |
| storageAccountId        | string | storageAccounts.id |
| primaryEndpoints        | object | storageAccounts.properties.primaryEndpoints |
| primaryBlobEndpoint        | string | storageAccounts.properties.primaryEndpoints.blob |
| provisioningState        | string | storageAccounts.properties.provisioningState |
| resourceLocation        | string | storageAccounts.location |

## Sample Inputs
```yaml
sa_array:
  - name: example-sa1
    sku: Standard_LRS
    kind: StorageV2
    accessTier: Hot
    location: eastus
  - name: example-sa2
    sku: Standard_GRS
    kind: Storage
    accessTier: Cool
    location: westus

```

## Examples

### Example Bicep Code
```bicep
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

```

### Calling the Bicep Module from Azure ACR
```bicep

module bicep-module-template 'iacbicep.azurecr.io/bicep-module-template:vX.Y.Z' = {
  name: 'exampleDeployment'
  params: {
    location: 'eastus'
    param1: 'value1'
  }
}

```
