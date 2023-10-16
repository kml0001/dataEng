import requests as request
from functions.flatten_functions import flatten_data

headers = {
    "X-Redmine-API-Key": "1341f71cd5bb28be48df3e7bbd0655654a4857a5"
}

url = "https://redmine.generalsoftwareinc.net/issues.json"
response = request.get(url, headers=headers)
values = response.json()
# Flatten the JSON data
issues = dict(values.items()).get('issues')

flatten_data(issues, 'flattened_issues')
