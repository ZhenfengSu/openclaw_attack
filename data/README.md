# Data Overview

`sample_attack_cases.jsonl` contains a small starter set of attack-chain cases for schema validation only.

`simulated_attack_cases.jsonl` contains richer cross-domain cases designed for
the current prompt-only harness. These are better for immediate manual
inspection because each case embeds a fuller simulated artifact.

`web_search_live_attack_cases.jsonl` contains live local-MCP cases for isolated
web-search poisoning.

`rag_live_attack_cases.jsonl` contains live local-MCP cases for isolated rag
retrieval poisoning.

`mcp_live_attack_cases.jsonl` contains live MCP metadata-hijack cases.

`skill_live_attack_cases.jsonl` contains live local-skill metadata and
memory-seed cases.

`email_workspace_attack_cases.jsonl` contains email attack cases backed by the
local virtual mail system. Each run seeds a mailbox scenario before prompting
the agent.

It is not yet a representative benchmark.

## Future data organization

- `cases/`: finalized benchmark cases
- `payloads/`: reusable payload templates and variants
- `env_presets/`: serialized environment states
- `references/`: benign reference traces or expected plans

## Design rule

Cases should describe the attack chain structurally.
Payload text variants should be versioned separately when possible.
