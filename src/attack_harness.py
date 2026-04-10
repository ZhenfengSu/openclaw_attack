from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from case_loader import load_jsonl
from openclaw_runner import (
    OpenClawRuntimeConfig,
    build_case_prompt,
    run_agent_turn,
    run_preflight,
)


@dataclass
class AttackRunConfig:
    backend: str
    case_path: str
    out_path: str
    case_ids: Optional[List[str]] = None
    skip_preflight: bool = False


def build_environment(case: Dict) -> Dict:
    """Materialize a small environment summary for prompt construction."""
    return {
        "domain": case.get("domain"),
        "memory_enabled": case.get("requires_memory", False),
        "multi_turn_enabled": case.get("requires_multi_turn", False),
        "delegation_enabled": case.get("requires_delegation", False),
        "tool_chain_enabled": case.get("requires_tool_chain", False),
        "tools_available": [],
    }


def run_case(case: Dict, runtime_config: OpenClawRuntimeConfig) -> Dict:
    environment = build_environment(case)
    prompt = build_case_prompt(case, environment)
    execution = run_agent_turn(prompt=prompt, config=runtime_config)

    return {
        "case_id": case["case_id"],
        "backend": "local_openclaw_agent",
        "status": "completed" if execution["ok"] else "failed",
        "environment": environment,
        "prompt": prompt,
        "command": execution["command"],
        "returncode": execution["returncode"],
        "stdout": execution["stdout"],
        "stderr": execution["stderr"],
        "notes": (
            "Executed through the local OpenClaw CLI using the "
            "`openclaw agent` entry point."
        ),
    }


def run_cases(
    cases: List[Dict],
    runtime_config: OpenClawRuntimeConfig,
) -> List[Dict]:
    return [run_case(case, runtime_config) for case in cases]


def select_cases(cases: List[Dict], case_ids: Optional[List[str]]) -> List[Dict]:
    if not case_ids:
        return cases
    case_id_set = set(case_ids)
    return [case for case in cases if case.get("case_id") in case_id_set]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run attack cases through the local OpenClaw agent.",
    )
    parser.add_argument(
        "--case-path",
        default="data/sample_attack_cases.jsonl",
        help="Path to the JSONL attack case file.",
    )
    parser.add_argument(
        "--out-path",
        default="results/attack_runs.json",
        help="Path to write the JSON results.",
    )
    parser.add_argument(
        "--case-id",
        action="append",
        dest="case_ids",
        help="Run only the specified case id. Repeat for multiple cases.",
    )
    parser.add_argument(
        "--openclaw-command",
        default="openclaw",
        help="OpenClaw CLI command name or absolute path.",
    )
    parser.add_argument(
        "--profile",
        help="Optional OpenClaw profile passed through to the CLI.",
    )
    parser.add_argument(
        "--container",
        help="Optional container name passed through to the CLI.",
    )
    parser.add_argument(
        "--agent-name",
        default="main",
        help="Agent name passed as `openclaw agent --agent` when no `--agent-target` or `--session-id` is set.",
    )
    parser.add_argument(
        "--agent-target",
        help="Optional `openclaw agent --to` target.",
    )
    parser.add_argument(
        "--session-id",
        help="Optional `openclaw agent --session-id` override.",
    )
    parser.add_argument(
        "--deliver",
        action="store_true",
        help="Pass `--deliver` to `openclaw agent`.",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip `openclaw gateway status --require-rpc --json` before running.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=180,
        help="Per-case timeout for the OpenClaw CLI call.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    harness_config = AttackRunConfig(
        backend="local_openclaw_agent",
        case_path=args.case_path,
        out_path=args.out_path,
        case_ids=args.case_ids,
        skip_preflight=args.skip_preflight,
    )
    runtime_config = OpenClawRuntimeConfig(
        cli_command=args.openclaw_command,
        profile=args.profile,
        container=args.container,
        agent_name=args.agent_name,
        agent_target=args.agent_target,
        session_id=args.session_id,
        deliver=args.deliver,
        timeout_seconds=args.timeout_seconds,
    )

    cases = load_jsonl(harness_config.case_path)
    selected_cases = select_cases(cases, harness_config.case_ids)
    if not selected_cases:
        raise SystemExit("No cases selected. Check --case-id or the case file.")

    preflight = None
    if not harness_config.skip_preflight:
        preflight = run_preflight(runtime_config)
        if not preflight["ok"]:
            results = {
                "run_started_at": utc_now(),
                "config": asdict(harness_config),
                "runtime": asdict(runtime_config),
                "preflight": preflight,
                "results": [],
            }
            write_results(args.out_path, results)
            raise SystemExit(
                "OpenClaw preflight failed. Inspect the output JSON for details."
            )

    results = {
        "run_started_at": utc_now(),
        "config": asdict(harness_config),
        "runtime": asdict(runtime_config),
        "preflight": preflight,
        "results": run_cases(selected_cases, runtime_config),
    }
    write_results(args.out_path, results)
    print(
        f"Wrote {len(results['results'])} result(s) to {args.out_path}",
    )
    return 0


def write_results(path: str, payload: Dict) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
