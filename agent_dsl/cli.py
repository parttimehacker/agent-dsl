from __future__ import annotations

import argparse
import json
import sys

from .exceptions import WorkflowError
from .runner import run_workflow


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an Agent DSL workflow.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a workflow file")
    run_parser.add_argument("workflow", help="Path to a YAML workflow file")

    args = parser.parse_args()

    if args.command == "run":
        try:
            result = run_workflow(args.workflow)
        except WorkflowError as exc:
            print(f"Workflow failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2, default=str))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
