# 02 — S3 Versioning

## What this covers
Protecting objects against accidental overwrite or deletion using S3
bucket versioning.

## What I did
- Enabled versioning on the bucket
- Uploaded the same object key twice with different content, producing
  two distinct versions
- Confirmed both versions listed independently via console and CLI
  (`list-object-versions`)
- Deleted the object and confirmed it wasn't actually destroyed -- a
  delete marker was added instead, while both real versions remained
  intact underneath
- Permanently removed the data by explicitly deleting each version ID
  and the delete marker itself

## Key takeaway
With versioning enabled, a normal delete is reversible by default --
it only adds a delete marker on top of existing versions. True,
permanent deletion requires deleting every version ID individually.
This makes versioning a strong, low-effort safety net against
accidental overwrites or deletions, at the cost of extra storage for
retained old versions.
