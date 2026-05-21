# moderation-labelers

**What** - a labeler. A service that emits labels on accounts and records, which users subscribe to. Moderation as a composable, stackable product rather than one company's global call. Ozone is the tooling, Northsky is a community example.

**Why it fits the Atmosphere** - a labeler is one of the four core atproto service types (PDS, relay, App View, labeler). It consumes the firehose and publishes label records.

**Why it might be for Kai** - the interesting angle is not social moderation, it is labeling as a general signal. A labeler that tags posts by topic, by quality, by source could feed the topic feeds. Labels are a clean composable primitive.

**Open questions**

- Topic labeling overlaps heavily with [topic-feeds](topic-feeds.md). A labeler and a feed generator are two ways to express the same ranking. Which primitive is the right one.
- Running a real moderation labeler is a community-trust commitment. A personal signal labeler is not.
