import json
import datetime
from dateutil import relativedelta


def issue_sheduled_this_month(create_issue_date, this_date):
    first_day_of_month = this_date.replace(day=1)

    last_day_of_month = this_date.replace(day=28)

    while True:
        last_day_of_month = last_day_of_month + datetime.timedelta(days=1)
        if last_day_of_month.month != this_date.month:
            last_day_of_month -= datetime.timedelta(days=1)
            break

    return first_day_of_month < create_issue_date < last_day_of_month


def get_issues(all_issues, project_id):
    issues = []
    for i in all_issues:
        if i['project_id'] == project_id:
            issues.append(i)

    return issues


def issue_have_child(all_issues, issue):
    result = False
    for i in all_issues:
        if i['parent_id'] == issue['id']:
            result = True
            break

    return result


projects_json_path = '../../projects/flattened_projects.json'
issues_json_path = '../../issues/flattened_issues.json'

with open(projects_json_path, 'r') as json_file:
    all_projects = json.load(json_file)

with open(issues_json_path, 'r') as json_file:
    all_issues = json.load(json_file)

projects_efficiency = {}

for project in all_projects:
    project_id_str = str(project['id'])
    projects_efficiency[project_id_str] = {}

    initial_date_str = project['created_on']
    initial_date_date = datetime.datetime.strptime(initial_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

    final_date_str = project['updated_on']
    final_date_date = datetime.datetime.strptime(final_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

    increment = datetime.timedelta(days=30)
    while initial_date_date <= final_date_date:
        task_delayed = 0
        task_accomplished = 0
        task_scheduled = 0
        p_eff = 0
        project_issues = get_issues(all_issues, project['id'])

        for issue in project_issues:
            if not issue_have_child(all_issues, issue):
                create_issue_date = datetime.datetime.strptime(issue['created_on'], "%Y-%m-%dT%H:%M:%SZ").date()
                if issue_sheduled_this_month(create_issue_date, initial_date_date):
                    task_scheduled += 1
                if issue['status_id'] == 3 or issue['status_id'] == 4:
                    due_date = issue['due_date']
                    closed_on = issue['closed_on']
                    if due_date:
                        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
                        if closed_on:
                            closed_on = datetime.datetime.strptime(closed_on, "%Y-%m-%d").date()
                        else:
                            updated_on = issue['updated_on'][:10]
                            closed_on = datetime.datetime.strptime(updated_on, "%Y-%m-%d").date()

                        if due_date >= closed_on:
                            task_accomplished += 1
                        else:
                            task_delayed += 1

        if not (task_scheduled == 0):
            p_eff = ((task_accomplished - task_delayed) / task_scheduled) * 100

        month_str = datetime.datetime.strftime(initial_date_date, "%m-%Y")
        projects_efficiency[project_id_str][month_str] = p_eff
        initial_date_date += increment

with open('efficiency_by_project.json', 'w') as file:
    json.dump(projects_efficiency, file, indent=4)
