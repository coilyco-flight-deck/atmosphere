# Agent instructions

Workspace conventions load globally via `~/.claude/CLAUDE.md` -> `agentic-os-kai/AGENTS.md`. This file covers only what's specific to this repo.

---

## What atmosphere is

Incubator monorepo for AT Protocol / Bluesky Atmosphere apps and experiments. `ideas/` is the front door for unstructured idea dumps. `packages/` and `apps/` fill in as real things take shape.

## Public-repo discipline

This repo is **public**. Standard public-repo writing rules apply (see `writing-public-repos` skill).

## No build verbs yet

`.coily/coily.yaml` has an empty `commands:` block because atmosphere is currently docs + ideas only. As real apps land in `apps/`, add their build/test verbs to that file before invoking them.

## See also

- [README.md](README.md) - human-facing intro.
- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [.coily/coily.yaml](.coily/coily.yaml) - allowlisted commands.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilysiren/agentic-os/issues/59).
