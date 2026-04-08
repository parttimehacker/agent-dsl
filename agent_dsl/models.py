from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Step:
    name: str
    kind: str
    bind: str | None = None
    tool: str | None = None
    args: dict[str, Any] = field(default_factory=dict)
    instruction: str | None = None
    source: str | None = None


@dataclass(slots=True)
class Workflow:
    name: str
    goal: str
    inputs: dict[str, Any]
    policy: dict[str, Any]
    steps: list[Step]
    output_variable: str
