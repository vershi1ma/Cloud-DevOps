# Core Deployment & Security

## What was built
- Launched an EC2 instance (Amazon Linux 2023, t3.micro) in a custom security group
- Configured inbound/outbound security group rules (SSH restricted to a single IP, HTTP open publicly)
- Installed and configured Apache manually, and served a custom HTML page
- Connected via AWS Systems Manager Session Manager (IAM role-based access, no SSH keys or open SSH port required)
- Took an EBS snapshot for backup/recovery
- Allocated and associated an Elastic IP for a persistent public address
- Validated SSH key-based access (ssh-keygen, key-based auth, ~/.ssh/config host aliases) on a separate, temporary instance — confirming familiarity with the near-universal standard while keeping SSH closed by design on the production instances in this deployment

## Real problems hit and fixed
- **SSH connectivity failures**: EC2 Instance Connect repeatedly failed from a mobile browser; root-caused to the connection needing to match the client's real-time public IP, which changes frequently on cellular data. Solved by switching to Session Manager (IAM-based access, no inbound SSH dependency at all).
- **Wrong security group edited**: initially modified a security group not actually attached to the running instance; found and fixed by cross-referencing the instance's actual attached security group ID.
- **Wrong AWS region**: an Elastic IP allocated in `us-east-1` couldn't attach to an instance running in `eu-north-1` — Elastic IPs are region-scoped; reallocated in the correct region.
- **Session Manager not connecting**: root-caused to no IAM role being attached to the instance; fixed by attaching an `AmazonSSMManagedInstanceCore` role and rebooting to force the SSM agent to pick up new credentials.
