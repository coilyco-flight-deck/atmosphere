# Agent instructions

Workspace conventions load globally via `~/.claude/CLAUDE.md` -> `agentic-os-kai/AGENTS.md`. This file covers only what is specific to this repo.

## Scope

atmosphere is the incubator monorepo for AT Protocol / Bluesky Atmosphere apps and experiments. `ideas/` is the front door for unstructured idea dumps. `apps/` and `packages/` fill in as real things take shape.

## Project shape

- `ideas/` - idea dumps, one markdown file per idea, no ceremony.
- `apps/` - the actual Atmosphere apps, one directory each (today: `bsky-scorer`).
- `reference/` - protocol and ecosystem reference notes.
- `docs/` - repo-level docs, including the FEATURES inventory.

## Repo boundaries

Self-contained public incubator. Apps share plumbing (lexicons, identity, PDS client, Jetstream) so a change ripples atomically. When an app stabilizes and stops sharing churn, it graduates to its own repo.

## Commands

Route dev commands through ward, which reads [`.ward/ward.yaml`](.ward/ward.yaml) (run verbs with `ward exec <verb>`); bare `make` / `uv` / `python` are denied by lockdown. The `commands:` block is empty until real apps land - add build/test verbs there before invoking them.

## Validation

`pre-commit` runs the agentic-os catalog hooks (documentation-layout, catalog-trifecta, catalog-doc-size, context-load-points) plus skill, secret, and commit-message hooks. Never bypass with `--no-verify`.

## Safety

This repo is **public**. Standard public-repo writing rules apply (see the `writing-public-repos` skill). No secrets, tokens, or opaque ids in tracked files.

## Cross-repo contracts

Catalog node in the agentic-os graph. The managed pre-commit block is owned by `agentic-os/scripts/apply-agentic-os-hooks.py`; do not hand-edit between its markers.

## Release

No releases yet. Landing flows to the canonical Forgejo `main`; the GitHub mirror stays PR-gated.

## Agent rules

She/her for Kai in every artifact. Keep docs within catalog size caps. Place new docs at the repo root, under `docs/*.md`, or in a skill folder - or add their location to the `[tool.agentic-os.documentation-layout]` excludes in `pyproject.toml`.

## See also

- [README.md](README.md) - human-facing intro.
- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [.ward/ward.yaml](.ward/ward.yaml) - allowlisted commands (`ward exec <verb>`).
- [.coily/coily.yaml](.coily/coily.yaml) - retained during migration.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilyco-flight-deck/agentic-os/issues/59).
