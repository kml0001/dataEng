import requests as request
from functions.flatten_functions import flatten_data

headers = {
    "X-Redmine-API-Key": "1341f71cd5bb28be48df3e7bbd0655654a4857a5"
}

# params = {'include': 'trackers,issue_categories,enabled_modules,time_entry_activities,issue_custom_fields'}

url = "https://redmine.generalsoftwareinc.net/projects.json"
# response = request.get(url, headers=headers, params=params)
response = request.get(url, headers=headers)
values = response.json()
# Flatten the JSON data
projects = dict(values.items()).get('projects')

flatten_data(projects, 'flattened_projects')