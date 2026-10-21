# AWS

Category: platform-infra-devops · Topic ID: aws

## Sources

- [could not fetch] https://roadmap.sh/aws — the roadmap.sh landing page, consistent with its client-rendered pages failing.
- [fetched] https://aws.amazon.com/getting-started/cloud-essentials/ — real content.
- [fetched] https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html — real content.
- [could not fetch] https://www.youtube.com/watch?v=3hLmDS179YE — title only, no transcript.

## Findings

**Origin and scale** (AWS whitepaper): AWS began in 2006 as the first mainstream cloud-computing
offering; now over 200 distinct services, powering businesses across 190 countries. The core
economic shift it enabled: trading upfront capital infrastructure expense for low variable cost
that scales with actual usage — no more weeks/months of procurement lead time before a server
exists.

**Interaction surfaces** (cloud-essentials): AWS Management Console (web UI), AWS CLI,
SDKs (programmatic), IDE toolkits — the same tool/interface variety most major platforms offer,
useful to know by name when a client mentions which one their team actually uses day to day.

**Infrastructure as Code, two named frameworks**: **AWS CDK** (define infrastructure using a
real programming language, not a bespoke config format) and **AWS CloudFormation** (declarative
templates describing the desired state of AWS resources). This is the direct AWS-specific
analogue to `terraform.md` (researched next in this category) — Terraform is provider-agnostic,
CDK/CloudFormation are AWS-native; an FDE needs to know which one a given client has already
standardized on rather than assuming.

**Security model, directly relevant to an engagement's compliance posture**: the **shared
responsibility model** — AWS secures the underlying infrastructure, the customer secures their
own data and applications on top of it. Misunderstanding where that line falls is a common real
source of security gaps. The **Well-Architected Framework** names six pillars: operational
excellence, security, reliability, performance, cost optimization, sustainability — a useful
checklist structure for reviewing any AWS-based architecture, not just a marketing term.

**Direct relevance to this system**: the shared responsibility model is the cloud-infrastructure
version of this project's own ADR-0001 approval-gate boundary — Cimcime (the "platform")
operates autonomously within its sandbox, but production deploy/real spend/real third-party
communication are explicitly the human's responsibility to approve, same shape as "AWS secures
infrastructure, you secure what you put on it."

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
