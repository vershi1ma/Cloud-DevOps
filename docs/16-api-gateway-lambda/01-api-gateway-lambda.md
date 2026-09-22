# 16 — API Gateway + Lambda: A Public REST API

## What this covers
Putting a real, public REST API in front of the existing `dynamo-orders-handler`
Lambda (from Module 14), so the `orders` DynamoDB table becomes reachable over
plain HTTP — no AWS credentials, no SDK, just a URL. Chose API Gateway's REST
API product deliberately over the newer, simpler HTTP API, specifically to
work through its extra concepts (resources, methods, and deployment as a
distinct step from configuration) rather than have them abstracted away.

## Building the API
Built up as separate, explicit objects: a REST API container (`orders-api`),
a child resource (`/orders`), and a `GET` method on that resource wired to
the Lambda via **proxy integration** — meaning API Gateway forwards the
entire raw HTTP request to the function rather than doing any request/response
mapping itself. Attaching the integration auto-created a scoped resource
policy on the Lambda, granting `apigateway.amazonaws.com` invoke permission
conditioned on the exact API ID, method, and path — not a blanket grant.
Nothing is actually reachable until explicitly **deployed to a stage**
(`prod`); resources and methods alone are just configuration.

## The proxy-integration event-shape mismatch
The Lambda's original logic (from Module 14) expected a flat
`{"action": "put"|"query", ...}` object, since that's what direct CLI
invocation had always sent it. Proxy integration sends something entirely
different — the full raw HTTP request (method, headers, query string, body)
with no `action` field anywhere — so the first live request correctly reached
the Lambda but was rejected by its own logic. Fixed by branching on
`"httpMethod" in event`: a `GET` maps to `action="query"` with `customer_id`
read from the query string, a `POST` maps to `action="put"` with the item
read from the JSON body, while the original direct-invoke shape still works
unchanged underneath. Confirmed working end-to-end via `curl` and a plain
browser request, both returning live DynamoDB data with zero AWS credentials
involved in the request.

## Real problems hit and fixed
- **Proxy-integration event mismatch**: see above — the single most common
  first-time gotcha connecting an existing Lambda to API Gateway; the
  function ran successfully but rejected the request due to the shape
  change, not a wiring failure
- **Expired presigned S3 URL**: fetching the Lambda's existing source via
  `aws lambda get-function --query Code.Location` returns a presigned URL
  valid for only ~10 minutes; generating it in one step and using it later
  in a separate command let it expire silently (empty/missing file, no
  error). Fixed by fetching and using the URL in the same command
- **iSH heredoc corruption on large pastes**: writing the ~40-line patched
  Lambda file via `cat << 'EOF'` caused part of the paste to be interpreted
  as literal shell commands mid-stream rather than file content — likely a
  paste-buffer limit on a block that size. Fixed by base64-encoding the
  file and piping it through a single unbroken line
  (`echo "<b64>" | base64 -d > file.py`), which can't be split across
  separate command submissions the way a multi-line paste can
- **"Missing Authentication Token" in-browser**: a misleadingly-named
  API Gateway response that actually just means no route matches the
  requested path — hit by navigating to an incomplete URL, resolved by
  using the exact deployed path (`/prod/orders?customer_id=...`)

## Key takeaway
Proxy integration is simpler to set up than manual mapping, but it comes
with a real cost: your Lambda receives the *entire* HTTP request, not a
clean custom payload, so any Lambda built and tested via direct invocation
needs its entry point adapted before it can safely serve real traffic behind
API Gateway. That adaptation — reading `httpMethod`, `queryStringParameters`,
and `body` instead of assuming a flat custom event — is the actual skill
this module tests, more than the console click-through itself.
