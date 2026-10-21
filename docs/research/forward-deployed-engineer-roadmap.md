# Forward Deployed Engineer Roadmap — Research Notes

- **Source**: https://roadmap.sh/forward-deployed-engineer (client-rendered; not directly scrapable)
- **Content mirror used**: https://github.com/nilbuild/developer-roadmap/tree/main/roadmaps/forward-deployed-engineer/content (this is the repo id `kamranahmedse/developer-roadmap` now redirects to — the authoritative content source for the roadmap)
- **Fetched**: 2026-10-21
- **Topic count**: 97 content files, all fetched successfully.
- **Note on structure**: the mirror repo has no separate layout/grouping file for this roadmap (no JSON/graph definition found anywhere else in the repo tree) — only the flat `content/` folder of per-topic markdown. The categories and ordering below are inferred from reading every topic's actual content, not from roadmap.sh's visual layout, which may group things slightly differently.

---

## 1. FDE Role & Career Path

### Introduction
A Forward Deployed Engineer works directly inside a customer's environment to build, deploy, and stabilize AI systems. The role originated at Palantir, where engineers called "Deltas" embedded with clients (sometimes on military bases) to ship code overnight based on same-day field feedback. The same model now underpins how OpenAI, Anthropic, and others bring AI into large enterprises. It demands technical depth, fast codebase comprehension, and the communication skill to explain AI's capabilities and limits to non-technical decision makers.
- [@article@Forward deployed engineer is AI's hottest job](https://thenewstack.io/forward-deployed-engineer-fde-openai-google/)
- [@article@Forward-deployed engineer: The complete guide](https://www.rocketlane.com/blogs/forward-deployed-engineer)
- [@video@How to Become a Forward Deployed Engineer in 2026](https://www.youtube.com/watch?v=vLlIBT0HSSc)
- [@video@Forward Deployed Engineer Full Course](https://www.youtube.com/playlist?list=PLWSlr9idVBc0)

### The Delta
"The Delta" is Palantir's original term for what is now called an FDE: the gap between what a software product does out of the box and what a specific customer actually needs. It's both a role (the engineer who closes the gap) and a concept (the custom work needed to make a product fit a real environment). FDE interviews often ask candidates to identify "the Delta" in a given customer scenario.
- [@article@A Comprehensive Analysis of Palantir's Forward Deployed Engineering Model](https://medium.com/activated-thinker/a-comprehensive-analysis-of-palantirs-forward-deployed-engineering-model-4502a036b5e4)
- [@article@How Palantir Invented the Forward Deployed Engineer Model and Why AI Startups Are Adopting It](https://fde.academy/blog/how-palantir-invented-the-forward-deployed-engineer-model)

### Embedded Engineering
Describes the physical/organizational model of an FDE engagement: the engineer is embedded inside the customer's team rather than working remotely or at arm's length — joining their Slack, attending their standups, working in their codebase, and being present where the problems actually live.
- [@article@What Is Forward Deployment Engineering?](https://optywise.com/forward-deployment-engineering)
- [@article@Forward Deployed AI Engineers: What They Are and When You Need One](https://www.futureproofing.dev/resources/ai-native-team/forward-deployed-ai-engineers)

### Roles & Responsibilities
The FDE job runs in three phases. **Audit**: embed with different teams, map workflows, find bottlenecks, decide where AI creates real value (and where it doesn't). **Evals**: build systems that measure whether the AI actually reasons through problems the way a skilled human would, not just whether it produces an answer. **Deployment**: ship into production starting with the smallest possible unit of autonomy, layering on capability only after each step is proven.
- [@article@Forward Deployed Engineer (FDE): What Is It, Skills and Scope](https://fde.academy/blog/forward-deployed-engineer)
- [@article@Forward Deployed Engineer: The Complete 2026 Report — Origin, Demand, Roles, Salary & More](https://www.uplers.com/article/forward-deployed-engineer-guide/)
- [@video@This Is How Forward Deployed Engineering Is Actually Done](https://www.youtube.com/watch?v=AD-EmZ3v6-g)

### FDE Tiers
The job market has split into three tiers with different skill emphases. **AI lab FDEs**: deep ML fluency, strong agent-architecture skills, help customers adopt models in production. **Enterprise software FDEs**: data-platform depth, integration experience, connecting a vendor's product to a customer's existing data infrastructure. **Consulting/staffing FDEs**: broad solutions-architecture skills, account-management instincts, ability to run an end-to-end engagement independently. Which tier you're targeting should shape which parts of this roadmap you prioritize.
- [@article@How AI Labs Are Solving The Last Mile Problem](https://www.forbes.com/sites/gelilabekele/2026/09/04/ai-deployment-and-the-forward-deployed-engineering-model/)
- [@article@Forward Deployed roles: the emerging job family](https://forwarddeployedcreative.com/forward-deployed-roles/)
- [@article@AI Engineers, Applied Scientists, Forward Deployed Engineers: Let's Unpack.](https://towardsdatascience.com/ai-engineers-applied-scientists-forward-deployed-engineers-lets-unpack/)

### From X to FDE
Three backgrounds transition well: software engineers, consultants, and product managers. Engineers have the technical base but often need to learn to communicate AI tradeoffs to non-technical stakeholders and build a portfolio proving they can own a full deployment, not just write code. Consultants/PMs already translate data into business outcomes (half the job) but need to close the engineering gap by building real agents, RAG pipelines, and eval frameworks from scratch.
- [@article@How to Become a Forward Deployed Engineer](https://fde.academy/blog/how-to-become-a-forward-deployed-engineer)
- [@article@How to Transition from a Developer or Architect to AI FDE roles](https://newsletter.bigtechcareers.com/p/how-to-transition-from-a-developer)
- [@article@The Definitive Guide to Forward Deployed Engineer Interviews in 2026](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026)

---

## 2. Core Software Engineering Foundations

### Learn a Programming Language
Mastering the syntax, semantics, and standard libraries of a language — from fundamentals (variables, types, control flow, functions) to idiomatic, maintainable patterns.
- [@article@Best Programming Languages to Learn for an FDE Role](https://fde.academy/blog/best-programming-languages-to-learn-for-an-fde-role)
- [@article@The Forward Deployed Engineer Tech Stack: Tools, Languages, and Frameworks](https://fde.academy/blog/forward-deployed-engineer-tech-stack)
- [@article@The Exact Tools, Languages and Frameworks Forward Deployed Engineers Rely On](https://www.scaler.com/topics/forward-deployed-engineer-tools-frameworks-language/)

### Python
General-purpose, readable, with a broad ecosystem spanning web dev, data engineering, scripting, automation, and AI/ML.
- [@roadmap@Dedicated Python Developer Roadmap](https://roadmap.sh/python)
- [@article@Tutorial Series: How to Code in Python](https://www.digitalocean.com/community/tutorials/how-to-write-your-first-python-3-program)
- [@article@Google's Python Class](https://developers.google.com/edu/python)
- [@video@Learn Python - Full Course](https://www.youtube.com/watch?v=4M87qBgpafk)

### JavaScript
Runs in browsers for dynamic page behavior and interactions; via Node.js it also runs server-side, enabling one language across the full web stack.
- [@roadmap@Dedicated JavaScript Roadmap](https://roadmap.sh/javascript)
- [@course@JavaScript Essentials 1](https://www.netacad.com/courses/javascript-essentials-1?courseLang=en-US)
- [@official@JavaScript MDN Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [@video@JavaScript Tutorial Full Course - Beginner to Pro](https://www.youtube.com/watch?v=EerdGm-ehJQ)

### JavaScript / TypeScript
TypeScript is a typed superset of JavaScript, catching errors at compile time and improving maintainability at scale. Together, JS/TS are the dominant choice for full-stack web development.
- [@roadmap@Dedicated JavaScript Roadmap](https://roadmap.sh/javascript)
- [@roadmap@Dedicated TypeScript Roadmap](https://roadmap.sh/typescript)
- [@official@Overview of TypeScript](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)
- [@official@JavaScript Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [@video@JavaScript Crash Course](https://www.youtube.com/watch?v=XIOLqoPHCJ4)
- [@video@Learn TypeScript – Crash Course for Beginners](https://www.youtube.com/watch?v=ZvZ7gvcmPmI)

### Java / Scala
Java is a statically typed, OOP, JVM language widely used in enterprise systems, backend services, and Android. Scala, also JVM-based, blends OOP and functional styles and is common in Spark-based data processing.
- [@roadmap@Dedicated Java Developer Roadmap](https://roadmap.sh/java)
- [@roadmap@Dedicated Scala Developer Roadmap](https://roadmap.sh/scala)
- [@video@Java Basics – Crash Course](https://www.youtube.com/watch?v=GdzRzWymT4c)
- [@video@Scala Crash Course by a Scala Veteran](https://www.youtube.com/watch?v=-xRfJcwhy7A)

### Go
Statically typed, compiled, built by Google for simplicity and performance; common for backend services, CLIs, and cloud infra. Its goroutine/channel concurrency model suits network-heavy, distributed workloads.
- [@roadmap@Dedicated Go Roadmap](https://roadmap.sh/golang)
- [@official@Go Documentation](https://go.dev/doc/)
- [@official@Get Started with Go](https://go.dev/doc/tutorial/getting-started)
- [@video@Learn GO Fast: Full Tutorial](https://www.youtube.com/watch?v=8uiZC0l4Ajw)

### Rust
Systems language focused on safety, speed, and concurrency; its ownership model with strict compile-time checks prevents bugs like null dereferences and buffer overflows without a garbage collector — high-level ergonomics with C++-level performance.
- [@roadmap@Dedicated Rust Roadmap](https://roadmap.sh/rust)
- [@official@Rust by Example](https://doc.rust-lang.org/stable/rust-by-example/index.html)
- [@opensource@Rust Book](https://edu.anarcho-copy.org/Programming%20Languages/Rust/rust-programming-language-steve-klabnik.pdf)
- [@video@Rust Crash Course Tutorial for Beginners](https://www.youtube.com/playlist?list=PLPoSdR46FgI412aItyJhj2bF66cudB6Qs)

### C++
High-performance, statically typed, with fine-grained control over memory/system resources; used in systems programming, game engines, embedded software, and performance-critical applications.
- [@roadmap@Dedicated C++ Developer Roadmap](https://roadmap.sh/cpp)
- [@article@Learn C++](https://www.learncpp.com/)
- [@article@C++ vs. C: When (and when not) to use each language](https://roadmap.sh/cpp/vs-c)
- [@video@C++ Tutorial for Beginners - Full Course](https://youtu.be/vLnPwxZdW4Y)

### HTML
The standard markup language for structuring web content (headings, paragraphs, links, forms, images); the foundation CSS and JavaScript build on.
- [@roadmap@Dedicated HTML Roadmap](https://roadmap.sh/html)
- [@article@HTML MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [@article@What is HTML – Definition and Meaning](https://www.freecodecamp.org/news/what-is-html-definition-and-meaning/)
- [@video@HTML Tutorial for Beginners: HTML Crash Course](https://www.youtube.com/watch?v=qz0aGYrrlhU)

### CSS
Controls visual presentation of HTML — layout, color, typography, spacing, animation, responsive design. Modern CSS (Flexbox, Grid, custom properties) enables complex adaptive layouts.
- [@roadmap@Dedicated CSS Roadmap](https://roadmap.sh/css)
- [@article@Web.dev by Google — Learn CSS](https://web.dev/learn/css/)
- [@video@CSS Tutorial – Full Course for Beginners](https://www.youtube.com/watch?v=OXGznpKZ_sA&t=25s)

### React
Component-based JavaScript library for building UIs; each component manages its own state/rendering and components compose into full interfaces. One of the most widely used frontend frameworks in production.
- [@roadmap@Dedicated React Developer Roadmap](https://roadmap.sh/react)
- [@official@React Docs](https://es.react.dev/index)
- [@article@Introduction to React](https://www.w3schools.com/react/react_intro.asp)
- [@video@React Tutorial Full Course - Beginner to Pro](https://www.youtube.com/watch?v=TtPXvEcE11E)

### Frontend
Covers HTML/CSS/JS for what users see and interact with in-browser. FDEs who can build functional frontends are more self-sufficient — able to deliver end-to-end demos and prototypes without a separate frontend team.
- [@article@What Is Front-End Development?](https://www.coursera.org/articles/what-is-front-end-development)
- [@video@Introduction to Front End Development](https://www.simplilearn.com/front-end-developer-free-course-skillup)
- [@video@Front End Developer Learning Path](https://www.youtube.com/playlist?list=PLWKjhJtqVAbmMuZ3saqRIBimAKIMYkt0E)

### Backend
Server-side logic: handling requests, running business logic, talking to databases, returning responses — typically Python/Node.js/Java/Go connected to databases and external services. Owning backend lets an FDE own full feature delivery, not just hand off at the API boundary.
- [@article@What is backend? A comprehensive intro to server-side development](https://alokai.com/blog/what-is-backend)
- [@video@How The Backend Works](https://www.youtube.com/watch?v=4r6WdaY3SOA)
- [@video@Complete Backend Course](https://www.youtube.com/watch?v=rOpEN1JDaD0)

### Node.js
JavaScript runtime on Chrome's V8 engine for server-side JS; non-blocking, event-driven architecture suited to I/O-heavy workloads (APIs, real-time apps, data streaming).
- [@roadmap@Dedicated Node.js Developer Roadmap](https://roadmap.sh/nodejs)
- [@official@Node.js - Getting Started](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
- [@article@Node.js Introduction](https://www.w3schools.com/nodejs/nodejs_intro.asp)
- [@video@Node.js Crash Course](https://www.youtube.com/watch?v=32M1al-Y6Ag)

### Git & GitHub
Distributed version control tracking code changes and enabling collaboration without overwriting each other's work; GitHub adds pull requests, review, issue tracking, and CI/CD. Standard in nearly every dev workflow.
- [@roadmap@Dedicated Git and GitHub Roadmap](https://roadmap.sh/git-github)
- [@official@Getting Started - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [@article@What is version control?](https://www.atlassian.com/git/tutorials/what-is-version-control)
- [@video@Git & GitHub Crash Course for Beginners](https://www.youtube.com/watch?v=mAFoROnOfHs)

### Data Structures & Algorithms
Arrays, linked lists, trees, graphs, hash maps, and the step-by-step procedures (sorting, searching, traversal) built on them. Knowing these well means being able to evaluate performance characteristics, debug inefficiencies in customer systems, and reason clearly about solutions.
- [@article@What is System Design?](https://algomaster.io/learn/system-design/what-is-system-design)
- [@article@Data Structures and Algorithms (DSA) Tutorial](https://www.tutorialspoint.com/data_structures_algorithms/index.htm)
- [@video@What Are Data Structures?](https://www.youtube.com/watch?v=bum_19loj9A)
- [@video@Learn Data Structures and Algorithms Visually – Crash Course](https://www.youtube.com/watch?v=RpLnQnurpLY)

### APIs Design
Defining how services communicate through well-structured interfaces: choosing protocol (REST/GraphQL/gRPC), clear resource models, consistent error handling, careful versioning. Good design is predictable, easy to use, and stable.
- [@roadmap@Dedicated API Design Roadmap](https://roadmap.sh/api-design)
- [@article@What is API design?](https://www.ibm.com/think/topics/api-design)
- [@video@APIs for Beginners - How to use an API (Full Course)](https://www.youtube.com/watch?v=WXsD0ZgxjRw)

### GraphQL
Query language/runtime letting clients request exactly the fields they need instead of fixed-shape endpoints — reduces over-fetching, adds flexibility, especially useful for frontend-heavy apps with variable data needs.
- [@roadmap@Dedicated GraphQL Roadmap](https://roadmap.sh/graphql)
- [@official@Introduction to GraphQL](https://graphql.org/learn/)
- [@official@Getting started with GraphQL](https://graphql.org/)
- [@video@GraphQL Course for Beginners](https://www.youtube.com/watch?v=5199E50O7SI)

### Authentication
Verifying identity (passwords, API keys, OAuth 2.0, JWTs) — distinct from authorization, which governs what an authenticated user can do. Foundational to securing any app handling user data or sensitive operations.
- [@article@Basic Authentication](https://roadmap.sh/guides/basic-authentication)
- [@article@Session Based Authentication](https://roadmap.sh/guides/session-based-authentication)
- [@article@Token Based Authentication](https://roadmap.sh/guides/token-authentication)
- [@article@JWT Authentication](https://roadmap.sh/guides/jwt-authentication)

### API Security
Protecting APIs from unauthorized access/abuse: authentication, authorization, rate limiting, input validation, defenses against injection/replay attacks. Poorly secured APIs are a common production attack vector.
- [@article@OWASP Project API Security](https://owasp.org/API-Security/editions/2023/en/0x00-toc/)

### SQL
The standard language for relational databases — create/read/update/delete records, define table structure and relationships. Foundational for any relational-data work.
- [@roadmap@Dedicated SQL Roadmap](https://roadmap.sh/sql)
- [@course@Complete Course to Master Practical SQL](https://roadmap.sh/courses/sql)
- [@article@SQL Tutorial](https://www.sqltutorial.org/)
- [@video@Learn SQL In 60 Minutes](https://www.youtube.com/watch?v=p3qvj9hO_Bo)

### PostgreSQL
Open-source relational database with advanced features (JSONB, full-text search, window functions, custom types) — a widely used default in both startups and large orgs.
- [@roadmap@Dedicated PostgreSQL DBA Roadmap](https://roadmap.sh/postgresql-dba)
- [@official@PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [@article@Introduction to PostgreSQL](https://www.w3schools.com/postgresql/postgresql_intro.php)
- [@video@Learn PostgreSQL Tutorial - Full Course for Beginners](https://www.youtube.com/watch?v=qw--VYLpxG4)

### NoSQL Databases
Stores data outside traditional tables (documents, key-value, graph, wide-column) — MongoDB, Redis, Cassandra, DynamoDB — chosen for high write throughput, flexible schema, or horizontal scalability.
- [@roadmap@Dedicated MongoDB Roadmap](https://roadmap.sh/mongodb)
- [@roadmap@Dedicated Redis Roadmap](https://roadmap.sh/redis)
- [@article@Types of NoSQL Databases: How to Choose the Right One](https://roadmap.sh/backend/types-of-nosql-databases)
- [@video@How do NoSQL Databases work](https://www.youtube.com/watch?v=0buKQHokLK8)
- [@video@SQL vs NoSQL Explained](https://www.youtube.com/watch?v=ruz-vK8IesE)

### Linux
Open-source OS underlying most production software, servers, and cloud environments. Comfort navigating Linux, managing processes, reading logs, and configuring services is a practical necessity for real deployments.
- [@course@Linux for Noobs](https://labex.io/courses/linux-for-noobs)
- [@article@Practice Linux Fundamentals](https://labex.io/linuxjourney)
- [@video@Linux Fundamentals](https://www.youtube.com/watch?v=kPylihJRG70)
- [@video@Bash Scripting Tutorial for Beginners](https://www.youtube.com/watch?v=tK9Oc6AEnR4)

---

## 3. AI & LLM Engineering

### LLM Fundamentals
LLMs are trained on huge text corpora to generate, summarize, classify, and reason about language by predicting next tokens given context. Understanding their limits — hallucination, context length, latency — is the foundation for building reliable systems around them.
- [@article@What is a large language model (LLM)?](https://www.cloudflare.com/en-gb/learning/ai/what-is-large-language-model/)
- [@article@New to LLMs? Start Here](https://towardsdatascience.com/new-to-llms-start-here/)
- [@video@How Large Language Models Work](https://www.youtube.com/watch?v=5sLYAQS9sWQ)

### AI Engineering Skills
Building software that uses ML/LLMs as components: selecting models, integrating via APIs, prompt engineering, context management, deploying AI features to production. This is the core of the FDE job — turning a model into a product that runs reliably inside a company's infrastructure.
- [@article@What Is an AI Engineer? (And How to Become One)](https://www.coursera.org/articles/ai-engineer)
- [@video@A Practical Guide To Becoming An AI Engineer (2026)](https://www.youtube.com/watch?v=oHu_xWe0agI)
- [@video@AI, Machine Learning, Deep Learning and Generative AI Explained](https://www.youtube.com/watch?v=qYNweeDHiyU)
- [@video@AI Engineering Vs AI Forward Deployed Engineer (FDE)](https://www.youtube.com/watch?v=05ZezulZKkQ)

### Choosing your Model Provider
LLM providers trade off capability, cost, latency, context length, and licensing (OpenAI, Anthropic, Google, Meta open-weights, Mistral). Choosing the right one means evaluating benchmarks, pricing, API reliability, data-privacy terms, and fit to the application's needs.
- [@video@How to Choose Large Language Models: A Developer's Guide](https://www.youtube.com/watch?v=pYax2rupKEY&t=9s)
- [@video@Choose the right AI model for your use case](https://www.youtube.com/watch?v=aqWXSShwGO0)

### Gemini
Google DeepMind's multimodal model family (text, code, images), available via Google AI Studio and Vertex AI in sizes trading off speed vs. capability.
- [@official@Google's Gemini Docs](https://workspace.google.com/solutions/ai/)
- [@article@What is Google Gemini?](https://zapier.com/blog/google-gemini/)
- [@article@How To Master Google Gemini in 2026 (Free Course)](https://www.youtube.com/watch?v=-_FizlRlfYs)

### Prompt Engineering
Crafting inputs for more accurate/reliable model outputs: zero-/few-shot prompting, chain-of-thought, role assignment, structured output. Can meaningfully improve behavior with no fine-tuning.
- [@roadmap@Dedicated Prompt Engineering Roadmap](https://roadmap.sh/prompt-engineering)
- [@article@What is prompt engineering?](https://www.ibm.com/think/topics/prompt-engineering)
- [@video@Prompt Engineering Full Course](https://www.youtube.com/watch?v=2BpCk4d2Cc0)

### Prompt Management
Systematic creation, versioning, testing, and refinement of prompt templates — treating prompts as code so changes in phrasing can be tracked against performance, consistency maintained across model versions, and cost/latency optimized.
- [@article@What is prompt management?](https://www.braintrust.dev/articles/what-is-prompt-management)
- [@article@What is Prompt Management?](https://humanloop.com/blog/prompt-management)
- [@video@Prompt Management 101 - Full Guide for AI Engineers](https://www.youtube.com/watch?v=Qddc_DNo9qY)

### Context Engineering
Strategically curating/structuring/refining the information given to an LLM — prompt crafting, RAG, conversation-memory management — so the model has the background it needs for a specific task.
- [@article@What Is Context Engineering? | IBM](https://www.ibm.com/think/topics/context-engineering)
- [@article@Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [@article@Context Engineering for AI Agents: A Deep Dive](https://towardsdatascience.com/deep-dive-into-context-engineering-for-ai-agents/)
- [@video@Context engineering explained](https://www.youtube.com/watch?v=BBPQYtR7oUk)

### RAGs
Retrieval-Augmented Generation: fetch relevant documents/data and inject into context before generation, giving the model current/specific knowledge without fine-tuning. Combines a retrieval step (embeddings/search) with a generation step (LLM).
- [@article@What is Retrieval-Augmented Generation? - Google](https://cloud.google.com/use-cases/retrieval-augmented-generation)
- [@article@RAG Explained: Understanding Embeddings, Similarity, and Retrieval](https://towardsdatascience.com/rag-explained-understanding-embeddings-similarity-and-retrieval/)
- [@video@What is Retrieval-Augmented Generation? - IBM](https://www.youtube.com/watch?v=T-D1OfcDW1M)

### Vector DBs
Store high-dimensional embeddings with efficient (usually approximate-nearest-neighbor) similarity search — a core component of RAG and semantic search, finding content semantically similar to a query rather than keyword-matching.
- [@article@Vector Databases](https://developers.cloudflare.com/vectorize/reference/what-is-a-vector-database/)
- [@article@What are Vector Databases?](https://www.mongodb.com/resources/basics/databases/vector-databases)
- [@video@What is a Vector Database?](https://www.youtube.com/watch?v=gl1r1XV0SLw)
- [@video@Production RAG with LangChain & Vector Databases – Full Course](https://www.youtube.com/watch?v=mHxLXzYjQRE)

### AI Agents
Systems where an LLM is given tools and a goal and takes a sequence of actions rather than answering one prompt — calling APIs, searching, writing/running code, reading files. Well-designed agents usually use one orchestrating LLM call plus a series of tool calls; start with the smallest unit of autonomy, prove it, then expand.
- [@roadmap@Dedicated AI Agents Roadmap](https://roadmap.sh/ai-agents)
- [@article@What are AI Agents?](https://aws.amazon.com/what-is/ai-agents/)
- [@article@AI Agents Explained in Simple Terms for Beginners](https://www.geeky-gadgets.com/ai-agents-explained-for-beginners/)
- [@video@What are AI Agents?](https://www.youtube.com/watch?v=F8NKVhkZZWI)

### Agent Architectures
How an agent is structured — reasoning, tool selection, memory, stopping conditions. Common patterns: ReAct (reason+act), plan-and-execute, tree-of-thought. The right choice depends on how much control is needed over model behavior and the customer's tolerance for unpredictable output.
- [@article@What is agentic architecture?](https://www.ibm.com/think/topics/agentic-architecture)
- [@article@AI Agent Architecture: Tutorial & Examples](https://fme.safe.com/guides/ai-agent-architecture/)
- [@video@AI Agents, Clearly Explained](https://www.youtube.com/watch?v=FwOTs4UxQS4)

### Multi-Agents
Multiple agents with distinct roles coordinating on a larger task — one plans, others execute subtasks, a final one synthesizes. Improves reliability and modularity for complex workflows that would overwhelm a single agent.
- [@article@What is a multi-agent system?](https://www.ibm.com/think/topics/multiagent-system)
- [@article@Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems)
- [@article@Agentic AI 103: Building Multi-Agent Teams](https://towardsdatascience.com/agentic-ai-103-building-multi-agent-teams/)
- [@video@Multi Agent Systems Explained](https://www.youtube.com/watch?v=sWH0T4Zez6I)

### Tools & Functions
The mechanisms through which agents act on the world — querying a database, calling an API, running a code interpreter, searching the web. Defined as schemas the model can invoke; the application executes the function and returns the result.
- [@article@What are Tools? - Hugging Face](https://huggingface.co/learn/agents-course/en/unit1/tools)
- [@article@What is Tool Calling?](https://www.databricks.com/blog/what-is-tool-calling/ai-agent-tools)
- [@article@AI Agents Explained in Simple Terms for Beginners](https://www.geeky-gadgets.com/ai-agents-explained-for-beginners/)
- [@video@What is Tool Calling? Connecting LLMs to Your Data](https://www.youtube.com/watch?v=h8gMhXYAv1k)

### Memory & State Management
How agents store/retrieve information across steps. Short-term memory lives in the context window; long-term memory needs external storage (DB, vector store). Good state management matters for agents that must track progress, avoid repetition, and stay consistent over long interactions.
- [@article@Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110)
- [@article@Memory Management in AI Agents](https://python.langchain.com/docs/how_to/chatbots_memory/)
- [@article@Storing and Retrieving Knowledge for Agents](https://www.pinecone.io/learn/langchain-retrieval-augmentation/)
- [@video@Building Brain-Like Memory for AI Agents](https://www.youtube.com/watch?v=VKPngyO0iKg)

### MCP
The Model Context Protocol: an open standard connecting AI models to external tools/data through a unified interface, so developers implement MCP servers instead of custom integrations per tool — composable agents across many services.
- [@article@What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
- [@article@MCP Explained: How Modern AI Agents Connect to the Real World](https://towardsdatascience.com/mcp-explained-how-modern-ai-agents-connect-to-the-real-world/)
- [@video@What is MCP? Integrate AI Agents with Databases & APIs](https://www.youtube.com/watch?v=eur8dUO9mvE)
- [@video@How Model Context Protocol (MCP) actually works](https://www.youtube.com/watch?v=cGuyrANVi4A)

### Building Eval Pipelines
Automated systems for measuring AI quality across test cases. A good eval traces the steps a skilled human would take and grades the agent on each one, not just the final answer. Start from a golden dataset — real queries with hand-labeled ideal outputs — as the measuring standard.
- [@article@What Is An Evaluation Pipeline?](https://arize.com/glossary/evaluation-pipeline/)
- [@article@Automated Regression Testing: The Complete 2026 Guide](https://roadmap.sh/ai-engineer/automated-regression-testing)
- [@video@LLM Evaluation](https://www.youtube.com/playlist?list=PLEneLIDJFpcA)

### Debugging Agent Logic
Tracing an agent's reasoning steps, tool calls, and decisions to find where it went wrong — harder than normal debugging because agent behavior is non-deterministic. Structured logging, step-by-step traces, and replay capability are the main tools for making failures visible and reproducible.
- [@article@What Is Agent Debugging?](https://arize.com/glossary/debugging-agents/)
- [@article@AI Agent Debugging](https://nhimg.org/glossary/ai-agent-debugging/)
- [@video@How to Debug, Evaluate, and Ship Reliable AI Agents with LangSmith](https://www.youtube.com/watch?v=oSjAbx67f0k)

### Inference Optimization
Techniques for faster/cheaper model predictions without materially hurting quality: quantization, distillation, caching, batching. Especially relevant for LLMs where inference cost is substantial at scale.
- [@article@How can I optimize for an inference application?](https://cloud.google.com/discover/inference-optimization?hl=en)
- [@article@Inference optimization techniques and solutions](https://nebius.com/blog/posts/inference-optimization-techniques-solutions)
- [@video@Mastering LLM Inference Optimization](https://www.youtube.com/watch?v=9tvJ_GYJA-o)
- [@video@Inference Engines explained in 10min](https://www.youtube.com/watch?v=_xM8scs4_x4&t=54s)

### AI Governance
Policies, processes, and controls ensuring AI systems behave safely, fairly, and compliantly — defining acceptable use, managing model risk, ensuring decision transparency, monitoring for bias/harmful output.
- [@article@What is AI governance?](https://www.ibm.com/think/topics/ai-governance)
- [@article@AI Governance Best Practices](https://www.databricks.com/blog/ai-governance-best-practices-how-build-responsible-and-effective-ai-programs)
- [@video@Security & AI Governance: Reducing Risks in AI Systems](https://www.youtube.com/watch?v=4QXtObc61Lw)
- [@video@The Importance of AI Governance](https://www.youtube.com/watch?v=Q020C-Jw0o8)

---

## 4. AI Coding Tools

### Claude Code
Anthropic's AI coding assistant: writes, edits, explains, and debugs code across languages/frameworks, designed to handle complex multi-file tasks and refactors alongside generation.
- [@roadmap@Dedicated Claude Code Roadmap](https://roadmap.sh/claude-code)
- [@official@Claude Code overview](https://code.claude.com/docs/en/overview)
- [@official@How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- [@video@CLAUDE CODE FULL COURSE 4 HOURS (2026)](https://www.youtube.com/watch?v=QoQBzR1NIqI)

### Cursor
AI-powered editor on top of VS Code integrating LLMs into the coding workflow: chat-based editing, multi-file edits, codebase-aware completion, agent-style project-wide changes.
- [@official@Cursor Docs](https://cursor.com/docs)
- [@article@Claude Code vs Cursor: Which AI Coding Tool To Choose in 2026?](https://roadmap.sh/claude-code/vs-cursor)
- [@video@Cursor AI Tutorial for Beginners](https://www.youtube.com/watch?v=3289vhOUdKA)
- [@video@Cursor Tutorial for Beginners (AI Code Editor)](https://www.youtube.com/watch?v=ocMOZpuAMw4)

### Codex
OpenAI's code-focused model trained on large amounts of public code; generates code from natural language, completes functions, assists documentation — powers GitHub Copilot and helped popularize AI-assisted coding.
- [@official@Codex Docs](https://developers.openai.com/codex)
- [@article@Claude Code or Codex? How to Pick the Right AI Agent](https://roadmap.sh/claude-code/vs-codex)
- [@video@Codex Crash Course](https://www.youtube.com/playlist?list=PL4cUxeGkcC9iDBeA8IyR1IE1kl4w5IDEG)

### OpenCode
Open-source, terminal-based AI coding agent working with many model providers (Anthropic, OpenAI, Google, local models) — provider-agnostic. Useful for FDEs in customer environments with strict rules on which models/data are approved, or that require self-hosted models.
- [@official@OpenCode Docs](https://opencode.ai/v2/docs/)
- [@article@opencode.school](https://opencode.school/)
- [@article@Claude Code vs OpenCode: Which Coding Agent Fits You?](https://roadmap.sh/claude-code/vs-opencode)
- [@video@OpenCode Tutorial for Beginners](https://www.youtube.com/watch?v=QzqaZshQcJI&t=91s)

### OpenClaw
An AI-assisted development tool automating integration between complex software systems and LLMs — a structured framework for code generation, refactoring, and debugging directly in an existing environment, lowering the barrier to rapid prototyping.
- [@roadmap@Dedicated OpenClaw Roadmap](https://roadmap.sh/openclaw)
- [@official@OpenClaw Docs](https://docs.openclaw.ai/)
- [@article@How to Install OpenClaw: A Complete Setup Guide](https://roadmap.sh/openclaw/installation-guide)
- [@article@OpenClaw Security: 12 Best Practices](https://roadmap.sh/openclaw/security-best-practices)
- [@article@OpenClaw vs. Claude Code](https://roadmap.sh/openclaw/vs-claude-code)
- [@video@OpenClaw Tutorial for Beginners](https://www.youtube.com/watch?v=u4ydH-QvPeg)

### Vibe Coding
Using AI tools to write/edit/iterate code via natural language at a higher abstraction level — describing intent and guiding the AI rather than hand-writing every line, then reviewing/refining output.
- [@article@Vibe coding tutorial: Build your first app with Claude Code](https://roadmap.sh/vibe-coding/tutorial)
- [@article@Vibe Coding Best Practices](https://roadmap.sh/vibe-coding/best-practices)
- [@article@The 10 Best Vibe Coding Tools in 2026](https://roadmap.sh/vibe-coding/best-tools)
- [@video@What Is Vibe Coding?](https://www.youtube.com/watch?v=Y68FF_nUSWE)

---

## 5. Cloud, Infrastructure & DevOps

### Cloud Platforms
On-demand compute, storage, networking, databases, and managed services instead of physical hardware; teams deploy/scale on cloud infra rather than running their own servers.
- [@article@What is cloud computing?](https://aws.amazon.com/what-is-cloud-computing/)
- [@video@Cloud Computing In 6 Minutes](https://www.youtube.com/watch?v=M988_fsOSWo)
- [@video@Cloud Computing Playlist [2027 Updated]](https://www.youtube.com/playlist?list=PLEiEAq2VkUUIJ3o1tehvtux0_Ynf42CBN)

### AWS
Largest cloud platform by market share: compute (EC2, Lambda), storage (S3), databases (RDS, DynamoDB), networking, AI/ML tooling, and a deep third-party ecosystem.
- [@roadmap@Dedicated AWS Roadmap](https://roadmap.sh/aws)
- [@official@AWS Cloud Essentials](https://aws.amazon.com/getting-started/cloud-essentials/)
- [@official@Overview of Amazon Web Services](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [@video@AWS Certified Cloud Practitioner Training](https://www.youtube.com/watch?v=3hLmDS179YE)

### Azure
Microsoft's cloud platform, strong in enterprise environments already on Active Directory/Office 365/.NET; offers compute, storage, networking, DevOps tooling, and AI services including Azure OpenAI.
- [@official@What is Azure?](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-azure)
- [@official@Azure Docs](https://learn.microsoft.com/en-us/azure/?product=popular)
- [@video@Microsoft Azure](https://www.youtube.com/playlist?list=PLEiEAq2VkUUKihhGvJw05bU8DhoQMn_ni)
- [@video@Microsoft Azure Fundamentals Certification Course](https://www.youtube.com/watch?v=5abffC-K40c)

### GCP
Google's cloud offering, strong in data/analytics (BigQuery) and AI/ML infra (Vertex AI); often preferred for data-intensive workloads or orgs already on Google Workspace.
- [@official@Google Cloud Documentation](https://docs.cloud.google.com/docs)
- [@article@What is Google Cloud Platform?](https://www.huntress.com/cybersecurity-101/topic/what-is-google-cloud-platform)
- [@video@Google Cloud Platform playlist](https://www.youtube.com/playlist?list=PLEiEAq2VkUUI0xT8VNpjBuWvmnLHxPcsE)

### Containers
Lightweight packaging of an application with its dependencies/config to run consistently across environments; unlike VMs, containers share the host kernel, so they start fast and run efficiently. Docker is the dominant tool.
- [@article@What are Containers?](https://cloud.google.com/learn/what-are-containers)
- [@video@What are Containers?](https://www.youtube.com/playlist?list=PLawsLZMfND4nz-WDBZIj8-nbzGFD4S9oz)

### Docker
The leading platform for building/shipping/running containers; a Dockerfile defines image build steps, and Docker runs images locally or pushes them to a registry — the standard for consistent behavior from dev through production.
- [@roadmap@Dedicated Docker Roadmap](https://roadmap.sh/docker)
- [@official@Docker Docs](https://docs.docker.com/)
- [@video@Docker Crash Course for Absolute Beginners](https://www.youtube.com/watch?v=pg19Z8LL06w)

### Kubernetes
Open-source container orchestration automating deployment, scaling, and management: scheduling across a cluster, service discovery, load balancing, rolling updates, self-healing. The standard for running containers in production at scale.
- [@roadmap@Dedicated Kubernetes Roadmap](https://roadmap.sh/kubernetes)
- [@official@Kubernetes Docs](https://kubernetes.io/docs/home/)
- [@article@Introduction of Kubernetes](https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes)
- [@video@Kubernetes Tutorial for Beginners](https://www.youtube.com/watch?v=X48VuDVv0do)

### Terraform
HashiCorp's infrastructure-as-code tool: define cloud resources in config files and provision/update them automatically, across multiple providers — the standard for repeatable, version-controlled infra.
- [@roadmap@Dedicated Terraform Roadmap](https://roadmap.sh/terraform)
- [@official@Terraform Documentation](https://developer.hashicorp.com/terraform)
- [@article@Terraform Backend: How it Works and How to Configure it](https://roadmap.sh/terraform/backend)
- [@video@Complete Terraform Course](https://www.youtube.com/watch?v=7xngnjfIlK4)

### DevOps Skills
Automating/streamlining build, test, and deploy. An FDE fluent in DevOps can own the whole deployment lifecycle — spinning up infra through shipping a containerized agent into a client's cloud — without depending on another team.
- [@article@What Is DevOps? A Guide to the Basics](https://www.coursera.org/articles/what-is-devops)
- [@video@DevOps In 5 Minutes](https://www.youtube.com/watch?v=Xrgk023l4lI)
- [@video@DevOps Engineering Course for Beginners](https://www.youtube.com/watch?v=j5Zsa_eOXeY)

### DevSecOps
Integrating security directly into the DevOps pipeline rather than as a final pre-release gate: automated security scanning in CI/CD, dependency vulnerability checks, secrets management, security review throughout development.
- [@roadmap@Dedicated DevSecOps Roadmap](https://roadmap.sh/devsecops)
- [@article@What is DevSecOps? - Red Hat](https://www.redhat.com/en/topics/devops/what-is-devsecops)
- [@article@What is DevSecOps? - AWS](https://aws.amazon.com/what-is/devsecops/)
- [@video@DevSecOps Course for Beginners – API Security](https://www.youtube.com/watch?v=JfiWi8RjN-8)

### Security
Protecting applications, data, and infra from unauthorized access, misuse, or attack. AI systems add concerns: prompt injection, model abuse, unintended data leakage through outputs.
- [@roadmap@Dedicated Cyber Security Expert Roadmap](https://roadmap.sh/cyber-security)
- [@article@What Is LLM Security? Starter Guide](https://www.paloaltonetworks.com/cyberpedia/what-is-llm-security)
- [@video@OWASP's Top 10 Ways to Attack LLMs](https://www.youtube.com/watch?v=gUNXZMcd2jU)

### Day 2 Operations
Everything after a system goes live: ongoing upkeep, monitoring for failures, handling edge cases not anticipated during development, responding to real-user feedback.
- [@article@What are Day-2 Operations?](https://www.cloudthinker.io/what-is-day-2-operations)
- [@article@Day 2 Operations: A Practical Guide for Managing Post-Deployment Complexity](https://www.cycloid.io/blog/day-2-operations-a-practical-guide-for-managing-post-deployment-complexity/)

### Observability
Understanding a system's internal state from its external outputs — logging, metrics, distributed tracing. For AI systems this extends to monitoring model outputs, tracking prompt/response quality, and detecting unexpected production behavior.
- [@article@What is LLM observability?](https://www.ibm.com/think/topics/llm-observability)
- [@article@Top 10 Best LLM Observability Tools](https://roadmap.sh/ai-engineer/observability-tools)
- [@video@LLM Observability Explained](https://www.youtube.com/watch?v=o76xU3RQ47Q)

### Managed ML Services
Cloud-provider offerings (AWS SageMaker, Google Vertex AI, Azure ML) that abstract away training/deployment/serving infrastructure for ML models, handling provisioning/scaling/monitoring.
- *(no resource links given in the source file)*

### MLOps
Applies DevOps principles to ML systems: versioning data/models, automating training pipelines, serving inference at scale, detecting model degradation over time.
- [@article@What is MLOps?](https://aws.amazon.com/what-is/mlops/)
- [@article@Machine Learning Operations (MLOps) For Beginners](https://towardsdatascience.com/machine-learning-operations-mlops-for-beginners-a5686bfe02b2/)
- [@article@MLOps: What It Is, Why It Matters, and How to Implement It](https://web.archive.org/web/20251126053103/https://neptune.ai/blog/mlops)
- [@video@MLOps Course – Build Machine Learning Production Grade Projects](https://www.youtube.com/watch?v=-dJPoLm_gtE)

---

## 6. Data Engineering

### Data Engineering
Building/maintaining systems that collect, store, process, and move data at scale: pipelines, warehouses, and data-quality assurance for downstream consumers like analysts and ML systems.
- [@article@Visit the Dedicated Data Engineer Roadmap](https://roadmap.sh/data-engineer)
- [@article@What is data engineering?](https://www.ibm.com/think/topics/data-engineering)
- [@video@Data Engineering Course for Beginners](https://www.youtube.com/watch?v=PHsC_t0j1dU)

### Data Modeling
Deciding how data is structured/stored for efficient queries and shared understanding. Patterns: star schema (fact table + dimension tables), one-big-table (OBT) for some analytics workloads, and the medallion architecture (bronze/silver/gold layers) in lakehouses.
- [@article@What Is Data Modeling? | IBM](https://www.ibm.com/think/topics/data-modeling)
- [@video@What is Data Modelling? Beginner's Guide](https://www.youtube.com/watch?v=CUR6rKrIEGc)

### Data Pipelines
Series of steps moving/transforming data from source systems into a warehouse or processing layer — batch (scheduled) or streaming (as-it-arrives). Reliability requires handling failures, schema changes, and validation.
- [@article@What is a Data Pipeline? - IBM](https://www.ibm.com/topics/data-pipeline)
- [@video@What are Data Pipelines?](https://www.youtube.com/watch?v=oKixNpz6jNo)
- [@video@Build a Data Engineering Pipeline using Python and Airflow](https://www.youtube.com/playlist?list=PLf0swTFhTI8pRV9DDzae2o1m-cqe5PtJ2)
- [@video@Building Data Pipelines with Apache Kafka and Confluent](https://www.youtube.com/playlist?list=PLa7VYi0yPIH1MculjFWJxs-aENPxRHHOS)

### Data Warehouses
Systems optimized for analytical queries across large structured datasets (Snowflake, BigQuery, Redshift) — built for reading/aggregating, unlike operational databases built for frequent writes; typically central to a company's analytics/BI.
- [@article@What Is a Data Warehouse?](https://www.oracle.com/database/what-is-a-data-warehouse/)
- [@video@What is a Data Warehouse?](https://www.youtube.com/watch?v=k4tK2ttdSDg)
- [@video@Database vs Data Warehouse vs Data Lake](https://www.youtube.com/watch?v=-bSkREem8dM)

### Airflow
Open-source workflow orchestration for scheduling/monitoring data pipelines, with pipelines defined as Python DAGs; web UI for monitoring runs, managing dependencies, handling retries/alerts.
- [@official@Airflow Docs](https://airflow.apache.org/docs)
- [@opensource@airflow](https://github.com/apache/airflow)
- [@article@Building Pipelines In Apache Airflow – For Beginners](https://towardsdatascience.com/building-pipelines-in-apache-airflow-for-beginners-58f87a1512d5/)
- [@video@Airflow Tutorial For Beginners](https://www.youtube.com/watch?v=IiczxlbQb8s)

### Spark
Distributed computing framework for parallel large-dataset processing across a cluster — batch, streaming, SQL, and ML through one unified API. Common where data volume exceeds single-machine capacity.
- [@official@Apache Spark Docs](https://spark.apache.org/docs/latest/)
- [@article@Spark By Examples](https://sparkbyexamples.com)
- [@video@PySpark - Zero to Hero](https://www.youtube.com/playlist?list=PL2IsFZBGM_IHCl9zhRVC1EXTomkEp_1zm)

### Data Privacy & Compliance
Handling personal/sensitive data per applicable law and policy (GDPR, CCPA, HIPAA, etc.). For AI systems: what data goes to third-party model APIs, what's stored, how long it's retained.
- [@article@Security, Compliance, and Data for Forward Deployed Engineers](https://www.theforwarddeployed.io/production/security-compliance)
- [@article@Understanding Data Privacy Compliance](https://www.salesforce.com/platform/data-privacy-compliance/what-is-data-privacy-compliance/)
- [@video@Data Security: Protect your critical data](https://www.youtube.com/watch?v=N8xEgSe5RwE)

---

## 7. Integration & Enterprise Systems

### Integration Engineering
Connecting systems not designed to work together: building APIs over existing data layers, bridging incompatible auth systems, chaining tools with different data formats, wrapping third-party products in reliable interfaces. Most of the real difficulty in AI deployments lives here, not in the model itself.
- [@article@Software Integration: Examples and Why It's Important](https://www.coursera.org/articles/software-integration)
- [@article@What Is An Integration Engineer?](https://latamcent.com/glossary/integration-engineer/)

### Last-Mile Integration
The final connections between a product and a specific customer's systems/data/workflows — often the shortest but hardest part of a deployment: the product works generally, but fitting this customer's setup requires custom engineering.
- [@article@What a forward deployed engineer does, and how to tell if you are ready](https://www.extendfuture.com/blog/forward-deployed-engineer/)
- [@article@The Last Mile of AI: Why Forward Deployed Engineers Are Becoming the Most Critical Role](https://www.linkedin.com/pulse/last-mile-ai-why-forward-deployed-engineers-becoming-gottumukkala-7a79c/)
- [@article@What is a Forward Deployed Engineer(FDE)? The "Last Mile" Special Ops of the AI Revolution](https://blog.mrprompty.com/what-is-a-forward-deployed-engineer-fde-the-last-mile-special-ops-of-the-ai-revolution/)

### Working with Legacy Systems
Established, often-undocumented infrastructure most large orgs run on (on-prem DBs with no API, decade-old ERPs, internal tools nobody fully understands). Approach: build around them — wrap with APIs, query safely, connect to modern infra without replacing what the business depends on.
- [@article@Working With Legacy Systems: A Forward Deployed Engineer's Survival Guide](https://www.guvi.in/blog/working-with-legacy-systems-fde-guide/)
- [@article@Legacy system modernisation: challenges and common approaches](https://www.future-processing.com/blog/legacy-system-modernisation/)
- [@video@What Is Legacy Code? How AI Is Modernizing Legacy Systems](https://www.youtube.com/watch?v=CKC47S92wA4)

### System of Record
The authoritative source of truth for a data type within an org (Salesforce for customer data, SAP for financial, Workday for HR). Identifying it early matters: anything touching that data must integrate with the real system, not a stale copy or cache.
- *(no resource links given in the source file)*

### Enterprise Workflow
The processes/systems through which large orgs operate — approvals, handoffs, integrations with existing tools, compliance requirements. Building for enterprise means designing solutions that fit within these workflows.
- [@article@What is enterprise workflow management?](https://www.manageengine.com/appcreator/enterprise-workflow-management.html)
- [@article@What Is Workflow Automation? A Guide for Enterprise](https://www.elementum.ai/blog/workflow-automation-enterprise-guide)

---

## 8. Client Engagement & Delivery

### Discovery & Scoping
Identifying the problem, understanding the customer's current systems/processes, and defining success before building starts — asking the right questions, finding constraints, setting realistic expectations. Getting this right determines whether the rest of the engagement goes smoothly.
- [@article@AI Techniques (Production): Use Case Discovery & System Scoping](https://academy.openai.com/public/clubs/builders-etkn1/videos/ai-techniques-production-use-case-discovery-and-system-scoping-2025-12-11)
- [@article@AI Discovery & Scoping Session](https://www.elevatecorporatetraining.com.au/ai-discovery-scoping/)

### Requirements Gathering
Requirements come from observation as much as conversation — watching how teams actually work, since that often differs from how they describe their work. Goal: surface undocumented workflow, the data source people actually trust, and edge cases that would break an agent in week one.
- [@course@Requirements Gathering in Business Analysis](https://www.coursera.org/learn/requirements-gathering-in-business-analysis)
- [@article@Requirements Gathering in Software Engineering](https://www.jamasoftware.com/requirements-management-guide/requirements-gathering-and-management-processes/what-is-requirements-gathering/)
- [@video@Requirement Gathering Techniques For A Business Analyst](https://www.youtube.com/watch?v=8EBWxW5Cn1g)

### Technical Scoping & Sequencing
Breaking a project into discrete tasks, estimating complexity, identifying dependencies, then ordering tasks — starting with the highest-risk/most-uncertain parts. A well-scoped, well-sequenced project is easier to track and gives the customer visibility.
- [@article@How to effectively scope your software projects](https://medium.com/free-code-camp/how-to-effectively-scope-your-software-projects-from-planning-to-execution-e96cbcac54b9)
- [@article@The Ultimate Guide to Scoping Consulting Projects](https://consultingquest.com/insights/scoping-consulting-projects-framework/)
- [@article@Sequence Activities to Improve Project Scheduling](https://brainsensei.com/glossary/sequence-activities/)
- [@video@Project Scope Statement [IN 4 EASY STEPS]](https://www.youtube.com/watch?v=QDLk2QIuJkg)

### Tradeoffs: Scope, Speed, Quality
Every project trades off scope, speed, and quality. Cutting scope can speed delivery without hurting quality; cutting quality can speed things short-term but creates later problems. FDEs need to understand and clearly communicate these tradeoffs so customers make informed decisions.
- [@article@Project management triangle: Triple constraint guide](https://asana.com/resources/project-management-triangle)
- [@video@What is the Iron Triangle? Time, Cost, Quality, Scope?](https://www.youtube.com/watch?v=JHSHOAfV-uw)

### Stakeholder Management
Less about keeping people happy, more about making sure the right people know what's happening before it's a problem: identify skeptics early, give them evidence (usually evals) to build trust, manage expectations before a demo rather than after it fails, escalate blockers fast. Excellent technical work can still fail an engagement if approvers/adopters/funders never buy in.
- [@article@Stakeholder Management Guide](https://simplystakeholders.com/resources/guides/stakeholder-management/)
- [@article@Your Ultimate Guide to Effective Stakeholder Management](https://www.boreal-is.com/stakeholder-management-ultimate-guide/)
- [@video@What is Stakeholder Management?](https://www.youtube.com/watch?v=-tNHplQ_-hw)
- [@video@How to Manage Difficult Stakeholders](https://www.youtube.com/watch?v=NaGhBpfZLzg)

### Communication
If you can't explain what AI can and can't do to a non-technical VP, you can't be an FDE. It means translating between the technical reality of what's being built and the business reality of what justifies the investment — discussing token cost and latency in the same conversation as ROI, and knowing when to say AI isn't the right answer.
- [@article@6 Strategies to Improve Your Communication Skills as a Software Developer](https://www.talaera.com/industry-specific-english/communication-skills-software-developers/)
- [@article@Beyond Code: Communication Skills Every Software Engineer Needs](https://dev.to/thawkin3/beyond-code-communication-skills-every-software-engineer-needs-5714)
- [@video@Talk Like a Strategy Consultant (McKinsey's Culture)](https://www.youtube.com/watch?v=VtUpRjAqdKM)
- [@video@TALK LIKE A CONSULTANT](https://www.youtube.com/watch?v=ppokRtCeuyI)

### Presenting Options
When a major technical decision needs stakeholder buy-in: lay out the options, explain tradeoffs of each, make a clear recommendation. Structure the presentation around what matters to the audience, not technical completeness.
- *(no resource links given in the source file)*

### Executive Reporting
Communicating engagement status to non-technical decision makers in a format they can act on. Lead with value delivered, not tasks completed; flag risks with a required action/decision attached; connect technical milestones to business outcomes.
- [@article@What Is Executive Reporting?](https://www.indeed.com/career-advice/career-development/executive-reporting)
- [@article@Executive reporting: how to create better reports](https://planyway.com/blog/executive-reporting)

### UAT
User Acceptance Testing: the customer's own team validates the system works before production — test scripts, acceptance criteria, FDE support during testing. Usually the formal delivery gate, and often where last-minute scope issues surface.
- [@article@What is User Acceptance Testing (UAT)?](https://www.guru99.com/user-acceptance-testing.html)
- [@article@User Acceptance Testing (UAT): Definition, Types & Best Practices](https://www.splunk.com/en_us/blog/learn/user-acceptance-testing-uat.html)
- [@video@How to plan your UAT](https://www.youtube.com/watch?v=AU8SV7091-s)

### Product Feedback Loop
Ship, collect feedback, use it to improve the next iteration — working closely with the customer to see how the delivered product is actually used, finding gaps between expectation and reality, feeding observations back into the build while still on the engagement.
- [@roadmap@Dedicated AI Product Builder Roadmap](https://roadmap.sh/ai-product-builder)
- [@article@What is a product feedback loop (and how do I implement it)?](https://launchdarkly.com/blog/product-feedback-loop/)
- [@article@Product Feedback Loop: Definition, 5 Steps, Types & Examples](https://formbricks.com/blog/product-feedback-loop)

---

## 9. Business & Strategy

### Business Acumen
Understanding how an organization operates, its priorities, how it makes money, and where technology can create real value. Connecting engineering decisions to business outcomes is what distinguishes FDEs from traditional software engineers.
- [@article@Business acumen for FDEs: follow the money before you write the first line of code](https://fdetimes.net/en/guides/fde-business-acumen-follow-the-money/)
- [@article@Business acumen](https://en.wikipedia.org/wiki/Business_acumen)
- [@video@Business Acumen 101](https://www.youtube.com/watch?v=JwhPhS26Mos)

### ROI & AI Impact
Quantifying how an AI system creates value — cost savings, productivity, revenue growth, risk reduction — while being honest about what AI can realistically deliver. Framing work in business terms builds customer confidence and avoids overselling.
- [@article@How to maximize AI ROI in 2026](https://www.ibm.com/think/insights/ai-roi)
- [@article@What is ROI and How to Calculate Return on Investment](https://www.esade.edu/beyond/en/what-is-roi-and-how-to-calculate-return-on-investment/)
- [@article@Forward Deployed Engineering: The Complete Guide for Industrial Companies](https://miragemetrics.com/guides/forward-deployed-engineering)

### Time-to-Value
Elapsed time from engagement start to the customer having something usable. Compressing it means shipping a working feature early rather than a perfect design, prioritizing the highest-value work first, and sequencing so trust builds incrementally.
- [@article@What Is TTV: A Complete Guide to Time to Value](https://amplitude.com/explore/analytics/time-to-value)
- [@article@Time to Value (TTV)](https://baremetrics.com/academy/time-to-value-ttv)
- [@video@What Is Time to Value (TTV)?](https://www.youtube.com/watch?v=Ae5-shAAU-s&t=17s)

### Productized Consulting
A consulting model that delivers a repeatable, packaged system rather than just custom advice or a one-off solution — building in a way that abstracts customer-specific detail so the core architecture is reusable across engagements.
- [@article@How to productize consulting services: A strategic guide](https://www.naviu.tech/blog/how-to-productize-consulting-services)
- [@article@Consultant's Guide to Productization](https://www.consultingsuccess.com/consultants-guide-to-productization)
- [@video@How To Productize Your Consulting Services](https://www.youtube.com/watch?v=CltfhWVp9p8)

---

## 10. Documentation

### Technical Writing
Producing clear, accurate, useful documentation: API docs, ADRs, runbooks, onboarding guides, design docs. Especially important for FDEs since good docs let the customer operate and extend the system after the engagement ends, without calling the FDE back for every question.
- [@roadmap@Dedicated Technical Writer Roadmap](https://roadmap.sh/technical-writer)
- [@article@Google Technical Writing Courses](https://developers.google.com/tech-writing/overview)
- [@article@What Is Technical Writing? A Comprehensive Guide](https://www.heretto.com/blog/what-is-technical-writing)
- [@video@Technical Writing Course for Beginners](https://www.youtube.com/watch?v=vT5pcc30Ffw)

---

## Gaps / notes

- **No fetch failures** — all 97 topic files in `roadmaps/forward-deployed-engineer/content/` were retrieved successfully.
- **No layout/grouping source exists** in the mirror repo for this specific roadmap — the 10 categories above are inferred from content, not copied from roadmap.sh's visual tree. roadmap.sh's actual on-page grouping may differ in boundary placement for a few topics (noted below).
- **Topics that plausibly span two categories**:
  - `learn-a-language` (Learn a Programming Language) sits at the boundary between "Orientation" and "Core Software Engineering" — placed in the latter since its content is about language-learning mechanics, not role framing.
  - `gemini` is a model, not a coding tool, but is adjacent to the AI Coding Tools cluster in the raw file listing — placed under AI & LLM Engineering next to `choosing-model-providers`.
  - `vibe-coding` could sit under either "AI Coding Tools" or "AI Engineering Skills" — placed under AI Coding Tools since its content is about the AI-assisted coding *workflow*, not system-building.
  - `product-feedback-loop` could sit under "Business & Strategy" instead of "Client Engagement & Delivery" — placed in the latter since its content is about engagement-time behavior, not business metrics.
  - `data-privacy--compliance` could sit under "Security" (cluster 5) instead of "Data Engineering" — placed with Data Engineering since its content is specifically about data handling/retention, not infra security.
- **Three topic files have no resource links at all** in the source: `managed-ml-services`, `system-of-record`, `presenting-options`. This is faithfully preserved above, not an extraction error.
- **Apparent duplication in the source roadmap itself**: both `javascript` and `javascript--typescript` exist as separate topic files with overlapping content (the former is JS-only, the latter frames JS+TS together) — both are included above since both exist as real nodes in the roadmap; likely the roadmap offers them as alternate/adjacent nodes rather than one being a mistake.
