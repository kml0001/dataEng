import json

with open('../../projects/flattened_projects.json', 'r') as file:
    projects = json.load(file)

projects_without_parents = []

for project in projects:
    if project['parent_id'] == -1:
        projects_without_parents.append(project)

with open('t2_projects_without_parents.json', 'w') as file:
    json.dump(projects_without_parents, file, indent=4)

print(f'cantidad de proyectos sin padre: {len(projects_without_parents)}')