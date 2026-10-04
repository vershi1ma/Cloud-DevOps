def handler(event, context):
    import pg8000
    import os
    conn = pg8000.connect(
        host=os.environ["DB_HOST"],
        user="postgres",
        password=os.environ["DB_PASSWORD"],
        database="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_items")
    rows = cur.fetchall()
    conn.close()
    return {"statusCode": 200, "body": str(rows)}
