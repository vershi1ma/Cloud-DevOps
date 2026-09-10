# 04 — Lambda + RDS Integration

## What this covers
Connecting a Lambda function to a private RDS database inside a VPC --
the most involved integration in this project, requiring network
access, IAM permissions, and a manually bundled database driver to all
work together.

## What I did
- Attached the AWSLambdaVPCAccessExecutionRole policy to the existing
  Lambda execution role, enabling it to create network interfaces
  inside a VPC
- Created a dedicated security group (cloudlearner-lambda-sg) for the
  function, then added it as an allowed inbound source on the RDS
  security group
- Installed pg8000 (a pure-Python PostgreSQL driver, chosen specifically
  to avoid native-binary compilation issues) and bundled it directly
  into the deployment zip alongside the function code
- Deployed the function with `--vpc-config` (subnets + security group)
  and environment variables for the DB host and password
- Hit and fixed a real bug: the dependency was nested one folder too
  deep in the zip (package/pg8000/... instead of pg8000/... at zip
  root), causing `ModuleNotFoundError` on the first invocation.
  Rebuilt the zip from inside the dependency folder and redeployed
  with `update-function-code`
- Invoked the function and confirmed it read real data back from RDS
  automatically -- the same row inserted manually in the RDS
  fundamentals lesson

## Cleanup
Deleted the RDS instance (`--skip-final-snapshot`) once this lesson
was complete, per the cost-conscious plan agreed on before building it
-- confirmed zero RDS instances remain in the account.

## Why the driver had to be bundled manually
Lambda's runtime includes only core Python -- no third-party libraries.
Every dependency must be included in the deployment package itself,
unlike EC2 where a package can simply be pip-installed once onto a
persistent machine.

## Key takeaway
Making Lambda talk to a VPC-private resource requires three separate
things to agree: an IAM permission allowing VPC attachment, a security
group explicitly trusted by the target resource, and correct network
placement (subnets). The dependency-packaging bug was a genuine,
common real-world Lambda pitfall -- fixed by understanding how Lambda
unpacks a deployment zip, not by guesswork.
