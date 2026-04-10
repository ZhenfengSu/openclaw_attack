# Source Layout

The `src/` directory is intentionally small for now.

Its initial responsibility is to host the future attack execution pipeline:

- case loading and validation
- environment materialization
- payload injection
- target runtime execution
- trace export
- metric computation

## Planned modules

- `case_loader.py`: load and validate JSONL attack cases
- `attack_harness.py`: orchestrate execution and trace collection
- `environment_builders/`: domain-specific benchmark environments
- `trace_analysis/`: attack-specific metrics and reporting
