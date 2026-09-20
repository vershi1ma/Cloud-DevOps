# 15 — VPC Deep-Dive: Building the Network by Hand

## What this covers
Building a VPC, public and private subnets, an Internet Gateway, a NAT
Gateway, and the route tables that tie them together from scratch — the
networking layer every EC2 instance in this project has always run on
without it ever being examined directly.

## What was built
- `learning-vpc` (`10.1.0.0/16`), isolated from the project's existing VPC
- Two subnets: `learning-public-subnet` (`10.1.1.0/24`) and
  `learning-private-subnet` (`10.1.2.0/24`)
- An Internet Gateway, attached to the VPC
- `learning-public-rt`, with a `0.0.0.0/0 → IGW` route, associated with the
  public subnet — the one thing that actually makes a subnet "public";
  nothing else about a subnet's name, size, or contents determines it
- A NAT Gateway, placed in the public subnet, giving the private subnet
  outbound-only internet access via `learning-private-rt`
- A `t3.micro` test instance launched directly into the private subnet, no
  public IP, to prove the isolation for real rather than just by
  configuration inspection

## Proving it, not just configuring it
Connected to the private-subnet instance via Session Manager — which only
works because the SSM agent needs outbound internet access, routed through
the NAT Gateway just built. Once connected, `curl` to an external site
returned `200`, confirming genuine outbound reachability from an instance
with no public IP and no direct route to the internet. That combination —
reachable outbound, unreachable inbound — is the actual, testable
definition of a private subnet, not something to take on faith.

## Real problem hit and fixed
The first route-table association attempt appeared to succeed in the
console but the CLI verification (`describe-route-tables`) showed
`"Associations": []` — the public route table had the correct
`0.0.0.0/0 → IGW` rule but was associated with nothing, meaning the subnet
wasn't actually public yet despite looking configured correctly. Caught by
verifying via CLI rather than trusting the console's apparent success, and
fixed by re-doing the subnet association step explicitly.

## Cost discipline
A NAT Gateway is the one resource in this entire curriculum that bills by
the hour regardless of use (~$0.045/hr plus data processed). It was created,
used to prove the concept, and deleted — along with its Elastic IP and the
test instance — in the same session, rather than left running between
lessons like every other (free) resource in this project. The VPC, subnets,
Internet Gateway, and route tables all cost nothing and remain in place as
a reference architecture.

## Key takeaway
"Public" and "private" are not properties AWS assigns to a subnet — they
are entirely a consequence of what that subnet's route table points to.
The real interview-ready test is: open the route table and look for
`0.0.0.0/0 → igw-xxxxx`. A NAT Gateway solves a narrower, specific problem —
outbound access for otherwise-unreachable resources — and is the one place
in this whole project where "free tier" stops applying by default.
