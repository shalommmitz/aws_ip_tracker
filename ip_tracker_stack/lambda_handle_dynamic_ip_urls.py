import os
import json
import datetime
import boto3
from urllib.parse import unquote_plus

table_name = os.environ["TABLE_NAME"]
hashes = set(os.environ["HASH_LIST"].split(","))
manage_hash = os.environ["MANAGE_HASH"]
dynamodb = boto3.client("dynamodb")

def handler(event, context):
    path = unquote_plus(event.get("rawPath", "").lstrip("/"))
    source_ip = event.get("requestContext", {}).get("http", {}).get("sourceIp", "unknown")
    now = datetime.datetime.utcnow().isoformat()

    if path == f"manage/{manage_hash}":
        return get_all_hashes()

    if path in hashes:
        log_ip(path, source_ip, now)
        return {
            "statusCode": 200,
            "body": f"Logged IP for hash {path}"
        }

    return {"statusCode": 404, "body": "Not found"}

def log_ip(hash_val, ip, timestamp):
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "hash": {"S": hash_val},
            "timestamp": {"S": timestamp},
            "ip": {"S": ip}
        }
    )
    trim_old_entries(hash_val)

def trim_old_entries(hash_val):
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression="hash = :h",
        ExpressionAttributeValues={":h": {"S": hash_val}},
        ScanIndexForward=False
    )
    items = response.get("Items", [])
    if len(items) > 10:
        for item in items[10:]:
            dynamodb.delete_item(
                TableName=table_name,
                Key={"hash": item["hash"], "timestamp": item["timestamp"]}
            )

def get_all_hashes():
    response = dynamodb.scan(TableName=table_name)
    items = response.get("Items", [])
    results = [
        {
            "hash": i["hash"]["S"],
            "timestamp": i["timestamp"]["S"],
            "ip": i["ip"]["S"]
        } for i in items
    ]
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(results)
    }
