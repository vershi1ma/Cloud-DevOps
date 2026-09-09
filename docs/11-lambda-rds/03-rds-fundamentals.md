# 03 — RDS Fundamentals

## What this covers
Provisioning a managed PostgreSQL database with RDS, configuring
network access, and connecting to it from EC2.

## What I did
- Created an RDS PostgreSQL instance (Sandbox / db.t4g.micro, free-tier
  eligible) named cloudlearner-db
- Configured the RDS security group to allow inbound traffic only from
  Cloudlearner-server's security group -- not open to the internet
- Connected from Cloudlearner-server via Session Manager using `psql`,
  over an automatically-encrypted TLS connection
- Created a table, inserted a row, and queried it back successfully

## Cost note
Unlike most of this project, RDS is not free forever -- new accounts
get a 12-month free tier (750 hours/month of a small instance class).
This instance is being kept running only through the upcoming Lambda +
RDS integration lesson, then deleted, rather than left running
indefinitely.

## Key takeaway
RDS removes the operational burden of running a database yourself --
no OS patching, no manual backup configuration, no install process --
while still behaving like a normal database once connected. Network
access control (security groups scoped to a specific source, not the
public internet) is handled the same way as every other AWS service in
this project: least-privilege by default.
