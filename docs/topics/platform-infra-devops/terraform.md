# Terraform

Category: platform-infra-devops · Topic ID: terraform

## Sources

- [fetched] https://roadmap.sh/terraform — real content (another roadmap.sh landing page that rendered this time).
- [fetched] https://developer.hashicorp.com/terraform — real content, the official overview.
- [fetched] https://roadmap.sh/terraform/backend — real content, the most technically substantive source here.
- [could not fetch] https://www.youtube.com/watch?v=7xngnjfIlK4 — title only, no transcript.

## Findings

**What it is**: HashiCorp's infrastructure-as-code tool — define cloud infrastructure (servers,
databases, networking, DNS) in configuration files, provision/destroy via commands rather than
manual console clicks, provider-agnostic across AWS/Azure/GCP/Oracle Cloud/Docker and others.
This is the cross-provider counterpart to the AWS-native CDK/CloudFormation already found in
`aws.md`, and GCP's docs (`gcp.md`) name Terraform as its own recommended IaC tool too —
confirming Terraform's role as the common choice when a client's infrastructure spans more than
one provider.

**Terraform state and backends — the most directly relevant finding in this whole category**
(roadmap.sh/terraform/backend): a backend is "the system Terraform uses to store and manage
your infrastructure state data" — controls where `.tfstate` lives and how teams share access.
**Local backend** (default): on-disk, no locking, poor for team use. **Remote backend**
(production): cloud storage (S3/Azure Blob/GCS) with state **locking** (prevents concurrent
writes from corrupting the state) plus versioning/backup. Critical best practices named:
**never commit state files to git**, enable object versioning for disaster recovery, use
environment variables for credentials (never hardcoded), encrypt state in transit and at rest,
keep separate state files per environment to limit blast radius.

**Direct, almost one-to-one relevance to this system's own ADR-0004**: Terraform's state/backend
problem — where does the single source of truth for "what currently exists" live, local vs.
remote, with locking to prevent concurrent corruption — is *exactly* the problem ADR-0004
solved for this project with GitHub Issues as the state-store source of truth and an optional
Postgres mirror. "Never commit state files to git" looks like it contradicts this project's own
choice (state *does* live in git-adjacent GitHub Issues) — but the resolution is the same
distinction Terraform itself draws: Terraform's own state file is forbidden in git because it's
mutable, frequently-written, and lock-sensitive data (closer to a database); this project's
`GLOSSARY.md`/`docs/adr/` *are* committed to git because they're append-mostly, rarely-conflicting
knowledge, while the actual frequently-mutated state (topic status, phase) lives in GitHub
Issues specifically, not in a git-tracked file — the same category distinction Terraform draws
between state (never git) and configuration (always git), just mapped onto this project's own
two kinds of persisted data.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
