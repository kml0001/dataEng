import requests as request

from functions.flatten_functions import flatten_data

headers = {"X-Redmine-API-Key": "047f85e0b24fe4d7651e576fedd11ad410336e2d"}

url = "https://redmine.generalsoftwareinc.com/issues.json?offset=0&limit=200"
response = request.get(url, headers=headers)
values = response.json()
# Flatten the JSON data
issues = dict(values.items()).get("issues")

flatten_data(issues, "flattened_issues")
