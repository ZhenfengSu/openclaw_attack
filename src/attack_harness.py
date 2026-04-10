from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AttackRunConfig:
    backend: str
    case_path: str
    out_path: str


def build_environment(case: Dict) -> Dict:
    """Placeholder for environment materialization."""
    return {
        "domain": case.get("domain"),
        "memory_enabled": case.get("requires_memory", False),
        "delegation_enabled": case.get("requires_delegation", False),
        "tools_available": [],
    }


def run_case(case: Dict) -> Dict:
    """Placeholder for real attack execution.

    This function should eventually:
    1. build the benchmark environment
    2. inject the payload
    3. run the target agent through the local OpenClaw installation
    4. export an attack trace
    """
    env = build_environment(case)
    return {
        "case_id": case["case_id"],
        "backend": "local_openclaw",
        "environment": env,
        "status": "not_implemented",
        "notes": (
            "Use the local OpenClaw runner as the execution backend. "
            "Preferred entry point: `openclaw agent`. "
            "Optional advanced entry point: Gateway RPC via `openclaw gateway call`."
        ),
    }


def run_cases(cases: List[Dict]) -> List[Dict]:
    return [run_case(case) for case in cases]
