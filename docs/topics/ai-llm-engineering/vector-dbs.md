# Vector DBs

Category: ai-llm-engineering · Topic ID: vector-dbs

## Sources

- [fetched] https://developers.cloudflare.com/vectorize/reference/what-is-a-vector-database/ — real content (a different Cloudflare path than the blocked `llm-fundamentals.md` one — this one worked).
- [fetched] https://www.mongodb.com/resources/basics/databases/vector-databases — real content.
- [could not fetch] https://www.youtube.com/watch?v=gl1r1XV0SLw — title only, no transcript.
- [could not fetch] https://www.youtube.com/watch?v=mHxLXzYjQRE — title only, no transcript.

## Findings

**What they are**: databases that store and search data as high-dimensional vectors, enabling
similarity search (semantic closeness) rather than exact-match/keyword lookup. Cloudflare's
framing: they act as "long-term memory for AI applications," avoiding re-processing an entire
dataset through a model on every query.

**Core mechanics**: data is converted to **embeddings** (numerical vectors from an ML model,
commonly 768 dimensions for text) and stored in an index; a query is embedded with the *same*
model, then the nearest stored vectors are retrieved via a distance metric — cosine similarity
(works well for text), Euclidean distance (suits image recognition), or dot product. Retrieval
at scale uses Approximate Nearest Neighbor algorithms (mongodb.com names HNSW specifically)
rather than exact nearest-neighbor search, trading a small accuracy cost for large speed gains.

**Use cases, converging across both sources**: semantic search, recommendation systems, anomaly
detection, and RAG (retrieval-augmented generation — directly connecting to `rags.md`'s earlier
findings). mongodb.com adds image/video recognition and drug discovery as less-obvious
applications, and highlights **hybrid search** (vector + text + structured filters combined) as
its own specific capability.

**Direct relevance to this system**: this project doesn't currently use a vector database — its
"retrieval" is a plain-text, structural lookup (GitHub Issues filtered by label, study files
found by filename) rather than semantic similarity search. That's a deliberate, correct choice
for *this* system's scale (97 topics is small enough for exact lookups to suffice), but it's
worth naming explicitly: if this project's knowledge base grew to the point where an agent
needed to find "topics semantically related to X" rather than "topics in category Y," a vector
store over the study-file contents would be the natural next tool, not a redesign of the
existing GitHub-Issues state store.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
