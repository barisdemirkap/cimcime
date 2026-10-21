# Kubernetes

Category: platform-infra-devops · Topic ID: kubernetes

## Sources

- [fetched] https://roadmap.sh/kubernetes — real content this time (unlike most roadmap.sh landing pages, this one's intro blurb rendered).
- [fetched] https://kubernetes.io/docs/home/ — real content, the official docs.
- [could not fetch] https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes — the fetch tool explicitly reported it only got navigation/footer content, no article body, and correctly declined to fabricate a substitute.
- [could not fetch] https://www.youtube.com/watch?v=X48VuDVv0do — title only, no transcript.

## Findings

**What it is**: an open-source container orchestration engine (CNCF-hosted) that automates
deployment, scaling, and management of containerized applications — roadmap.sh's summary adds
self-healing, service discovery, automated rollout/rollback, and consistent operation across
multi-cloud/hybrid environments as the headline capabilities.

**Core architecture concepts** (kubernetes.io): cluster = control-plane nodes managing worker
nodes; **Pods** are the smallest deployable unit (one or more containers); higher-level
workload abstractions (Deployments, StatefulSets, DaemonSets, Jobs) sit on top of pods; Services
expose/load-balance pod traffic; persistent volumes + storage classes handle data; **ConfigMaps
and Secrets** handle application configuration — the Kubernetes-native equivalent of this
project's own gitignored `secrets/` convention, same underlying principle (don't bake config
into the image/code) with a cluster-native mechanism.

**Key tooling**: `kubectl` (CLI for cluster interaction), `kubeadm` (bootstrap a production
cluster), the Kubernetes API itself (RESTful, everything in the cluster is ultimately an API
operation).

**Direct relevance to this system**: Kubernetes' **self-healing** feature (restart failed
containers, reschedule pods automatically) is the infrastructure-level analogue to this
project's own reliance on idempotent, re-runnable operations (`seed`'s safe-to-rerun guarantee,
`_find_or_create_*` helpers) — both solve "recover automatically from a failure without a human
noticing" via the same underlying design instinct (make the recovery action safe to just redo),
just at different layers of the stack.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
