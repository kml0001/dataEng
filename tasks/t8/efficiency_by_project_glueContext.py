import csv
import datetime
import json
from io import StringIO

import boto3


def generate_same_day_of_next_month(date: datetime.date):
    year = date.year
    month = date.month
    day = date.day
    if month + 1 > 12:
        year += 1
        month = 1
    else:
        month += 1
    if day >= 28 and month == 2:
        if year % 4 != 0:
            day = 28
        elif day >= 29:
            day = 29
    if day > 30:
        if month <= 7:
            if month % 2 == 0:
                day = 30
        else:
            if month % 2 != 0:
                day = 30
    return datetime.date(year, month, day)


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
        if i["project_id"] == project_id:
            issues.append(i)

    return issues


def issue_have_child(all_issues, issue):
    result = False
    for i in all_issues:
        if i["parent_id"] == issue["id"]:
            result = True
            break

    return result


s3 = boto3.client("s3")

projects_bucket_name = "bucketfor008182637297"
projects_file_key = "redmine/projects/flattened_data/flattened_projects.json"
issues_bucket_name = "bucketfor008182637297"
issues_file_key = "redmine/projects/flattened_data/flattened_issues.json"

projects_response = s3.get_object(Bucket=projects_bucket_name, Key=projects_file_key)
issues_response = s3.get_object(Bucket=issues_bucket_name, Key=issues_file_key)


# projects_json_data = projects_response["Body"].read().decode("utf-8")
# issues_json_data = issues_response["Body"].read().decode("utf-8")

all_projects = json.loads(projects_response["Body"])
all_issues = json.loads(issues_response["Body"])

projects_efficiency = []
for project in all_projects:
    initial_date_str = project["created_on"]
    initial_date_date = datetime.datetime.strptime(initial_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

    final_date_str = project["updated_on"]
    final_date_date = datetime.datetime.strptime(final_date_str, "%Y-%m-%dT%H:%M:%SZ").date()

    while initial_date_date <= final_date_date:
        task_delayed = 0
        task_accomplished = 0
        task_scheduled = 0
        p_eff = 0.0
        project_issues = get_issues(all_issues, project["id"])

        for issue in project_issues:
            if not issue_have_child(all_issues, issue):
                create_issue_date = datetime.datetime.strptime(issue["created_on"], "%Y-%m-%dT%H:%M:%SZ").date()
                if issue_sheduled_this_month(create_issue_date, initial_date_date):
                    task_scheduled += 1
                if issue["status_id"] == 3 or issue["status_id"] == 4:
                    due_date = issue["due_date"]
                    closed_on = issue["closed_on"]
                    if due_date:
                        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
                        if closed_on:
                            closed_on = datetime.datetime.strptime(closed_on, "%Y-%m-%d").date()
                        else:
                            updated_on = issue["updated_on"][:10]
                            closed_on = datetime.datetime.strptime(updated_on, "%Y-%m-%d").date()

                        if due_date >= closed_on:
                            task_accomplished += 1
                        else:
                            task_delayed += 1

        if task_scheduled > 0:
            p_eff = ((task_accomplished - task_delayed) / task_scheduled) * 100

        month_year_str = datetime.datetime.strftime(initial_date_date, "%m-%Y")
        month, year = month_year_str.split("-")
        record = {
            "id": f"{project['id']}_{month_year_str}",
            "project_id": project["id"],
            "project_name": project["name"],
            "month": month,
            "year": year,
            "tasks_acomplished": task_accomplished,
            "tasks_delayed": task_delayed,
            "tasks_scheduled": task_scheduled,
            "efficiency": p_eff,
        }
        projects_efficiency.append(record)

        initial_date_date = generate_same_day_of_next_month(initial_date_date)

s3.put_object(
    Body=(bytes(json.dumps(projects_efficiency).encode("UTF-8"))),
    Bucket="bucketfor008182637297",
    Key="redmine/projects/flatten_data/projects/projects_efficiency.json",
)

csv_buffer = StringIO()
header = projects_efficiency[0].keys()

# Write the CSV data to the in-memory buffer
writer = csv.DictWriter(csv_buffer, fieldnames=header)
writer.writeheader()
writer.writerows(projects_efficiency)
# Get the CSV contents from the buffer
csv_content = csv_buffer.getvalue()
# Close the buffer
csv_buffer.close()
s3.put_object(
    Body=csv_content,
    Bucket="bucketfor008182637297",
    Key="redmine/projects/flatten_csv/projects/projects_efficiency_csv.csv",
)
