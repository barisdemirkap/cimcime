# Memory & State Management

Category: ai-llm-engineering · Topic ID: memory-state-management

## Sources

- [fetched] https://arxiv.org/abs/2502.12110 ("A-MEM: Agentic Memory for LLM Agents") — real content, directly on-topic.
- [fetched, redirected] https://python.langchain.com/docs/how_to/chatbots_memory/ → 308-redirected to https://docs.langchain.com/oss/python/langchain/overview — real content fetched, but the redirect landed on LangChain's general framework overview rather than the specific memory guide originally linked (LangChain's docs have apparently been restructured); it mentions LangGraph "persistence" in passing but gives no memory implementation detail. Noted honestly as a partial/off-target result, not a full answer.
- [fetched] https://www.pinecone.io/learn/langchain-retrieval-augmentation/ — real content, but it's about RAG chunking/embeddings (overlapping with `rags.md`), and explicitly does not cover memory/state itself.
- [could not fetch] https://www.youtube.com/watch?v=VKPngyO0iKg — title only ("Building Brain-Like Memory for AI"), no transcript.

## Findings

**The one source that's actually about this topic** (arxiv.org, A-MEM paper): a dynamic memory
system for LLM agents applying Zettelkasten note-linking principles — new information becomes a
structured note (description, keywords, tags), the system finds and links related existing
memories, and critically supports **memory evolution**: a new addition can trigger updates to
*existing* memory entries, not just append new ones. The paper frames this as a shift from
passive storage-and-retrieval toward adaptive, context-aware memory, and reports it outperforms
existing approaches across six foundation models in testing.

**What the other two sources actually cover instead**: LangChain's current docs overview
(general framework composition, multi-provider support, LangGraph-based orchestration with
"persistence" mentioned but not detailed) and Pinecone's RAG/chunking/embedding walkthrough
(400-token chunks with 20-token overlap, `text-embedding-ada-002`, 1536-dim vectors) — both real,
useful content, but **neither one is actually about memory/state management**, this topic's
actual subject. Worth flagging as a resource-relevance gap in the source roadmap itself, distinct
from a fetch failure: the content exists and was read, it just doesn't answer the question the
topic title asks.

**Direct relevance to this system**: A-MEM's "memory evolution" idea — new information updating
existing entries rather than only appending — is structurally close to how this project's own
`GLOSSARY.md` and `docs/adr/*.md` work: ADR-0002 wasn't just appended to when ADR-0008 came
along, it was explicitly *edited in place* to note the amendment. The study files under
`docs/topics/` are the simpler, append-mostly form of memory (closer to a flat note store);
`GLOSSARY.md`/ADRs are the evolving, cross-linked form A-MEM describes.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
