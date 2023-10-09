import requests as request
from functions.flatten_functions import flatten_data

headers = {
    "X-Redmine-API-Key": "047f85e0b24fe4d7651e576fedd11ad410336e2d"
}

# params = {'include': 'trackers,issue_categories,enabled_modules,time_entry_activities,issue_custom_fields'}

url = "https://redmine.generalsoftwareinc.com/projects.json"
# response = request.get(url, headers=headers, params=params)
response = request.get(url, headers=headers)
values = response.json()
# Flatten the JSON data
projects = dict(values.items()).get('projects')

flatten_data(projects, 'flattened_projects')