import csv
import json
from io import StringIO

import boto3


def to_json(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def to_csv(data, path):
    header_set = set()
    for dict in data:
        header_set.update(dict.keys())
    header_list = list(header_set)

    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header_list)
        writer.writeheader()
        writer.writerows(data)


def to_json_s3(data, bucket, partition):
    s3 = boto3.client("s3")
    s3.put_object(
        Body=(bytes(json.dumps(data).encode("UTF-8"))),
        Bucket=bucket,
        Key=partition,
    )


def to_csv_s3(data, bucket, partition):
    s3 = boto3.client("s3")
    csv_buffer = StringIO()
    header = data[0].keys()

    # Write the CSV data to the in-memory buffer
    writer = csv.DictWriter(csv_buffer, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)
    # Get the CSV contents from the buffer
    csv_content = csv_buffer.getvalue()
    # Close the buffer
    csv_buffer.close()
    s3.put_object(
        Body=csv_content,
        Bucket=bucket,
        Key=partition,
    )
