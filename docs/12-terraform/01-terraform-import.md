# 01 — Terraform: Adopting Existing Infrastructure

## What this covers
Introducing Terraform (infrastructure as code) into a portfolio that was
previously built entirely by hand -- without disruption or rebuilding
anything. Also covers a Terraform-specific execution environment
constraint on iSH/iPadOS.

## What I did
- Discovered Terraform cannot run under iSH (Alpine on iPadOS): its Go
  runtime crashes with `fatal error: unexpected signal during runtime
  execution` -- the same class of emulation limitation that rules out
  Docker/Kubernetes on iSH. Installed and ran Terraform directly on the
  existing EC2 instance instead, over the same Session Manager access
  path used throughout this project (no SSH, no new access pattern)
- Wrote a minimal Terraform configuration describing the EC2 instance
  and, separately, the public S3 static website bucket (bucket resource,
  website configuration, and public access block -- split across three
  resources per the AWS provider's v5 model)
- Used `terraform import` to bring both the existing EC2 instance and
  the existing S3 bucket under Terraform management, rather than
  `apply`, which would have attempted to create duplicates
- Confirmed zero drift with `terraform plan` immediately after import
  ("No changes. Your infrastructure matches the configuration.")
- Extended the EC2 instance's IAM role (`EC2-SSM-Role`) with
  `AmazonEC2FullAccess` and `AmazonS3FullAccess`, since the instance now
  additionally serves as a Terraform runner and needs to read/manage
  those resources on its own behalf -- a deliberate scope increase tied
  to a new responsibility, not scope creep
- Proved real, working control (not just state tracking) by adding a
  `ManagedBy = "Terraform"` tag to both the EC2 instance and the S3
  bucket through `terraform plan` / `terraform apply`, then confirming
  the tags appeared in the AWS console

## Key takeaway
Adopting existing, hand-built infrastructure into Terraform is a
distinct and very common real-world skill, separate from provisioning
new infrastructure from scratch. `terraform import` plus a config that
matches reality (verified via `plan` showing no changes) is the safe
path -- it avoids duplicate or conflicting resources entirely. Once
imported, Terraform provides genuine control: changes made in code are
reflected in AWS after `plan`/`apply`, not just recorded in local state.

## Follow-up: closing the create/destroy gap
The work above only ever used `terraform import` -- never created a
resource from scratch. Closed that gap with a small, disposable S3
bucket: wrote a new `aws_s3_bucket` block for a bucket that didn't yet
exist, ran `terraform plan` (showed `1 to add`, with `(known after
apply)` values throughout -- the visible signature of a real create,
distinct from every prior `plan` against already-existing resources),
then `terraform apply` to actually create it.

Also ran `terraform destroy` to remove the demo bucket afterward --
and hit a genuine near-miss worth documenting: plain `terraform
destroy` with no arguments targets every resource in the state file,
not just the one intended for removal. It surfaced a plan to destroy
5 resources, including the live S3 website bucket. Caught it before
confirming, cancelled, and re-ran scoped to just the demo resource
with `terraform destroy -target=aws_s3_bucket.terraform_demo_bucket`.
Confirmed with a follow-up `terraform plan` that the real
infrastructure was untouched, then removed the now-orphaned resource
block from `main.tf` so a future `apply` wouldn't try to recreate it.

**Lesson:** `terraform destroy` (and `apply`, for that matter) operate
on the entire state file by default. `-target` scopes an operation to
a specific resource and is the correct tool for removing or fixing one
thing without touching everything else Terraform manages -- always
worth a second look at the full plan output, resource count included,
before typing `yes`.
