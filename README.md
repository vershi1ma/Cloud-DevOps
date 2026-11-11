# Cloud & DevOps Portfolio

Hands-on AWS and DevOps projects: a self-healing, HTTPS web tier, a CI/CD pipeline on Kubernetes (k3s), infrastructure as code with Terraform, and serverless services, with security built in from the start.

## Highlights
- **Self-healing web tier:** Auto Scaling Group (1-3 instances, multiple AZs) behind an Application Load Balancer, served over HTTPS (Let's Encrypt). Access through Session Manager, with no open SSH port.
- **CI/CD on k3s:** a git push builds the image, imports it into k3s and rolls out the new version using a self-hosted GitHub Actions runner. Two independent microservices with path-filtered pipelines.
- **Security by default:** KMS encryption at rest, CloudTrail audit logging, Secrets Manager, GuardDuty, DNS Firewall, Network Firewall.
- **Serverless and data:** API Gateway, Lambda, DynamoDB and SQS; Lambda with RDS (PostgreSQL).
- **Networking:** a hand-built VPC with public and private subnets, Internet Gateway and NAT Gateway.
- **Infrastructure as code:** Terraform, including importing existing resources.
## Skills demonstrated
IAM · EC2 · Security Groups & Network ACLs · EBS (volumes, snapshots) · Elastic IPs ·
Bash scripting (user data) · Custom AMIs & Launch Templates · Auto Scaling Groups
(self-healing infrastructure) · Application Load Balancers & Target Groups ·
CloudWatch metrics & alarms · EC2 cost models (On-Demand vs Spot) · DNS · TLS/SSL
certificate issuance (Let's Encrypt/ACME) · Apache configuration · Linux system
administration and dependency troubleshooting · AWS KMS (customer-managed keys, envelope encryption) · S3 & EBS encryption at rest · CloudTrail (audit logging) · AWS CLI (Alpine Linux / iSH) · AWS Systems Manager Parameter Store & Secrets Manager · Amazon GuardDuty (threat detection) · Route 53 Resolver DNS Firewall · AWS Network Firewall · Amazon S3 (buckets, storage classes, versioning, lifecycle policies, static website hosting) · AWS Lambda (serverless functions, execution roles, S3 event triggers) · Amazon RDS (managed PostgreSQL, security-group-scoped access) · Lambda VPC networking (security groups, subnets, dependency packaging) · Terraform (infrastructure as code, `import` of pre-existing resources, state management, IAM role scoping for automation) · Docker (image builds, Dockerfiles, container networking) · Kubernetes/k3s (Pods, Deployments, Services, self-healing via reconciliation loops, resource-constrained troubleshooting) · GitHub Actions CI/CD (self-hosted runners, systemd service management, automated build-import-rollout pipelines, path-filtered conditional pipelines for independent service deploys) · Microservices architecture (service decomposition, internal service discovery via Kubernetes DNS, config separation via environment variables) · Amazon DynamoDB (partition/sort key table design, on-demand billing, Lambda integration via boto3, Decimal-type handling) · VPC networking (subnets, route tables, Internet Gateway, NAT Gateway, Security Groups vs. Network ACLs) · API Gateway (REST APIs, Lambda proxy integration) · Amazon SQS (queues, message lifecycle, decoupled processing)

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
    - [Docker & k3s: Packaging and Orchestrating a Container](docs/12-docker-k3s/02-docker-k3s.md)
    - [CI/CD: Self-Hosted GitHub Actions Runner](docs/12-docker-k3s/03-cicd-self-hosted-runner.md)
  - Module 13 — Microservices
    - [Microservices: Independent Services on k3s](docs/13-microservices/01-microservices.md)
  - Module 14 — DynamoDB
    - [DynamoDB: NoSQL Data Storage with Lambda](docs/14-dynamodb/01-dynamodb.md)
  - Module 15 — VPC
    - [VPC Deep-Dive: Building the Network by Hand](docs/15-vpc/01-vpc-deep-dive.md)
  - Module 16 — API Gateway + Lambda
    - [Public REST API for an Existing Lambda](docs/16-api-gateway-lambda/01-api-gateway-lambda.md)
  - Module 17 — SQS
    - [Decoupling Order Writes with SQS](docs/17-sqs/01-sqs.md)

Each write-up covers what was built and the real problems hit and fixed along the way.
