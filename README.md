# atmosphere

Incubator monorepo for AT Protocol / Bluesky Atmosphere apps and experiments.

## Why a monorepo

This is the undefined frontier. Atmosphere apps share a lot of plumbing - lexicon definitions, identity and auth, a PDS client, a Jetstream firehose consumer. While everything here is experimental, a lexicon change should ripple through every app that reads it in one atomic commit. That is the monorepo's whole job.

The `coilysiren/cli-*` family is the opposite pattern: one repo per tool, because those tools are stable and well-bounded. Atmosphere is not there yet. When an app here proves itself and stops sharing churn with the rest, it graduates out into its own repo.

Monorepo for the frontier. Polyrepo for the settled tools.

## Layout

```
ideas/        idea dumps, one file per idea, no ceremony
packages/     shared code - lexicons, atproto-core (identity, auth, PDS client, Jetstream)
apps/         the actual Atmosphere apps, one directory each
```

`packages/` and `apps/` fill in as real things take shape. `ideas/` is the front door.

## Dumping ideas

Drop a markdown file into `ideas/`. Name it whatever. Do not overthink it. See `ideas/README.md`.

## References

- [atproto.com](https://atproto.com) - the canonical protocol spec, lexicons, identity.
- [docs.bsky.app](https://docs.bsky.app) - Bluesky developer docs, feed generator guide.
- [bluesky-social/feed-generator](https://github.com/bluesky-social/feed-generator) - official feed generator starter.
