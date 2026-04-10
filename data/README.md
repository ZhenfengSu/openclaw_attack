# Data Overview

`sample_attack_cases.jsonl` contains a small starter set of attack-chain cases for schema validation only.

It is not yet a representative benchmark.

## Future data organization

- `cases/`: finalized benchmark cases
- `payloads/`: reusable payload templates and variants
- `env_presets/`: serialized environment states
- `references/`: benign reference traces or expected plans

## Design rule

Cases should describe the attack chain structurally.
Payload text variants should be versioned separately when possible.
