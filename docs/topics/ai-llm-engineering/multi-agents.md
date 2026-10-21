# Multi-Agents

Category: ai-llm-engineering · Topic ID: multi-agents

## Sources

- [fetched] https://www.ibm.com/think/topics/multiagent-system — IBM's own explainer; real content.
- [fetched] https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems — Hugging Face's agents course page, with actual code patterns.
- [could not fetch] https://towardsdatascience.com/agentic-ai-103-building-multi-agent-teams/ — HTTP 403 Forbidden. This is the **third** towardsdatascience.com URL across this category's topics (`rags`, `mcp`, now this one) to fail the same way — looks like a systematic block against this fetch tool, not a one-off, worth treating as a known-bad source domain for future topics rather than re-discovering it each time.
- [could not fetch] https://www.youtube.com/watch?v=sWH0T4Zez6I — only the page title ("Multi Agent Systems Explained: How AI Agents & LLMs Work Together") recoverable, no transcript.

## Findings

**What a multi-agent system (MAS) actually is** (IBM): multiple AI agents collaborating toward a
shared objective, each with individual properties but behaving collaboratively — distinct from a
single agent merely calling other agents as tools, because in a true MAS the agents model each
other's goals and plans, not just invoke each other mechanically.

**Coordination mechanisms** (IBM): direct communication, indirect coordination via shared
environment state, shared learning (agents distribute learned experience so they don't each
redundantly re-learn the same policy), and specialized roles (agents develop domain expertise
rather than every agent being a generalist).

**Architecture patterns** (IBM): two primary network structures — **centralized** (a central unit
holds global knowledge; simpler, but a single point of failure) and **decentralized** (agents
coordinate with neighbors; more robust, harder to coordinate). Within either, agents can be
organized as hierarchies, "holons" (grouped entities treated as one), coalitions, or teams, each
trading off autonomy against interdependence differently.

**Concrete implementation pattern** (Hugging Face / smolagents): a manager/orchestrator agent
supervises specialized sub-agents (e.g. a web-search agent, a code-interpreter agent), composed
via a `managed_agents` parameter — e.g. `CodeAgent(model=model, managed_agents=[web_agent],
tools=[...])`. Concrete techniques named: splitting work by specialization to cut each agent's
own token usage (a web agent searches, a separate manager agent aggregates and visualizes);
`planning_interval=N` so an agent periodically stops to plan ahead rather than acting purely
reactively; `final_answer_checks` so a manager agent validates a sub-agent's output before
accepting it. The worked example (a "Batman filming locations" task) is explicitly framed around
why this helps: separating concerns "reduces the count of input tokens at each step, thus reducing
latency and cost" — a real efficiency argument, not just a modularity one.

**Direct relevance to this system**: Cimcime's own hierarchy (orchestrator → category-agents →
topic-agents, ADR-0002/ADR-0008) is itself a multi-agent system, and specifically a hierarchical,
largely centralized one in IBM's terms — Cimcime holds the dispatch authority, category-agents are
mid-level managers over their own topic-agents. The `managed_agents` composition pattern from the
Hugging Face source is a close technical analogue (though Cimcime's version coordinates through
shared repo state — GitHub Issues, per ADR-0004 — rather than in-process Python objects).

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
