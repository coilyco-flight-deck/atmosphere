---
name: ai-agents-feed-policy
generation: seed
version: 0
compiled_at: 2026-05-28
score_range: [0, 100]
push_threshold: 60
size_cap_rules: 40
prune_unfired_after_days: 21
rules:
  - id: boost-agent-frameworks
    kind: boost
    weight: 28
    pattern: "langchain|langgraph|llamaindex|autogen|crewai|smolagents|agno|pydantic-ai|openai agents sdk|claude agent sdk|mastra"
    last_fired_at: null
  - id: boost-agentic-patterns
    kind: boost
    weight: 24
    pattern: "tool use|tool calling|function calling|multi-agent|agent loop|react agent|planning loop|agent memory|scratchpad|self-correction|reflexion"
    last_fired_at: null
  - id: boost-mcp
    kind: boost
    weight: 22
    pattern: "model context protocol|\\bmcp\\b|mcp server|mcp client|tool server"
    last_fired_at: null
  - id: boost-agent-eval-observability
    kind: boost
    weight: 20
    pattern: "agent eval|agent tracing|agent observability|trajectory eval|tool-call accuracy|langsmith|braintrust|otel.*agent|span.*agent"
    last_fired_at: null
  - id: boost-agent-infra
    kind: boost
    weight: 18
    pattern: "computer use|browser agent|code agent|sandbox|e2b|firecracker|agent runtime|long-running agent|agent orchestration"
    last_fired_at: null
  - id: boost-bugfinder-frustration
    kind: boost
    weight: 16
    pattern: "broken|silently (drops|fails)|wasted .* (hours|afternoon|day)|footgun|undocumented|race condition|flaky|regression"
    note: "Technical frustration about agent tooling is a bug-finder lead, not noise. Only fires alongside an agent-topic boost."
    requires_any: ["boost-agent-frameworks", "boost-agentic-patterns", "boost-mcp", "boost-agent-infra"]
    last_fired_at: null
  - id: suppress-crypto-agents
    kind: suppress
    weight: 40
    pattern: "\\$[A-Z]{2,6}\\b|airdrop|token launch|presale|web3 agent|agent.*token|to the moon"
    last_fired_at: null
  - id: suppress-engagement-bait
    kind: suppress
    weight: 30
    pattern: "thread \\u2193|like and repost|follow for more|hot take|unpopular opinion|game changer|mind = blown|this is huge"
    last_fired_at: null
  - id: suppress-generic-ai-hype
    kind: suppress
    weight: 26
    pattern: "agi is (here|coming)|will replace all|the future of everything|prompt engineering tips|10 prompts"
    last_fired_at: null
  - id: suppress-pure-llm-no-agent
    kind: suppress
    weight: 14
    note: "Pure model-release or prompt-craft chatter with no agent substance. Mild suppress, not a hard gate."
    pattern: "new model dropped|benchmark scores|context window|fine-tun(e|ing)|quantization"
    last_fired_at: null
topic_clusters:
  - id: frameworks-and-sdks
    members: [boost-agent-frameworks, boost-mcp]
  - id: patterns-and-architecture
    members: [boost-agentic-patterns, boost-agent-infra]
  - id: reliability-and-eval
    members: [boost-agent-eval-observability, boost-bugfinder-frustration]
---

# AI Agents Feed Policy (seed v0)

Hand-written cold-start policy for scoring Bluesky posts on relevance to **AI agent engineering**. The daily compiler replaces this file once enough vote signal accumulates. Until then this seed prior holds.

## What counts as signal

High signal is concrete, practitioner-level content about building, running, evaluating, or debugging AI agents. Posts that name a framework, describe an agentic pattern, discuss tool use or MCP, or report a real failure mode in agent tooling. Low signal is hype, engagement bait, crypto noise, and generic LLM chatter with no agent substance.

A post complaining that an agent framework is broken is high signal, not negative noise. Those are bug-finder leads. The `boost-bugfinder-frustration` rule captures them, but only when an agent-topic rule also fires, so generic griping does not leak in.

## Scoring procedure

1. Start at a base score of 35.
2. Add the weight of every `boost` rule whose pattern matches.
3. Subtract the weight of every `suppress` rule whose pattern matches.
4. A rule with `requires_any` only contributes if at least one listed rule also fired.
5. Clamp to the `score_range`. Posts at or above `push_threshold` (60) get pushed to Telegram.

Record which rule ids fired on each scored post. The vote ledger attributes upvotes and downvotes back to those ids so the compiler can tell which rules earn their place and which decay out.

## Worked examples

These few-shot examples are the generalization signal. The compiler keeps 5 to 10 of them current. Each shows a post, its score, and the rules that drove it.

1. Post: "Shipped a LangGraph multi-agent setup where the planner delegates tool calls to sub-agents. Cut latency 40 percent by parallelizing the retrieval step." Score 95. Fired boost-agent-frameworks, boost-agentic-patterns. Concrete framework plus architecture detail.

2. Post: "Why does the MCP stdio transport silently drop the second tool result? Spent the whole afternoon on this, turns out the server has to flush before the newline." Score 88. Fired boost-mcp, boost-bugfinder-frustration. A real, reproducible failure mode in agent tooling. Prime bug-finder lead.

3. Post: "Added OpenTelemetry spans around our agent loop so we can see tool-call accuracy per trajectory in Honeycomb." Score 82. Fired boost-agent-eval-observability, boost-agentic-patterns. Practitioner observability for agents.

4. Post: "Computer-use agents running in an e2b sandbox finally feel production-ready for browser automation." Score 78. Fired boost-agent-infra. Agent runtime and infra substance.

5. Post: "Hot take: prompt engineering is dead, just use 10 prompts that will change your life, thread below." Score 5. Fired suppress-engagement-bait, suppress-generic-ai-hype. Bait with no substance.

6. Post: "$AGENT presale is live, the first web3 agent token to the moon, airdrop for early holders." Score 0. Fired suppress-crypto-agents. Crypto noise wearing an agent costume.

7. Post: "New model dropped, benchmark scores look great, bigger context window than the last one." Score 28. Fired suppress-pure-llm-no-agent. Model chatter with no agent angle, mild suppress keeps it below threshold.

8. Post: "Our ReAct agent kept looping on the same tool call. Fixed it by adding a scratchpad note of prior actions so it stops repeating itself." Score 90. Fired boost-agentic-patterns, boost-bugfinder-frustration. Pattern plus a fixed failure mode.
