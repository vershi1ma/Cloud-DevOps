# 14 — DynamoDB: NoSQL Data Storage with Lambda

## What this covers
Creating a DynamoDB table, understanding partition/sort key design, and
wiring a purpose-built Lambda function to read and write it with a
least-privilege IAM role — kept separate from the existing RDS Lambda to
keep the two data-store examples distinct in the portfolio.

## Table design
Created an `orders` table with `customer_id` as the partition key and
`order_date` as the sort key, on-demand (pay-per-request) billing. This
combination is the actual design decision DynamoDB forces up front: items
sharing a partition key are grouped together, so `customer_id` alone answers
"all orders for this customer" in one fast query, and adding the sort key
range enables "orders after a given date" without scanning the whole table.
The tradeoff, made explicit by testing it: a query for "all pending orders
across every customer" isn't supported by this key design at all — it would
require a full table scan or a secondary index, which is the real difference
between designing for known query patterns (DynamoDB) versus flexible ad-hoc
querying (RDS).

## Lambda integration
A new Lambda (`dynamo-orders-handler`) with its own IAM role, scoped to
exactly one table ARN and five actions (`GetItem`, `PutItem`, `UpdateItem`,
`DeleteItem`, `Query`) — no blanket DynamoDB access, same least-privilege
discipline as the RDS Lambda. The function takes a simple `action` field
(`put` or `query`) so both operations could be tested from a single
function without needing separate deployments.

## Real problems hit and fixed
- **CLI v1 vs v2 flag mismatch**: `--cli-binary-format` (needed on AWS CLI
  v2 for JSON payloads) isn't recognized on the CLI v1 installed here —
  dropped the flag; v1 accepts raw JSON directly
- **Type-tagged vs. plain values**: the raw CLI (`put-item`/`get-item`) uses
  DynamoDB's low-level, type-tagged format (`{"S": "value"}`); boto3's
  `resource()` API used inside the Lambda expects plain Python values
  instead. Passing the tagged format into the Lambda's JSON payload made
  boto3 interpret `{"S": "CUST-202"}` as a Map type rather than a string —
  a genuine "two APIs, two conventions" trap
- **Float rejection**: DynamoDB refuses native floats outright, even through
  the resource API — it requires Python's `Decimal` type specifically to
  avoid floating-point precision loss (a real concern for money values).
  Fixed by converting incoming numeric values to `Decimal` before
  `put_item`, and by JSON-encoding `Decimal` values back out with
  `default=str` on the way out, since `Decimal` isn't natively
  JSON-serializable either

## Key takeaway
DynamoDB's schema-less flexibility is real, but it isn't free: the table's
key design *is* the query design, decided before the table is even useful.
Get the partition/sort key choice right for your actual access patterns and
lookups are near-instant at any scale; get it wrong and even simple queries
require a full scan. That tradeoff — and the float/Decimal quirk — are the
two things most worth being able to explain from this module in an
interview.
