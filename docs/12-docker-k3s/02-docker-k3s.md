# 02 — Docker & k3s: Packaging and Orchestrating a Container

## What this covers
Building a custom Docker image from scratch, running it as a standalone
container, then deploying it into a lightweight Kubernetes cluster (k3s)
with self-healing and stable internal networking.

## What I did
- Provisioned a dedicated EC2 instance (`Docker-k3s-server`) for this work,
  separate from the Terraform-runner instance -- its own least-privilege
  IAM role (SSM access only) and its own security group with zero inbound
  rules, consistent with the no-open-ports approach used throughout this
  project
- Installed Docker via `dnf`, started and enabled the service, added the
  session user to the `docker` group to avoid needing `sudo` per command
- Wrote a small static HTML page and a `Dockerfile` (`FROM nginx:alpine` +
  `COPY` the page in), then built a real image with `docker build` --
  deliberately went beyond just running a pre-built public image
  (`hello-world`), since packaging an app from scratch is the actual core
  Docker skill
- Ran the image as a standalone container (`docker run`), verified it with
  `curl` from inside the instance -- confirmed nothing is reachable from
  outside AWS, since the security group has no inbound rules regardless of
  which port Docker binds to
- Installed k3s (lightweight single-node Kubernetes) and hit a genuine
  resource-constraint problem on `t3.micro`: the default install (bundling
  Traefik, a service load-balancer, and metrics-server) pushed memory to
  ~510MB and caused API server timeouts, confirmed via `journalctl` logs
  showing multi-second SQL queries and PLEG health-check failures. Fixed
  it by reinstalling with `--disable traefik --disable servicelb --disable
  metrics-server` rather than resizing the instance -- right-sizing the
  workload instead of the hardware
- Exported the Docker image (`docker save`) and imported it into k3s's
  separate containerd runtime (`k3s ctr images import`), since Docker and
  k3s do not share an image store even on the same machine
- Deployed the image first as a bare Pod (proved the pipeline works end to
  end), then replaced it with a Deployment (2 replicas) and a Service --
  the Kubernetes equivalent of an Auto Scaling Group and Load Balancer
  from Module 3
- Proved self-healing for real: deleted one of the two running pods and
  confirmed Kubernetes' reconciliation loop created a replacement
  automatically within seconds, with no action taken beyond the delete

## Key takeaway
A bare Pod is a one-shot instruction with no supervision -- if it dies,
nothing brings it back. A Deployment wraps pods with a continuous
reconciliation loop (compare desired replica count to actual, correct any
gap), which is the entire mechanism behind Kubernetes self-healing, and a
Service gives that set of pods one stable internal address regardless of
which individual pods are currently running. Kubernetes' default install
footprint is not free -- k3s's own extras (ingress, load-balancer shim,
metrics) can genuinely starve a `t3.micro`, and the correct fix is often
trimming what's running, not assuming more hardware is needed.
