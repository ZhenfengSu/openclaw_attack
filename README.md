# OpenClaw-Attack

An attack-centric research scaffold for studying cross-stage attack chains in open agent systems.

This repository focuses on the attack side first:

- defining a precise threat model
- organizing attack-chain benchmarks
- generating realistic attack environments and traces
- measuring attack trigger, hijack, persistence, and propagation

Defense modules are intentionally out of scope for this repository's first phase.

## Research Focus

We treat an agent attack as a chain instead of a single prompt:

`Attack Entry -> Decision Hijack -> Unsafe or Persistent Outcome`

The core question is not only whether an attack succeeds, but also:

- where it enters
- what decision object it hijacks
- at which step the hijack first happens
- whether it persists into memory or propagates to other agents

## Repository Layout

```text
openclaw_attack/
├── README.md
├── docs/
│   ├── 方案设计.md
│   └── 攻击缺口分析.md
├── schema/
│   ├── attack_case_schema.yaml
│   └── attack_trace_schema.yaml
├── data/
│   ├── README.md
│   └── sample_attack_cases.jsonl
├── attacks/
│   └── README.md
├── src/
│   ├── README.md
│   ├── attack_harness.py
│   └── case_loader.py
└── results/
```

## What This Repo Adds Beyond `openclaw_chainbench_v0`

- an explicit attack-only threat model
- attack coverage organized as a matrix instead of a few starter examples
- attack-specific schemas for cases and traces
- payload and environment abstractions for future attack execution
- metrics for trigger, hijack, persistence, exfiltration, and propagation

## Planned Architecture

### 1. Case Layer

Structured attack cases define:

- benign task
- attacker role and capability
- entry surface and payload carrier
- target asset and intended unsafe action
- hijacked decision object
- expected attack chain and outcome

### 2. Environment Layer

Each benchmark instance should materialize a realistic environment:

- email inbox
- calendar
- local workspace
- web or search results
- RAG corpus
- MCP or skill metadata
- upstream agent outputs

### 3. Attack Payload Layer

Payload templates should support:

- direct instruction variants
- stealthy recommendation variants
- policy-like or metadata-like variants
- single-turn and multi-turn variants
- persistence-seeking and propagation-seeking variants

### 4. Execution Layer

The attack harness should:

- instantiate an environment from a case
- inject payloads into the correct surface
- run the target agent through the local OpenClaw installation
- export step-level traces matching `schema/attack_trace_schema.yaml`

### 5. Analysis Layer

Trace analysis should measure:

- attack trigger rate
- first hijack step
- hijack rate by decision object
- unsafe action rate
- exfiltration success
- privilege escalation success
- persistence success
- cross-turn or cross-agent propagation

## Suggested Build Order

1. Finalize threat model and schema.
2. Expand cases to a coverage-driven benchmark.
3. Build payload templates and environment generators.
4. Implement a real attack harness.
5. Add trace analyzers and reporting.

## Current Status

This repository is a design-complete scaffold.

It already includes:

- a rewritten attack-focused plan
- a gap analysis for missing attack capabilities
- an extensible case schema
- an extensible trace schema
- starter attack cases

It does not yet include:

- a finished local OpenClaw runner
- automatic environment builders
- large-scale payload libraries

## Local OpenClaw Integration Direction

This repository should talk to your local OpenClaw installation instead of calling model APIs directly.

In your current local setup:

- model selection already lives in `~/.openclaw/openclaw.json`
- the default agent model is `moonshot/kimi-k2.5`
- the Gateway is configured on `ws://127.0.0.1:18789`

That means `openclaw_attack` should not add its own Kimi client unless you explicitly want a direct-model baseline outside OpenClaw.

## Which OpenClaw Entry Point Fits Attack Experiments

### `openclaw agent`

Best default entry point for attack experiments.

Why:

- it exercises the real Agent stack, not just raw model inference
- it respects the OpenClaw model layer, so your configured Kimi backend is used automatically
- it is the closest surface to real user-facing behavior
- it is the right place to observe prompt injection, tool-choice drift, planning drift, memory contamination, and multi-step behavior

### `openclaw gateway`

Best secondary entry point for automation and deeper instrumentation.

Why:

- it is the underlying WebSocket RPC control plane
- `gateway call <method>` is useful when you want structured RPC, subscriptions, or low-level inspection
- it is a better fit than `agent` when you later need event streaming, transcript subscription, or direct RPC methods like `agent.wait`

### `openclaw capability` / `openclaw infer`

Useful for model-only baselines, but not ideal as the main attack entry.

Why:

- it runs provider-backed inference
- it is good for comparing raw model susceptibility
- but it does not represent the full OpenClaw agent runtime, so it misses parts of the real attack surface

### `openclaw health`

Not an attack entry point.

Why:

- it is only for checking gateway health and channel readiness
- it should be used as a preflight check before experiments, not as the experiment runner

## Recommended Experiment Path

1. Use `openclaw health --json` or `openclaw gateway status --require-rpc --json` as a preflight check.
2. Use `openclaw agent` as the default attack execution entry.
3. Add `openclaw gateway call ... --expect-final` later when you need structured RPC automation or richer trace collection.
4. Reserve `openclaw capability` for ablations that intentionally bypass the full agent stack.
