# 03 — CI/CD: Self-Hosted GitHub Actions Runner

## What this covers
Automating the build-and-deploy loop for the k3s app: a `git push` triggers a
build, imports the image into k3s, and rolls out the new version — with no
manual deploy steps.

## Why a self-hosted runner
GitHub's own hosted runners can't reach `Docker-k3s-server` — it has no
inbound ports open, by design. The fix: install the runner directly on the
instance itself, registered with GitHub and polling outbound-only, so no
inbound access is ever needed. This is the piece that connects Docker, k3s,
and CI/CD into one working system.

## Pipeline
`.github/workflows/docker-build.yml`, triggered on push to `my-first-app/**`:
1. Check out the repo
2. Build the Docker image
3. Import the new image into k3s's containerd
4. `kubectl rollout restart deployment/my-first-app`

Verified end-to-end with a real push: a small HTML change went from commit to
live in both running pods, confirmed by exec-ing into a pod and reading the
file directly — not just a green checkmark in Actions.

## Real problems hit and fixed
- **Runner didn't survive after setup**: installed as a systemd service but
  never `enable`d, so it silently stopped and a later job hung indefinitely
  waiting for a runner that wasn't there. Fixed, and now boots automatically.
- **Memory exhaustion under combined load**: k3s + Docker + the runner + an
  active build together exceeded the instance's ~900MB RAM, causing hangs and
  misleading errors (a Docker Hub TLS timeout that was really memory
  starvation, not a network problem). Added a 1GB swap file rather than
  resizing the instance — a deliberate cost-vs-headroom call for a learning
  environment.
- **False-positive verification**: a leftover standalone container from the
  original Docker lesson was still bound to port 8080 in the background, so
  an early `curl`/`port-forward` check returned stale content and briefly
  looked like a failed deploy. Verified correctly by curling from inside the
  actual k3s pod instead of relying on a host port that could be shadowed.

## Key takeaway
A self-hosted runner trades GitHub's fully-managed build environment for full
control — and full responsibility for every tool, service, and resource
constraint on that box. That tradeoff, and the debugging it forced, is a real
infrastructure story worth being able to explain, not a workflow-file bug.
