import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("orders")
sns = boto3.client("sns")
TOPIC_ARN = "arn:aws:sns:eu-north-1:<ACCOUNT_ID>:orders-topic"

def convert_floats(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats(v) for v in obj]
    return obj

def lambda_handler(event, context):
    if "httpMethod" in event:
        method = event["httpMethod"]
        if method == "GET":
            params = event.get("queryStringParameters") or {}
            action = "query"
            customer_id = params.get("customer_id")
        elif method == "POST":
            body = json.loads(event.get("body") or "{}")
            action = "put"
            item = body.get("item", body)
        else:
            return {"statusCode": 405, "body": json.dumps({"error": "method not allowed"})}
    else:
        action = event.get("action")
        customer_id = event.get("customer_id")
        item = event.get("item")

    if action == "put":
        item = convert_floats(item)
        table.put_item(Item=item)

        # Publish to SNS - fans out to orders-queue and any future subscribers
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=json.dumps(item, default=str),
            Subject="New order placed"
        )

        return {"statusCode": 200, "body": json.dumps({"message": "Item inserted", "item": item}, default=str)}

    elif action == "query":
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("customer_id").eq(customer_id)
        )
        return {"statusCode": 200, "body": json.dumps(response["Items"], default=str)}

    else:
        return {"statusCode": 400, "body": json.dumps({"error": "action must be 'put' or 'query'"})}
