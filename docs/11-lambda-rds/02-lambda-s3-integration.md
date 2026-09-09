# 02 — Lambda + S3 Integration

## What this covers
Triggering a Lambda function automatically in response to S3 upload
events, rather than invoking it manually.

## What I did
- Wrote a function that reads the bucket name and object key out of an
  S3 event payload and logs them
- Deployed it, reusing the existing Lambda execution role
- Granted S3 explicit permission to invoke the function
  (`lambda add-permission`) -- a separate, required step distinct from
  the execution role itself
- Configured an S3 event notification on the existing lesson bucket to
  call the function on all object-create events
- Uploaded a test file and confirmed, via CloudWatch Logs, that the
  function fired automatically and correctly parsed the event -- no
  manual invocation involved
- Cleaned up the test object afterward

## Key takeaway
Three distinct pieces have to connect for event-driven Lambda to work:
the function itself, an explicit invoke permission for the triggering
service, and the event notification/subscription on that service. This
same pattern (something happens -> a function reacts automatically)
underlies common real-world uses like image processing pipelines,
upload-triggered malware scanning, and automated data ingestion.
