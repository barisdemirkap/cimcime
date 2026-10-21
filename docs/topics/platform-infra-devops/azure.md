# Azure

Category: platform-infra-devops · Topic ID: azure

## Sources

- [fetched] https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-azure — real content.
- [fetched] https://learn.microsoft.com/en-us/azure/?product=popular — real content.
- [could not fetch] https://www.youtube.com/playlist?list=PLEiEAq2VkUUKihhGvJw05bU8DhoQMn_ni — title only, no content.
- [could not fetch] https://www.youtube.com/watch?v=5abffC-K40c — title only, no transcript.

## Findings

**What it is**: Microsoft's cloud platform, launched 2010, 200+ products/services across
datacenters in 70+ regions, serving 95% of Fortune 500 companies (azure.microsoft.com's own
cited figure). Strong open-source support (Linux distros, Kubernetes, PostgreSQL) despite being
a Microsoft product.

**Beyond the standard three service models**: azure.microsoft.com names IaaS/PaaS/SaaS plus
two additional ones — **AIaaS** (AI-as-a-Service) and **MaaS** (Models-as-a-Service) — a useful
update to `cloud-platforms.md`'s three-model framing, reflecting how AI-specific offerings have
become distinct enough to need their own category rather than fitting inside PaaS.

**Headline service categories** (learn.microsoft.com): AI/ML (Azure OpenAI Service, Azure
Machine Learning, Azure Databricks, Document Intelligence, AI Search); compute (App Service,
Azure Functions, AKS, VMs); data/analytics (Synapse Analytics, Data Factory, Data Lake Storage,
Microsoft Fabric); databases (Azure SQL, Cosmos DB, managed PostgreSQL/MySQL, Redis cache);
networking/security (Firewall, DDoS Protection, ExpressRoute, Microsoft Defender for Cloud, Key
Vault for secrets); developer tooling (Azure DevOps — Pipelines/Repos/Boards, Container
Registry).

**Direct relevance to an FDE engagement**: **Key Vault** is Azure's answer to this project's own
gitignored `secrets/` convention — if an engagement is Azure-native, secrets belong in Key Vault
rather than environment files, same underlying principle ("never commit a secret, use a
dedicated mechanism") as `openclaw.md`'s security-best-practices findings, just the Azure-native
implementation of it.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
