from pathlib import Path

from agent_dsl.runner import run_workflow


def test_ai_protocol_brief_runs() -> None:
    result = run_workflow(Path("examples/ai_protocol_brief.yaml"))
    assert result["workflow"] == "ai_protocol_brief"
    assert result["tool_calls"] == 1
    assert "Items reviewed" in result["output"]


def test_structurehub_signal_check_runs() -> None:
    result = run_workflow(Path("examples/structurehub_signal_check.yaml"))
    assert result["workflow"] == "structurehub_signal_check"
    assert result["tool_calls"] == 1
    assert "Source:" in result["output"]
