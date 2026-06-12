# Pre-flight: environment findings

Empirical results from validating the local model and wiring, captured so the build session does not rediscover them.

## Local model

- Ollama serving on `localhost:11434`, bound to `0.0.0.0:11434`, so in-cluster pods can reach the host. Both OpenAI-compat (`/v1`) and native (`/api`) endpoints respond.
- Models present - `qwen3:4b` and `qwen3:8b` (Q4_K_M).

## Invocation recipe

The OpenAI-compat `/v1/chat/completions` endpoint is a trap for qwen3. It routes chain-of-thought into a separate `reasoning` field, ignores a `/no_think` directive, and returns empty `content` when it hits the token cap mid-reasoning. A small `max_tokens` yields nothing usable.

Reliable path - Ollama native `/api/chat` with:

- `"think": false` to suppress the reasoning pass (roughly 20x faster on short tasks).
- a JSON-schema `"format"` grammar to constrain output to a clean structured object. For classification, an `enum` on the label field pins it to the allowed set.

Verified - 4b returns `technical-frustration` for a broken-langchain post (correct, not gated as hate), and 8b returns clean `{score, reason}` JSON.

## Performance and capacity

- Warm throughput - 4b around 80 tok/s, 8b around 58 tok/s. Both are real GPU speeds. A few tok/s instead means CPU fallback from VRAM pressure.
- Cold load - paging weights into VRAM costs several seconds on first call and after eviction. A misleading slow-per-request number is almost always cold load, not inference. The original "14 seconds" measurement was almost entirely cold load.
- GPU - RTX 2080, 8GB. Holds **one** qwen3 quant resident at a time (8b is about 6GB in VRAM). Two do not fit. This is why the live path uses one model and the roll-up scales the live container to zero.
- nvidia-smi caveat - on Windows WDDM it cannot read per-process VRAM and inflates `memory.used` with shared system memory. Use `GET /api/ps` (the `size_vram` field) to confirm a model is GPU-resident, not the CLI.
- `keep_alive` - at trickle firehose rates, set a long `keep_alive` on scorer calls so each post does not re-pay cold load.

## Model endpoint for the chart

The scorer reaches Ollama on the host `kai-desktop-tower`. The chart configmap's model endpoint is `http://<TOWER_WIN_TAILNET_FQDN>:11434/v1`, resolved at deploy time from `/coilysiren/kai-desktop-tower/tailnet-fqdn`. The opaque FQDN stays a placeholder in committed YAML.

## Telemetry

`/coilysiren/signoz/ts-authkey` already exists in SSM. The OTel collector endpoint is env-driven. (The former `/coilysiren/honeycomb/api-key` was deleted in the 2026-06-11 SSM audit - SigNoz is the telemetry target.)

## Secrets and SSM

- `/coilysiren/atmosphere/telegram-bot-token` - SecureString, the bot token. Consumed as a Kubernetes Secret by the telegram-bot and scorer.
- `/coilysiren/atmosphere/telegram-chat-id` - SecureString, value `8711863424`, the target chat captured from `getUpdates`.
- Bot is `@coilysiren_atmosphere_bot`. Validated end to end - `getMe` ok, and a real `sendMessage` round-trip landed in the chat.
- Bluesky - no auth needed for v0. Jetstream is public.
- Model - local Ollama takes a throwaway key on the OpenAI-compat path.

All opaque values stay in SSM per the configs-in-SSM rule. Never hardcode the token, chat id, or tailnet FQDN into committed YAML or code. Never decrypt the token to screen while recording.
