# Attack Payload Library

This directory is reserved for reusable attack templates and variants.

## Intended structure

- `web/`: webpage and search-result payloads
- `email/`: email body and thread payloads
- `rag/`: retrieval chunk poisoning payloads
- `memory/`: persistence-seeking payloads
- `mcp/`: MCP and tool metadata payloads
- `multi_agent/`: delegation and handoff payloads

## Template design goals

Each payload family should track:

- template id
- target domain
- target hijack object
- style
- stealth level
- prerequisites
- expected impact

## Important rule

Keep payloads sanitized and research-oriented.
Do not include operational exploit instructions that would meaningfully increase misuse risk.
