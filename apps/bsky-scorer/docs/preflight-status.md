# Pre-flight: status and next steps

Where things stand at the end of pre-flight, and what the build session picks up.

## Done

- **Decisions locked** - language, model, pipeline, roll-up spin-down, skill schema, thresholds. See the decisions doc.
- **Local model validated** - invocation recipe, throughput, capacity limits. See the environment doc.
- **Telegram fully wired** - bot created, token and chat id stashed in SSM, message round-trip proven.
- **Seed classifier committed** - `apps/bsky-scorer/seed-skill.md`, the cold-start AI-agents scoring policy.
- **Pre-commit fleet adopted** - `apps/../.pre-commit-config.yaml` carries the agentic-os managed block. 9 hooks active. catalog-doc-size, catalog-trifecta, and documentation-layout deferred (see issue #11).
- **Cross-repo housekeeping** - models-qwen skill thickened in agentic-os with the invocation recipe, a validator cross-repo-link false-positive fixed, `.gitattributes` pinned `*.md` to eol=lf, and SSM.md updated with the new params.

## Open follow-ups

- **atmosphere #11** - clean up 43 documentation-layout violations (ideas/ and reference/ md locations, oversized docs including this preflight series and seed-skill.md, the non-flat writing-bluesky skill, AGENTS.md missing standard sections), then re-enable the three deferred hooks.
- **agentic-os #102** - `apply-agentic-os-hooks` hardcodes `SIBLINGS_ROOT` to `~/projects/coilysiren`, blind to the Windows `X:\projects-x\` layout. Suggested fix is an env-overridable root.
- **coily** - v2.41.0 has no `dispatch cascade` verb. If the fleet-wide cascade workflow is wanted, coily needs that verb built or updated.

## Next steps for the build session

1. File a Forgejo issue on `coilysiren/atmosphere` for the v0 scaffold, then work it (commit discipline - issue first).
2. Scaffold `apps/bsky-scorer/` as a Python project and add its build and test verbs to atmosphere's empty `.coily/coily.yaml` `commands:` block.
3. Build the v0 live path - firehose consumer to in-memory channel, scorer (8b hate-classify then score against the seed skill), Telegram bot with vote buttons appending to `votes.jsonl`.
4. Stand up the Helm chart per the bill of materials, including the roll-up CronJob RBAC for scaling the live Deployment to zero.
5. Get posts visibly landing in Telegram, then layer the daily compiler (log-only first), then the eval gate and pruning.

## Reading order

- `preflight-spec.md` - the design brief.
- `preflight-decisions.md` - what got locked.
- `preflight-environment.md` - model and wiring facts.
- `preflight-status.md` - this file.
