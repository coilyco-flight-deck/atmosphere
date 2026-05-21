# AT Protocol ecosystem reference

Two halves: the **protocol primitives** (the kinds of things atproto defines) and the **implementations** (specific apps and services people built on them). The primitives are stable. The implementations drift, so treat the app list as a snapshot, not a registry. When you need the current ecosystem map, search fresh.

## Protocol primitives

### Identity layer

- **DID** - decentralized identifier. The permanent, server-independent account ID. Two methods in use: `did:plc` (the common one) and `did:web` (anchored to a domain you control).
- **Handle** - the human-readable alias for a DID (`coilysiren.me`, `kai.bsky.social`). Verified by DNS record or an HTTP well-known file, which doubles as lightweight identity proof.
- **DID document** - the resolved record for a DID. Lists the handle, the PDS endpoint, and signing keys.
- **PLC directory** - the registry that resolves `did:plc` identifiers to DID documents. A centralizing point, run by Bluesky, with an open question mark over it.

### Data layer

- **Repository (repo)** - the signed key-value store holding all of one account's data. Portable because it is signed and the DID is server-independent.
- **Record** - a single typed item in a repo (a post, a like, a follow).
- **Collection / NSID** - records are grouped into collections named by NSID, a reverse-DNS namespace like `app.bsky.feed.post`.
- **Lexicon** - the schema system. Defines record types and API methods. Anyone can author new lexicons. This is the extensibility seam.
- **Blob** - binary data (images, video) referenced from records.
- **CID / MST** - content-addressed identifiers and the Merkle Search Tree that structures a repo so it can be verified and synced efficiently.
- **AT URI** - the address of a record, `at://<did>/<collection>/<rkey>`.

### Hosting and network layer

- **PDS (Personal Data Server)** - hosts repos. Bluesky runs most, you can self-host, repos migrate between them.
- **Relay** - crawls PDSes and emits the unified event stream, the **firehose**. Expensive to run, so a centralizing pressure point.
- **Jetstream** - a lightweight JSON version of the firehose. The practical thing to consume when building a feed generator or any indexer.
- **App View** - consumes the firehose and builds a product (indexes posts, computes threads, serves timelines). Swappable.
- **Feed generator** - a service that takes the firehose and returns a ranked list of post URIs. Custom feeds. The feed generator IS the algorithm.
- **Labeler** - a moderation service that emits labels on accounts and records. Users subscribe to labelers. **Ozone** is the labeler tooling stack.

### Auth

- **OAuth** - the atproto OAuth profile, how third-party apps get scoped access to a repo.
- **Service auth** - short-lived inter-service tokens signed by the account's key.

## app.bsky record types

Bluesky's own lexicon, useful as a worked example of what a lexicon namespace looks like:

- `app.bsky.feed.post`, `.like`, `.repost`, `.threadgate`, `.postgate`
- `app.bsky.graph.follow`, `.block`, `.list`, `.listitem`, `.starterpack`
- `app.bsky.actor.profile`
- `app.bsky.feed.generator` - the record that declares a feed
- `app.bsky.labeler.service` - the record that declares a labeler

## Implementations

Snapshot, not a registry. Things come and go.

### Clients (alternative front doors for Bluesky)

- Bluesky (reference app), Graysky, deer.social, Ouranos, Skeets, Tokimeki, Klearsky

### Microblogging

- Bluesky itself

### Long-form writing and publishing

- WhiteWind (markdown blogging), Leaflet (documents and publishing), Pastesphere (pastebin)

### Link aggregation and forums

- Frontpage (Hacker News / Reddit style), various forum and threaded-discussion experiments

### Photo

- Flashes, Skygram (Instagram-style), Grain (galleries and albums)

### Video and live streaming

- Skylight, Spark (short vertical video), Streamplace (live streaming, Twitch-shaped, native atproto lexicons)

### Reviews and tracking

- Popsky (film, Letterboxd-style), book-tracking apps (Bookhive and others), Skylights (combined books / movies / games), Teal.fm and Rocksky (music scrobbling, Last.fm-style)

### Events

- Smoke Signal (events, RSVPs, calendars)

### Developer tools

- Tangled (a full git forge on atproto: repos, issues, pull requests, GitHub-shaped, atproto identity)

### Chat and messaging

- Roomy (Discord/Slack-style group chat, atproto identity plus local-first CRDT message sync), Germ (direct messaging)

### Art and creative

- PinkSea (oekaki / draw-in-browser art board), Bluemoji (custom emoji)

### Profile and link-in-bio

- Linkat (Linktree-style page backed by your repo)

### File storage

- ATFile (treats your PDS repo as a filesystem, stores arbitrary files in it)

### Moderation and labelers

- Ozone (labeler tooling), community labelers like Northsky

### Infrastructure and plumbing

- Jetstream (lightweight JSON firehose), Constellation and microcosm (global backlink indexes: who replied to, quoted, liked a record network-wide), PLC directory, relays, App Views

### SDKs and libraries

- `@atproto/api` (TypeScript, the mature official one)
- `atproto` (Python)
- `indigo` (Go, Bluesky's own)
- `atrium` (Rust)
- `ATProtoKit` (Swift)
- lightweight TS toolkits in the `@atcute` / Skyware family

Freshness: SDK names and versions move. Verify against the current docs before pinning a dependency.

### Fun and joke apps

- Flushes (a bathroom check-in app, real, working, and the cleanest proof of the thesis: someone defined a `flushes` lexicon and shipped without asking anyone)
