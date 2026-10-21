# Security

Category: platform-infra-devops · Topic ID: security

## Sources

- [could not fetch] https://roadmap.sh/cyber-security — the roadmap.sh landing page, consistent with its client-rendered pages failing.
- [fetched] https://www.paloaltonetworks.com/cyberpedia/what-is-llm-security — real content, directly on-topic for an AI-agent system specifically.
- [could not fetch] https://www.youtube.com/watch?v=gUNXZMcd2jU — title only ("OWASP's Top 10 Ways to Attack LLMs"), no transcript.

## Findings

**What LLM security specifically covers**: protecting AI systems/applications from
unauthorized access, misuse, and exploitation across development, deployment, and operation —
distinct from traditional application security because LLM systems take freeform input and
produce probabilistic output, rather than predictable inputs through defined data flows,
requiring different threat models entirely.

**OWASP's Top 10 for LLM Applications — the six risks named**: **prompt injection** (crafted
input overrides the model's real instructions); **data exposure** (the model leaks
personal/business/proprietary info through its own outputs); **supply chain threats** (hidden
vulnerabilities in third-party components); **data poisoning** (manipulated training data biases
the model or implants a backdoor); **excessive agency** (an over-privileged system executes
unsafe actions across connected platforms — this is, essentially verbatim, the exact risk
ADR-0001's three approval gates exist to contain); **misinformation** (treating model output as
automatically authoritative leads to bad decisions downstream).

**Layered defense practices named**: input controls (filter/sanitize prompts and metadata from
every source); model isolation (sandbox execution to cap the damage if compromised — the same
sandboxing concept `docker.md` and `openclaw.md`/`claude-code.md` already flagged as real
options for this system's own Mac Mini deployment); output validation (classify/validate a
response before it's actually delivered/acted on); capability restriction (limit tool access to
only what's essential — the same "narrow, non-overlapping tools" principle
`context-engineering.md` already named from Anthropic's own guidance); supply-chain integrity
(verify model/component sources before deployment); training-data vetting (scan fine-tuning
data for malicious content or sensitive leakage); RAG-specific filtering on retrieval sources
(directly connects to `rags.md`).

**Direct, concrete relevance to this system — the single most on-the-nose finding in this whole
category**: "excessive agency" is the formal security term for exactly the failure mode ADR-0001
was built to prevent. This project's three approval gates (production deploy, real third-party
communication, real spend/account changes) are a direct, working mitigation for this named
OWASP risk — not an analogy this time, but the literal textbook control for the literal named
threat.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
