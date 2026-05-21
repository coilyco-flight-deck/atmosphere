# front-page

**What** - a Hacker News / Reddit-style link aggregator on atproto, Frontpage-shaped. Kai dumps data into it relentlessly, every single day, and once that habit holds "it's just all over" - the front page becomes a real running surface.

**Why it fits the Atmosphere** - link-aggregation records in a repo plus an App View that ranks and renders them. Frontpage already proves the shape, so this could be running Frontpage, forking it, or a custom build.

**Open questions**

- Run Frontpage as-is, or build a custom aggregator with its own ranking.
- What the daily data dump is. Could be fed by the daily-routines pipeline (educational reading list, GitHub feed) rather than typed by hand.
- Public community front page vs a personal one.

See [jetstream-parser](jetstream-parser.md), [topic-feeds](topic-feeds.md).
