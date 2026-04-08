from __future__ import annotations

from .exceptions import WorkflowError
from .models import Step, Workflow


def validate_workflow(workflow: Workflow) -> None:
    if not workflow.name:
        raise WorkflowError("Workflow name is required.")
    if not workflow.goal:
        raise WorkflowError("Workflow goal is required.")
    if not workflow.steps:
        raise WorkflowError("Workflow must contain at least one step.")
    if not workflow.output_variable:
        raise WorkflowError("Workflow output.variable is required.")

    seen_names: set[str] = set()
    for step in workflow.steps:
        _validate_step(step)
        if step.name in seen_names:
            raise WorkflowError(f"Duplicate step name: {step.name}")
        seen_names.add(step.name)


def _validate_step(step: Step) -> None:
    if step.kind not in {"tool", "model"}:
        raise WorkflowError(f"Unsupported step kind '{step.kind}' in step '{step.name}'.")

    if step.kind == "tool" and not step.tool:
        raise WorkflowError(f"Tool step '{step.name}' is missing the tool field.")

    if step.kind == "model" and not step.instruction:
        raise WorkflowError(f"Model step '{step.name}' is missing the instruction field.")
