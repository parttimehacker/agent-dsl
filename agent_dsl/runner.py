from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .engine import ExecutionContext, execute_step
from .exceptions import WorkflowError
from .models import Step, Workflow
from .validators import validate_workflow


def load_workflow(path: str | Path) -> Workflow:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    steps = [
        Step(
            name=item["name"],
            kind=item["kind"],
            bind=item.get("bind"),
            tool=item.get("tool"),
            args=item.get("args", {}),
            instruction=item.get("instruction"),
            source=item.get("source"),
        )
        for item in raw.get("steps", [])
    ]

    workflow = Workflow(
        name=raw["name"],
        goal=raw["goal"],
        inputs=raw.get("inputs", {}),
        policy=raw.get("policy", {}),
        steps=steps,
        output_variable=raw["output"]["variable"],
    )
    validate_workflow(workflow)
    return workflow


def run_workflow(path: str | Path) -> dict[str, Any]:
    workflow = load_workflow(path)
    context = ExecutionContext(workflow)

    for step in workflow.steps:
        execute_step(step, context)

    if workflow.output_variable not in context.variables:
        raise WorkflowError(
            f"Output variable '{workflow.output_variable}' was never produced by the workflow."
        )

    result = {
        "workflow": workflow.name,
        "goal": workflow.goal,
        "tool_calls": context.tool_calls,
        "output": context.variables[workflow.output_variable],
        "variables": context.variables,
    }

    if workflow.policy.get("require_non_empty_output") and not result["output"]:
        raise WorkflowError("Policy violation: output is empty.")

    return result
