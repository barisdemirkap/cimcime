# DevSecOps

Category: platform-infra-devops · Topic ID: devsecops

## Sources

- [could not fetch] https://roadmap.sh/devsecops — the roadmap.sh landing page, consistent with its client-rendered pages failing.
- [fetched] https://www.redhat.com/en/topics/devops/what-is-devsecops — real content.
- [fetched] https://aws.amazon.com/what-is/devsecops/ — real content, independently converging.
- [could not fetch] https://www.youtube.com/watch?v=JfiWi8RjN-8 — title only, no transcript.

## Findings

**What it is, converging across both sources**: security as a shared responsibility woven
through the entire development lifecycle, not a final checkpoint before release. Traditional
DevOps treated security as a late-stage gate that created bottlenecks under rapid delivery;
DevSecOps embeds it from the start instead.

**"Shift left, shift right"** — named independently by both sources as the core strategy: shift
left means catching vulnerabilities early (during development, not after); shift right means
extending monitoring into production rather than stopping at deployment. Vulnerabilities caught
early cost less and take less time to fix — the same "fix it at the earliest possible stage"
economics already seen in `requirements-gathering.md` (37% of failures from bad requirements)
and `inference-optimization.md`'s baseline-first principle, now applied to security specifically.

**Concrete security practices** (redhat.com): inviting security teams in early rather than at
the end; training developers in secure coding directly (not relying only on a separate security
team); supply-chain risk analysis; automated container scanning, static analysis during builds,
automated patching, configuration-compliance checks — automation specifically to avoid security
work becoming a manual bottleneck in a fast pipeline. Cloud-native/container-specific
safeguards: least-privilege standardized environments, centralized identity/access control,
encryption in transit and at rest, secure API gateways, CI/CD-integrated security.

**AWS's concrete tooling example**: Amazon Inspector (vulnerability management), AWS
CodeCommit (source control), **AWS Secrets Manager** (credential protection) — another
cloud-native implementation of the same "never hardcode a secret" principle already seen in
`azure.md`'s Key Vault and `terraform.md`'s backend best practices.

**Named implementation challenge** (AWS): cultural resistance and the friction of integrating
multiple security tools into existing workflows — echoing `devops-skills.md`'s own point that
DevOps (and by extension DevSecOps) is as much a culture problem as a tooling one.

**Direct relevance to this system**: this project's own `secrets/` convention, the three
ADR-0001 approval gates, and the two-axis code review running *before* every commit (not after)
are all DevSecOps practices applied to an AI-agent system instead of a human engineering team —
security/safety reviewed continuously through the work, never bolted on as an afterthought.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
