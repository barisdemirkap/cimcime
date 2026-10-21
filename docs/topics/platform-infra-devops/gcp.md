# GCP

Category: platform-infra-devops · Topic ID: gcp

## Sources

- [fetched] https://docs.cloud.google.com/docs — real content.
- [fetched] https://www.huntress.com/cybersecurity-101/topic/what-is-google-cloud-platform — real content, security-angle.
- [could not fetch] https://www.youtube.com/playlist?list=PLEiEAq2VkUUI0xT8VNpjBuWvmnLHxPcsE — title only, no content.

## Findings

**Featured products/categories** (docs.cloud.google.com): Cloud Run (serverless), Cloud
Storage, BigQuery (analytics), Compute Engine, Cloud SQL, Google Kubernetes Engine — spanning
serverless, data analytics, and infrastructure. Technology domains: AI/ML (genAI apps, agents,
model development — a first-class category here, same shift already noted in `azure.md`'s
AIaaS/MaaS service models), app development (APIs, CI/CD, source management), databases
(AlloyDB, Firestore), data analytics (BigQuery, Looker, orchestration), networking (VPC, load
balancing), security (IAM, encryption, compliance). Notably: **Terraform** is named explicitly
as GCP's own recommended infrastructure-as-code tool, not a GCP-specific alternative —
reinforcing `terraform.md`'s cross-provider positioning rather than contradicting it.

**Security framing, and an honest gap in this specific source** (huntress.com): GCP is
described as providing strong encryption and compliance as core strengths, but this particular
source doesn't go deep on cloud-specific threat classes (identity vulnerabilities, data
exfiltration, misconfiguration) — notable because the source itself (Huntress, a managed
security/threat-detection vendor) has an obvious reason to emphasize that built-in platform
security isn't sufficient alone. Worth reading that bottom-line claim as directionally
reasonable but somewhat self-interested, rather than a neutral assessment.

**Direct relevance to this system**: this is the third of three major clouds researched
(alongside `aws.md`/`azure.md`), and all three converge on the same structural shape — compute,
storage, managed databases, an AI/ML-specific service tier, and IaC tooling (native or
Terraform) — which is itself a useful finding: an FDE doesn't need deep expertise in all three
simultaneously, since the *shape* of the choice is consistent even when the specific product
names differ.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
