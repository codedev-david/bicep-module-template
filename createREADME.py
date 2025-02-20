import os
import re

def parse_bicep(file_path):
    print(f"Parsing Bicep file: {file_path}")
    with open(file_path, 'r') as f:
        content = f.readlines()

    resources, parameters, outputs = [], [], []
    param_description = None

    for line in content:
        description_match = re.search(r'@description\s*\(\'(.+?)\'\)', line)
        if description_match:
            param_description = description_match.group(1)

        if line.strip().startswith('param'):
            match = re.search(r'param\s+(\w+)\s+(\w+)', line)
            if match:
                param_name = match.group(1)
                param_type = match.group(2)
                default_match = re.search(r'=\s*(.+)', line)
                is_required = default_match is None  # If there's no "=" followed by a value, it's required
                parameters.append({
                    'name': param_name,
                    'type': param_type,
                    'required': is_required,
                    'description': param_description or "No description provided"
                })
            param_description = None  # Reset description

        elif line.strip().startswith('resource'):
            match = re.search(r'resource\s+(\w+)\s+\'([^\']+)\'', line)
            if match:
                resources.append({'name': match.group(1), 'type': match.group(2)})
        elif line.strip().startswith('output'):
            match = re.search(r'output\s+(\w+)\s+(\w+)\s*=\s*(.+)', line)
            if match:
                outputs.append({'name': match.group(1), 'type': match.group(2), 'value': match.group(3)})

    print(f"Finished parsing Bicep file. Found {len(parameters)} parameters, {len(resources)} resources, and {len(outputs)} outputs.")
    return resources, parameters, outputs

def find_example_file(example_folder, extension):
    print(f"Searching for example files with extension '{extension}' in folder: {example_folder}")
    for root, _, files in os.walk(example_folder):
        for file in files:
            if file.endswith(extension):
                print(f"Found example file: {file}")
                return os.path.join(root, file)
    print(f"No example files found with extension '{extension}'.")
    return None

def generate_readme(folder_name, resources, parameters, outputs, example_bicep, example_inputs, acr_example, output_file='README.md'):
    try:
        with open(output_file, 'w') as f:
            f.write(f'# {folder_name} Module Documentation\n\n')
            
            f.write('## Resources\n')
            if resources:
                for res in resources:
                    f.write(f"- {res['name']}: {res['type']}\n")
            else:
                f.write('No resources defined.\n')

            f.write('\n## Parameters\n')
            if parameters:
                f.write('| Name          | Type   | Required | Description                      |\n')
                f.write('|---------------|--------|----------|----------------------------------|\n')
                for param in parameters:
                    required_status = 'Yes' if param['required'] else 'No'
                    f.write(f"| {param['name']} | {param['type']} | {required_status} | {param['description']} |\n")
            else:
                f.write('No parameters defined.\n')

            f.write('\n## Outputs\n')
            if outputs:
                f.write('| Name                   | Type   | Value                                    |\n')
                f.write('|------------------------|--------|------------------------------------------|\n')
                for output in outputs:
                    f.write(f"| {output['name']}        | {output['type']} | {output['value']} |\n")
            else:
                f.write('No outputs defined.\n')

            f.write('\n## Sample Inputs\n')
            if example_inputs:
                f.write('```yaml\n')
                f.write(example_inputs)
                f.write('\n```\n')
            else:
                f.write('No sample inputs provided.\n')

            f.write('\n## Examples\n')
            if example_bicep:
                f.write('\n### Example Bicep Code\n')
                f.write('```bicep\n')
                f.write(example_bicep)
                f.write('\n```\n')
            if acr_example:
                f.write('\n### Calling the Bicep Module from Azure ACR\n')
                f.write('```bicep\n')
                f.write(acr_example)
                f.write('\n```\n')

            if not example_bicep and not acr_example:
                f.write('No examples provided.\n')

        print(f"README.md generated successfully at {output_file}!")
    except Exception as e:
        print(f"Error while generating README.md: {e}")

if __name__ == '__main__':
    bicep_file = None
    example_folder = './example'
    current_folder_name = os.path.basename(os.getcwd())
    acr_registry_name = 'iacbicep.azurecr.io'
    bicep_module_version = ':vX.Y.Z'

    # Strip everything before the first dash and the dash itself
    stripped_folder_name = re.sub(r'^[^-]*-', '', current_folder_name)

    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.bicep'):
                bicep_file = os.path.join(root, file)
                break
        if bicep_file:
            break

    if bicep_file:
        print(f"Processing file: {bicep_file}")
        resources, parameters, outputs = parse_bicep(bicep_file)

        example_bicep_file = find_example_file(example_folder, '.bicep')
        example_yml_file = find_example_file(example_folder, '.yml')

        example_bicep_content = None
        if example_bicep_file:
            with open(example_bicep_file, 'r') as f:
                example_bicep_content = f.read()

        example_inputs_content = None
        if example_yml_file:
            with open(example_yml_file, 'r') as f:
                example_inputs_content = f.read()

        acr_example = f"""
module {stripped_folder_name} 'br:{acr_registry_name}/{stripped_folder_name}{bicep_module_version}' = {{
  name: 'exampleDeployment'
  params: {{
    location: 'eastus'
    param1: 'value1'
  }}
}}
"""

        generate_readme(current_folder_name, resources, parameters, outputs, example_bicep_content, example_inputs_content, acr_example)
    else:
        print("No .bicep files found.")
