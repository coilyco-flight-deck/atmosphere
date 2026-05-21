# wiki-walker

**What** - a wiki walker for things Kai understands. A personal knowledge graph, first-class for her own knowledge specifically. Nodes are concepts Kai actually knows (platform engineering, devops, observability, and so on). Edges are connections between them. It links out to Wikipedia and other references. The point is to build trees, find connections, surface gaps, and walk the graph the way a Wikipedia rabbit hole works, but rooted in what Kai and coily already know.

**Origin** - started as "a Wikipedia-style site for books," then Kai realized that is just replicating LLM training data, then realized the real want is Wikipedia-shaped navigation over her own knowledge. The book idea is dropped. This is the keeper.

**Why it fits the Atmosphere** - the knowledge graph can be records in an atproto repo. A custom lexicon for knowledge nodes and edges makes the graph portable and, if Kai wants, public and subscribable. Other people could walk her graph or fork it.

**Open questions**

- Wikipedia scraping limits. Kai is aware of them and they need real thought before building. Likely use the Wikipedia API or dumps, not scraping.
- Where the graph seeds from. Kai's vault, her repos, her recent work, coily.
- Is the atproto angle load-bearing or is this just a personal app that happens to live in this repo. Decide before building.
- Overlap with the existing catalog-graph (cross-repo knowledge graph) and repo-recall. This could share machinery.

Kai flagged this one as "a great idea, I'm gonna get into that."
