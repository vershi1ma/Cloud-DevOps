# AWS Cloud Engineering Portfolio

## Overview
An evolving cloud engineering portfolio built while working toward a cloud/DevOps role.
It started as a single EC2 web server and has grown into a self-healing, load-balanced,
HTTPS-secured, encryption-hardened, and audit logged web tier — with security
(IAM, KMS, CloudTrail, Secrets Manager) treated as a first-class concern throughout,
not bolted on at the end. Ongoing work extends into S3, serverless (Lambda), databases
(RDS), and cloud-agnostic tooling (Terraform, containers, CI/CD), entirely using
free-tier and free-cost resources.

## Architecture
A web tier running on Amazon Linux 2023, originally a single manually-configured
instance, later extended with a reusable Launch Template, an Auto Scaling Group
(1-3 instances across multiple Availability Zones), and an Application Load Balancer.
Traffic is served over HTTPS using a free domain and a Let's Encrypt certificate.
Access is via AWS Systems Manager Session Manager (IAM role-based, no open SSH port).
Account activity is captured via a dedicated CloudTrail trail, and data at rest (S3
objects, EBS volumes) is encrypted using customer managed AWS KMS keys.
A separate public S3 bucket serves a live static website directly from S3, with no
EC2 instance or web server involved. The EC2 instance and the S3 static site bucket
are both managed as infrastructure as code via Terraform, which runs directly on the
EC2 instance (Terraform's Go runtime is incompatible with iSH/iPadOS emulation, so it
executes on a real Linux host instead) rather than in the iSH CLI environment used for
day-to-day AWS CLI and git work.

## Skills demonstrated
IAM · EC2 · Security Groups & Network ACLs · EBS (volumes, snapshots) · Elastic IPs ·
Bash scripting (user data) · Custom AMIs & Launch Templates · Auto Scaling Groups
(self-healing infrastructure) · Application Load Balancers & Target Groups ·
CloudWatch metrics & alarms · EC2 cost models (On-Demand vs Spot) · DNS · TLS/SSL
certificate issuance (Let's Encrypt/ACME) · Apache configuration · Linux system
administration and dependency troubleshooting · AWS KMS (customer-managed keys, envelope encryption) · S3 & EBS encryption at rest · CloudTrail (audit logging) · AWS CLI (Alpine Linux / iSH) · AWS Systems Manager Parameter Store & Secrets Manager · Amazon GuardDuty (threat detection) · Route 53 Resolver DNS Firewall · AWS Network Firewall · Amazon S3 (buckets, storage classes, versioning, lifecycle policies, static website hosting) · AWS Lambda (serverless functions, execution roles, S3 event triggers) · Amazon RDS (managed PostgreSQL, security-group-scoped access) · Lambda VPC networking (security groups, subnets, dependency packaging) · Terraform (infrastructure as code, `import` of pre-existing resources, state management, IAM role scoping for automation)

## Detailed write-ups
- [Core Deployment & Security](docs/01-core-deployment.md)
- [Automation & Golden Images](docs/02-automation-and-golden-images.md)
- [Auto Scaling & Load Balancing](docs/03-auto-scaling-and-load-balancing.md)
- Module 9 — Security Deep-Dive
  - [HTTPS with a Free Domain and Let's Encrypt](docs/09-security-deep-dive/01-https-lets-encrypt.md)
  - [CloudTrail (Audit Logging)](docs/09-security-deep-dive/02-cloudtrail.md)
  - [Encryption at Rest (KMS, S3, EBS)](docs/09-security-deep-dive/03-encryption-at-rest.md)
  - [Secrets Manager & Parameter Store](docs/09-security-deep-dive/04-secrets-manager.md)
  - [Patch Manager](docs/09-security-deep-dive/05-patch-manager.md)
  - [GuardDuty (Threat Detection)](docs/09-security-deep-dive/06-guardduty.md)
  - [DNS Firewall](docs/09-security-deep-dive/07-dns-firewall.md)
  - [Network Firewall](docs/09-security-deep-dive/08-network-firewall.md)
  - Module 10 — S3
    - [S3 Bucket Fundamentals](docs/10-s3/01-bucket-fundamentals.md)
    - [S3 Versioning](docs/10-s3/02-versioning.md)
    - [S3 Lifecycle Policies](docs/10-s3/03-lifecycle-policies.md)
    - [S3 Static Website Hosting](docs/10-s3/04-static-website-hosting.md)
  - Module 11 — Lambda + RDS
    - [Lambda Fundamentals](docs/11-lambda-rds/01-lambda-fundamentals.md)
    - [Lambda + S3 Integration](docs/11-lambda-rds/02-lambda-s3-integration.md)
    - [RDS Fundamentals](docs/11-lambda-rds/03-rds-fundamentals.md)
    - [Lambda + RDS Integration](docs/11-lambda-rds/04-lambda-rds-integration.md)
  - Module 12 — Cloud-Agnostic Tooling
    - [Terraform: Adopting Existing Infrastructure](docs/12-terraform/01-terraform-import.md)

Each write-up covers what was built and the real problems hit and fixed along the way.
