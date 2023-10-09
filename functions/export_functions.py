import csv
import json


def to_json(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def to_csv(data, path):
    header_set = set()
    for dict in data:
        header_set.update(dict.keys())
    header_list = list(header_set)

    with open(path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header_list)
        writer.writeheader()
        writer.writerows(data)
