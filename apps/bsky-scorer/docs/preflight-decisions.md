# Pre-flight: locked decisions

Decisions made during the pre-flight session. These resolve the brief's open questions and constrain the v0 build.

## Language and home

- **All Python**, single toolchain. The atproto and model SDKs are mature in Python, and a single toolchain is fastest to a working v0.
- App lives at `apps/bsky-scorer/` in the atmosphere monorepo.

## Model

- **Local Ollama**, OpenAI-compatible and native endpoints on the host. No Anthropic key needed for v0, which also makes the "more real" pluggable-endpoint story the default path.
- **`qwen3:8b` does both hate-classify and scoring.** One resident model, no eviction thrash. See the environment doc for why two models do not fit.
- Hate classifier outputs hate, technical-frustration, neutral, or positive. Gate on hate only. Technical-frustration is kept on purpose as a bug-finder lead.
- **Invocation:** Ollama native `/api/chat` with `think:false` plus a JSON-schema `format` grammar. The OpenAI-compat `/v1` path is a trap for qwen3 (see environment doc). `keep_alive` is set per-request by the scorer, not as host state.

## Live pipeline (continuous)

One container holds the resident model and runs, in order:

1. Firehose consumer subscribes to Jetstream.
2. Pre-filter (handle allowlist plus keyword gate), config-driven.
3. `qwen3:8b` hate-classify, gate on hate only.
4. `qwen3:8b` score against the current `skill.md`.
5. Filter one - score at or above the push threshold (start 60).
6. Filter two - dedup and already-pushed guard.
7. Push to Telegram with inline upvote and downvote buttons.

## Roll-up (periodic, the third model role)

The roll-up takes accumulated scores and computes day-to-day change. The live container **scales to zero** before the roll-up runs, so the roll-up model gets the whole GPU and nothing thrashes. Only one model class is ever resident.

- **New BoM line item beyond the brief:** the roll-up CronJob needs in-cluster RBAC to scale the live Deployment. A ServiceAccount plus a Role granting `patch` on `deployments/scale`, bound to the CronJob pod.

## Skill schema

- YAML frontmatter (machine-parseable) plus a markdown body (human-readable doc).
- Rule schema - `id`, `kind` (boost or suppress), `weight`, `pattern`, `last_fired_at`.
- Frontmatter also carries `topic_clusters`, `score_range`, `push_threshold`, `size_cap_rules`, and `prune_unfired_after_days` (the decay term).
- Body carries the scoring procedure and 5 to 10 worked examples.
- The seed is committed at `apps/bsky-scorer/seed-skill.md`. The init-container seeds it onto the PVC when empty.

## Thresholds

- Push threshold 60 (score range 0 to 100).
- Recompile gate - daily compile only runs once cumulative votes cross 20.
- Eval-before-promote gate - runs above 50 votes, skipped below (accept new skill, anything beats the seed).

## Telemetry

OpenTelemetry, env-driven collector endpoint. SignOz and Honeycomb credentials already exist in SSM (see environment doc).
