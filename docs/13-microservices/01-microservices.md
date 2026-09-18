# 13 — Microservices: Independent Services on k3s

## What this covers
Splitting a monolith pattern into two genuinely independent services running
on the existing k3s cluster, communicating over the network, and deployable
one at a time — not two copies of the same static page.

## What was built
- **`backend-service`**: a small Python service (stdlib `http.server`, no
  framework) returning JSON with a live server timestamp — proves the backend
  actually computes something, not just a static string
- **`frontend-service`**: calls the backend over the network and renders the
  result as HTML. The backend's address is injected via a `BACKEND_URL`
  environment variable rather than hardcoded — the actual mechanic that
  separates config from code
- Each service has its own Dockerfile, its own Deployment (2 replicas), and
  its own Service — deployed the same way as `my-first-app`: built locally,
  imported into k3s's containerd, applied via `kubectl`

## Proving it's real, not just running
- A throwaway pod (`kubectl run --rm`) reached `backend-service` purely by
  its Service name — no IP addresses anywhere — confirming k3s's internal DNS
  actually resolves service-to-service traffic
- Exec'd into the frontend pod and hit its own endpoint, which in turn calls
  the backend internally: the response showed the backend's live message and
  timestamp, rendered by the frontend — the full call chain working
  end-to-end, not two services that happen to coexist

## Independent CI/CD
Extended the existing self-hosted GitHub Actions pipeline using
`dorny/paths-filter` to detect which service actually changed and only
rebuild that one:
- Push under `my-first-app/**` → only `my-first-app` rebuilds
- Push under `microservices/backend/**` → only the backend rebuilds
- Push under `microservices/frontend/**` → only the frontend rebuilds

Verified with a real push: changed only the backend's response message,
pushed, and confirmed in the Actions run that the backend steps ran while
the frontend and `my-first-app` steps were skipped — then confirmed the new
content live in the running backend pod. That's genuine independent
deployability, the actual point of microservices, not just an architecture
diagram.

## Real problem hit and fixed
The first automated run failed with `operation not permitted` on
`docker save`. Cause: a stale root-owned `.tar` file was left in `/tmp` from
earlier manual testing (`sudo docker save`), and the unprivileged runner
user couldn't overwrite a root-owned file. Cleared the leftover files and
re-ran — a reminder that manual root-run testing on a shared instance can
leave residue that breaks the unprivileged automated path later.

## Note: API gateway / Ingress
Not built here — Traefik was deliberately disabled earlier for memory
reasons on this `t3.micro`. Both services stay internal to the cluster,
reached only via `kubectl exec`/`kubectl run` for testing, consistent with
the project's no-open-ports approach throughout.

## Key takeaway
The distinguishing feature of microservices isn't "more than one service" —
it's that a change to one doesn't require rebuilding, retesting, or
redeploying the others. That's what the path-filtered CI/CD pipeline proves:
a real backend change only ever touched the backend, end to end.
