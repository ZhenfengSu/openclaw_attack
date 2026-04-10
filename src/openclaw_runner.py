from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class OpenClawRuntimeConfig:
    gateway_url: str = "ws://127.0.0.1:18789"
    cli_command: str = "openclaw"
    preferred_entrypoint: str = "agent"


def select_experiment_entrypoint() -> Dict[str, str]:
    """Return the recommended OpenClaw entrypoints for attack experiments.

    `agent` is the default because it exercises the real agent stack and
    inherits the model configured inside OpenClaw.
    `gateway` is the advanced path for structured RPC automation.
    """
    return {
        "primary": "agent",
        "secondary": "gateway",
        "baseline_only": "capability",
        "preflight": "health",
    }
