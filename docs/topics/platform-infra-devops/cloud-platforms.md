# Cloud Platforms

Category: platform-infra-devops · Topic ID: cloud-platforms

## Sources

- [fetched] https://aws.amazon.com/what-is-cloud-computing/ — real content.
- [could not fetch] https://www.youtube.com/watch?v=M988_fsOSWo — title only, no transcript.
- [could not fetch] https://www.youtube.com/playlist?list=PLEiEAq2VkUUIJ3o1tehvtux0_Ynf42CBN — title only, no content.

## Findings

**What it is**: on-demand IT resource delivery over the internet with pay-as-you-go pricing —
compute, storage, databases provisioned as needed rather than maintained as owned physical
infrastructure.

**Three service models**: **IaaS** (most control — networking, virtual machines, storage; you
manage the applications and data yourself); **PaaS** (infrastructure concerns removed — deploy
and manage applications without touching hardware/maintenance); **SaaS** (fully managed
applications, e.g. web email — just use the software). This is the standard abstraction ladder
every specific provider (AWS/Azure/GCP, researched next) implements differently but maps onto.

**Key benefits**: agility (fast resource deployment → faster iteration); elasticity (scale up or
down to match real demand, not provisioned capacity); cost savings (pay for use, not idle
capacity); global reach (deploy close to users worldwide in minutes, cutting latency).

**Direct relevance to an FDE engagement**: which service model a client already uses (IaaS vs.
PaaS vs. SaaS) directly determines how much infrastructure work an FDE engagement needs to do
versus how much is already handled — a client fully on SaaS/PaaS tooling needs integration work,
not infrastructure provisioning; a client still on raw IaaS may need both.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
