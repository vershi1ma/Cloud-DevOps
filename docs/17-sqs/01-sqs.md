# 17 — SQS: Decoupling Order Writes from Downstream Processing

## What this covers
Added an SQS queue (`orders-queue`, Standard type) so every new order written
by `dynamo-orders-handler` also drops a message onto a queue, decoupling the
order-write path from whatever eventually consumes it. Also added a `POST`
method to the existing `/orders` API Gateway resource (Module 16 only had
`GET`), so orders can actually be created through the public API, not just
queried.

## What was built
- SQS Standard queue (`orders-queue`)
- Lambda execution role (`dynamo-lambda-role`) granted SQS access
- Lambda patched to call `sqs.send_message()` right after the DynamoDB
  `put_item()` call, on every successful order write
- `POST /orders` method added in API Gateway, proxy-integrated to the same
  Lambda, redeployed to the `prod` stage
- Verified end-to-end: a real `POST` through the public API created a
  DynamoDB record (confirmed via a plain browser `GET`) and produced a
  message on the queue (confirmed via `aws sqs receive-message`)

## Real problems hit and fixed
- **Missing POST method**: the first live test failed with "Missing
  Authentication Token" — misleading wording, but it just meant no route
  existed for `POST /orders` yet (Module 16 only wired `GET`). Fixed by
  adding the method and redeploying the stage.
- **Receipt handle mishandling**: `delete-message` requires the exact
  receipt handle from the most recent `receive-message` call — an old or
  placeholder handle is rejected (`ReceiptHandleIsInvalid`). Receiving a
  message never deletes it; it only hides it from other consumers for a
  short visibility-timeout window. A fresh `receive-message` immediately
  before `delete-message` is required each time.

## Key takeaway
SQS's receive/delete split is the whole point of the service: a consumer
can safely pick up a message, and if it crashes or fails mid-processing,
the message reappears for someone else to try — nothing is lost just
because it was read once.
