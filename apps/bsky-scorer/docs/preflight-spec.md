# Pre-flight: design brief

The original spec for the Bluesky scorer with a self-improving skill, lightly edited to the house voice. This is the source of truth for what v0 is building toward.

## Summary

A personal Bluesky scoring pipeline that filters the Jetstream firehose for AI Agents content and pushes high-relevance posts to Telegram. The novel piece is that the scoring policy is a markdown skill file that recompiles itself daily based on upvote and downvote feedback. The skill is both the agent's classifier and human-readable documentation of what counts as signal, updated atomically. The deliverable is a standalone Helm chart deployable to any Kubernetes cluster, with the model endpoint pluggable (Anthropic API, OpenAI-compatible endpoint, or self-hosted vLLM or Ollama).

## Thesis

The skills-as-team-format pattern applied to a personal classifier with a one-bit feedback channel. The skill is the compiled policy artifact. Daily compilation is the optimizer step. Telegram inline keyboards are the labeling interface. The compiled skill stays human-readable, diffable, and auditable, which is the property that distinguishes this from RLHF on opaque weights. The chart doubles as a public proof artifact, and the bug-finder pre-filter category surfaces real-world bug patterns for a parallel bug-finder thesis.

## Architecture

Four cooperating components plus shared state on a PVC. Model inference is external, configured via one endpoint URL and API key.

- **Firehose consumer** subscribes to Jetstream, applies a cheap pre-filter (handle allowlist, keyword gate), pushes candidates onward. PVC state: latest sequence cursor so restarts do not replay history.
- **Scorer** dequeues candidates, runs a cheap hate classifier and discards hate, then scores remaining posts against the current skill file. Posts above threshold get pushed to Telegram with inline upvote and downvote buttons. All pushed posts are logged to a JSONL vote ledger with score-at-push-time and which rule ids fired.
- **Telegram bot** runs long-polling, no inbound HTTP. Handles callback queries from inline keyboard buttons and appends vote events to the ledger.
- **Daily compiler** is a CronJob. Reads the current skill, the vote ledger since last compile, and a sample of recently scored posts. Produces a new candidate skill informed by misclassifications, runs an eval pass against a held-out sample, and only promotes the new skill if it does not regress. On promotion, writes the new skill to the PVC atomically.

## Key design decisions

- The sentiment filter discards hate, not negative sentiment broadly. Bug-finder leads come from people complaining about broken technical things, which is negative-affect but high signal. The classifier outputs hate, technical-frustration, neutral, or positive, and only gates on hate.
- The skill content includes structured boost and suppress patterns with weights, a topic-cluster section, and 5 to 10 worked examples. Worked examples are the few-shot signal that lets the next day's scorer generalize past keyword match.
- The skill has a hard size cap. New rules past the cap force pruning of old rules. Rules track last-fired-at and become eligible for pruning after N unfired days. This gives the policy a built-in decay term.
- Eval-before-promote is mandatory above a vote-count threshold (start 50). Below that, accept the new skill on the assumption that anything beats the seed prior.
- Cold start uses a hand-written AI-agents heuristic seeded by an init container if the PVC is empty. Daily compilation only runs once cumulative votes cross a threshold (start 20).
- Storage is a single PVC with append-only files. `skill.md` is the current policy, `votes.jsonl` the ledger, `cursor.txt` the firehose checkpoint, `posts-cache.jsonl` optional reference material. No database, no queue at personal scale.
- Telegram delivery uses polling, not webhooks. No ingress, no cert manager, no DNS.

## Bill of materials

- deployment-firehose, the Jetstream consumer with pre-filter
- deployment-scorer, the per-post loop running hate classifier and skill-based scorer
- deployment-telegram-bot, long-polling bot handling vote callbacks
- cronjob-compiler, the daily reflection loop with eval gate
- pvc for `skill.md`, `votes.jsonl`, `cursor.txt`, optional `posts-cache.jsonl`
- secret for Bluesky app password, Telegram bot token, model API key
- configmap for model endpoint URL, score thresholds, channel ids, pre-filter seeds
- init-container that seeds `skill.md` from a default template if the PVC is empty

## Open questions (from the brief)

- Exact skill schema, especially the worked-examples format the compiler can parse and rewrite.
- Hate classification method (Haiku per post was the brief default, see decisions doc for the local-model resolution).
- Vote ledger schema, at minimum post_uri, pushed_at, score_at_push, vote, voted_at, plus the rule_ids that fired.
- Whether the firehose pre-filter is configurable through the skill or stays in the configmap.
- Eval-before-promote behavior during cold start.
- Telemetry surface, collector endpoint, and span names.

## Constraints

Public-safe (no private network detail, addresses, identity descriptors, internal email). Configs in user-managed secret stores. She/her pronouns in all generated docs, commits, issue text. House voice rules (no em-dashes, no italics, no semicolons in prose, bold only as structural anchors, no prose tables, no "what this is not" sections). Commit discipline - every commit closes a same-repo issue, file first then commit, run tests and linters and builds without asking, never use --no-verify.

## First milestone (v0)

End to end - Helm chart installable with three secrets. Firehose writes pre-filtered candidates to an in-memory channel. Scorer reads candidates, classifies for hate, scores against the hand-written seed skill, pushes to a Telegram chat with vote buttons. Telegram bot captures vote callbacks and appends to `votes.jsonl` on the PVC. Daily CronJob runs but only logs what it would do, validating data shape. Once v0 is stable and votes flow, v1 adds the compiler with eval-before-promote, the size cap with rule pruning, and the init-container cold-start path.
