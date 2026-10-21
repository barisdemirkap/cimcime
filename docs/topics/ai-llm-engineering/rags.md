# RAGs

Category: ai-llm-engineering · Topic ID: rags

## Sources

- [could not fetch] https://cloud.google.com/use-cases/retrieval-augmented-generation — page is truncated by the fetch tool before any body content; only the title ("What is Retrieval-Augmented Generation (RAG)? | Google Cloud") came through across three separate fetch attempts, including one explicitly asking for a verbatim quote of whatever text precedes the truncation. Likely a client-rendered page the fetch tool can't execute, same class of problem as roadmap.sh's own site.
- [could not fetch] https://towardsdatascience.com/rag-explained-understanding-embeddings-similarity-and-retrieval/ — HTTP 403 Forbidden. The site blocks this fetch tool outright.
- [could not fetch] https://www.youtube.com/watch?v=T-D1OfcDW1M — only the page title ("What is Retrieval-Augmented Generation (RAG)? - YouTube") recoverable; no transcript or description, as expected for YouTube pages fetched this way.

## Findings

None of this topic's three linked resources yielded readable source content in this environment —
this section is deliberately left without synthesized findings rather than filled in from
parametric/general knowledge, per the rule that findings must be traceable to a source actually
read. This is itself a real finding worth acting on: `rags`, and likely other topics sharing these
same domains (cloud.google.com, towardsdatascience.com, youtube.com), may need either a different
fetch mechanism (e.g. an authenticated/browser-based tool) or alternate resource links before a
genuine deep-dive is possible.

**Resolved** (see ADR-0007): a topic with zero fetchable sources stays `needs-research`, tagged
`fde:needs-better-sources`, rather than being marked `researched`. This issue carries that label.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
