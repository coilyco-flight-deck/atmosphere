# atfile-storage

**What** - file storage on atproto, ATFile-shaped. ATFile treats your PDS repo as a filesystem and lets you store arbitrary files in it. Kai finds it interesting and wants to understand it before deciding what to build.

**Why it fits the Atmosphere** - it is a demonstration that a "repo" is more general than "social posts." A repo is just a signed collection of records, and a record can reference a blob, so a repo can hold files. ATFile defines a lexicon for file metadata and pushes the file bytes as blobs.

**Open questions**

- Understand ATFile properly first. How big can blobs be, what do PDS hosts allow, what are the practical storage limits on a Bluesky-hosted PDS.
- What Kai would actually store. Backups, vault snapshots, build artifacts.
- Whether this is worth building anything or is just "use ATFile."

Status: explainer-first. Not an app to build yet, a primitive to learn.
