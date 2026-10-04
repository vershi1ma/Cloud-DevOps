def handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"New object uploaded: {key} in bucket {bucket}")
    return {"statusCode": 200}
