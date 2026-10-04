# Lambda functions

Copies of the four AWS Lambda functions built during the Cloud and DevOps curriculum, captured from the deployed versions on 4 Oct 2026. Only the handler code is included, not bundled libraries. The AWS account ID in the orders handler is replaced with a placeholder, and the database function reads its host and password from environment variables, so no secrets live in the code.

| Folder | Purpose |
|---|---|
| dynamo-orders-handler | Orders API handler: DynamoDB reads and writes behind API Gateway, plus messaging |
| cloudlearner-hello | First Lambda function |
| cloudlearner-s3-trigger | Runs when a file lands in an S3 bucket |
| cloudlearner-rds-query | Queries an RDS database (the database has since been deleted) |
