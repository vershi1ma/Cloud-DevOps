# 01 — Lambda Fundamentals

## What this covers
Deploying and invoking a first AWS Lambda function: execution roles,
packaging code, invocation, and logging.

## What I did
- Created an IAM execution role (cloudlearner-lambda-role) with the
  AWSLambdaBasicExecutionRole managed policy attached
- Wrote a minimal Python handler function locally, packaged it as a zip
  (required deployment format for Lambda)
- Deployed the function via CLI (`create-function`)
- Invoked it and confirmed the actual JSON response came back correctly
- Viewed execution details in CloudWatch Logs (init, start/end, duration,
  memory) -- delivered automatically with zero extra configuration,
  unlike EC2 where CloudWatch requires an agent

## Key takeaway
Lambda runs code without any server to provision, patch, or leave
running -- billing is per invocation and execution time, not uptime.
The execution role is the same IAM mental model already used for
Session Manager and other AWS access, just scoped to what the function
itself needs to do.
