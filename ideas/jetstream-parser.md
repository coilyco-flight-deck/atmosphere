# jetstream-parser

**What** - a Jetstream parser. Read off the Jetstream firehose, figure things out. Kai's realization mid-thought: Jetstream is exactly where you build feed generators, so "I actually am going to be building a feed generator" - this is not a separate app so much as the shared engine under several of them.

**Why it fits the Atmosphere** - Jetstream is the lightweight JSON firehose. A clean, reusable Jetstream consumer is the foundation under feed generators, backlink indexes, and any atproto observability work.

**Where it lives** - this is not an `apps/` entry. It is `packages/atproto-core` material, the shared Jetstream consumer that the topic feeds, the front page, and Constellation-style indexing all sit on top of.

**Open questions**

- Language. TypeScript has the most mature atproto tooling. Python is Kai's default.
- Backfill vs live-tail. A parser that only sees live events misses history.

See [topic-feeds](topic-feeds.md), [front-page](front-page.md), [constellation-backlinks](constellation-backlinks.md). All three consume this.
