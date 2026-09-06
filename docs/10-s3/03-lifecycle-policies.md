# 03 — S3 Lifecycle Policies

## What this covers
Automating storage-class transitions and object expiration based on
object age, without manual intervention.

## What I did
- Uploaded a test object under a logs/ prefix
- Created a lifecycle rule (console) scoped to that prefix:
  - Transition to Standard-IA after 30 days
  - Expire (delete) after 90 days
- Verified the rule via CLI (`get-bucket-lifecycle-configuration`),
  confirming the prefix filter, transition, and expiration all matched
  what was configured
- Cleaned up the test object and removed the lifecycle rule

## Key takeaway
Lifecycle rules turn storage cost management into a "set once, runs
forever" mechanism -- the standard real-world approach to preventing
logs, backups, and old data from silently accumulating cost with no
one actively managing it.
