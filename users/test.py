import csv
import json

import requests as request

headers = {"X-Redmine-API-Key": "047f85e0b24fe4d7651e576fedd11ad410336e2d"}

url = "https://redmine.generalsoftwareinc.com/users.json"
response = request.get(url, headers=headers)
values = response.json()
# Flatten the JSON data
projects = dict(values.items()).get("projects")

flattened_data = []
for project in projects:
    custom_fields = dict(project).get("custom_fields")
    parent = dict(project).get("parent")
    if parent is not None:
        project.pop("parent")
    project.pop("custom_fields")
    flattened_project = project.copy()
    # procesamiento del custom_field
    for field in custom_fields:
        flattened_project["custom_fields_id"] = field["id"]
        flattened_project["custom_fields_name"] = field["name"]
        flattened_project["custom_fields_value"] = field["value"]

    # procesamiento del parent
    if parent is not None:
        flattened_project["parent_id"] = dict(parent).get("id")
        flattened_project["parent_name"] = dict(parent).get("name")
    else:
        flattened_project["parent_id"] = -1
        flattened_project["parent_name"] = ""
    flattened_data.append(flattened_project)

# Write the flattened data to a CSV file

with open("flattened_data2.json", "w") as file:
    json.dump(flattened_data, file)

header = flattened_data[0].keys()
with open("flattened_data.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(flattened_data)

print(projects)
print(flattened_data)
