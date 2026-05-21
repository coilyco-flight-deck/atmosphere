# topic-feeds

**What** - a feed generator service hosting one custom Bluesky feed per topic Kai wants to read about. `daily-social` pulls these topic feeds instead of the raw timeline, so the digest is topic-segmented at the source.

**Why it fits the Atmosphere** - feed generator. A small HTTP service that consumes the Jetstream firehose and returns a ranked list of post URIs per topic. One service, N topic feeds.

**Status** - first real app. Tracked in [agentic-os-kai#675](https://github.com/coilysiren/agentic-os-kai/issues/675). Lands in `apps/feeds/`.

**Candidate feeds** - one idea file per topic, drawn from Kai's Obsidian interest profile (educational reading lists, productive logs, Bluesky timeline themes):

- Tier 1 - [feed-atproto-dev](feed-atproto-dev.md), [feed-agent-engineering](feed-agent-engineering.md), [feed-observability](feed-observability.md)
- Tier 2 - [feed-platform-eng](feed-platform-eng.md), [feed-homelab-k8s](feed-homelab-k8s.md), [feed-supply-chain-sec](feed-supply-chain-sec.md)
- Tier 3 - [feed-go-cli](feed-go-cli.md), [feed-ai-infra](feed-ai-infra.md)

`feed-atproto-dev` is the recommended prototype-first feed.

**Open questions**

- Topic list. Pull candidates from the current-interest profile that `daily-educational` ranks against, so feeds and reading list stay aligned.
- Ranking. Keyword match, follows graph, embeddings.
- Whether topic feeds are private (just for `daily-social`) or published for anyone to subscribe.
