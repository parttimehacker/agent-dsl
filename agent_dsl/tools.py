from __future__ import annotations

from typing import Any, Callable


ToolFn = Callable[..., Any]


def search_web(query: str) -> list[dict[str, str]]:
    """Deterministic stub for repository demos."""
    return [
        {
            "title": "Protocol initiative A",
            "summary": f"Sample result related to: {query}",
            "source": "example.org/a",
        },
        {
            "title": "Protocol initiative B",
            "summary": f"Another sample result related to: {query}",
            "source": "example.org/b",
        },
    ]


def echo(value: Any) -> Any:
    return value


def structurehub_check(temp_c: float, hum_pct: float, dew_point_c: float) -> dict[str, Any]:
    risk = "normal"
    if dew_point_c >= 18:
        risk = "elevated"
    if dew_point_c >= 21:
        risk = "high"
    return {
        "temp_c": temp_c,
        "hum_pct": hum_pct,
        "dew_point_c": dew_point_c,
        "risk": risk,
        "message": f"Environment risk is {risk}.",
    }


TOOL_REGISTRY: dict[str, ToolFn] = {
    "search_web": search_web,
    "echo": echo,
    "structurehub_check": structurehub_check,
}
