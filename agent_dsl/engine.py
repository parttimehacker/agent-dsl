from __future__ import annotations

import re
from typing import Any

from .exceptions import WorkflowError
from .models import Step, Workflow
from .tools import TOOL_REGISTRY


_PATTERN = re.compile(r"\$\{([^}]+)\}")


class ExecutionContext:
    def __init__(self, workflow: Workflow) -> None:
        self.workflow = workflow
        self.variables: dict[str, Any] = {}
        self.tool_calls = 0

    def resolve(self, value: Any) -> Any:
        if isinstance(value, str):
            matches = list(_PATTERN.finditer(value))
            if not matches:
                return value
            if len(matches) == 1 and matches[0].span() == (0, len(value)):
                return self._lookup(matches[0].group(1))
            return _PATTERN.sub(lambda m: str(self._lookup(m.group(1))), value)
        if isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self.resolve(v) for v in value]
        return value

    def _lookup(self, path: str) -> Any:
        parts = path.split(".")
        if parts[0] == "inputs":
            current: Any = self.workflow.inputs
            parts = parts[1:]
        else:
            current = self.variables.get(parts[0])
            parts = parts[1:]
        for part in parts:
            if isinstance(current, dict):
                current = current[part]
            else:
                current = getattr(current, part)
        return current


def execute_step(step: Step, context: ExecutionContext) -> None:
    if step.kind == "tool":
        _execute_tool_step(step, context)
        return
    if step.kind == "model":
        _execute_model_step(step, context)
        return
    raise WorkflowError(f"Unsupported step kind: {step.kind}")


def _execute_tool_step(step: Step, context: ExecutionContext) -> None:
    max_tool_calls = int(context.workflow.policy.get("max_tool_calls", 100))
    if context.tool_calls >= max_tool_calls:
        raise WorkflowError("Policy violation: max_tool_calls exceeded.")

    tool = TOOL_REGISTRY.get(step.tool or "")
    if tool is None:
        raise WorkflowError(f"Unknown tool: {step.tool}")

    resolved_args = context.resolve(step.args)
    result = tool(**resolved_args)
    context.tool_calls += 1

    if step.bind:
        context.variables[step.bind] = result


def _execute_model_step(step: Step, context: ExecutionContext) -> None:
    source_value = context.variables.get(step.source or "")
    instruction = step.instruction or ""

    if isinstance(source_value, list):
        summary = f"{instruction}\n\nItems reviewed: {len(source_value)}.\n"
        for idx, item in enumerate(source_value[:5], start=1):
            summary += f"{idx}. {item}\n"
    else:
        summary = f"{instruction}\n\nSource:\n{source_value}"

    if step.bind:
        context.variables[step.bind] = summary
