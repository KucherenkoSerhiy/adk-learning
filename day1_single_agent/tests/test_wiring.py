"""Structural checks on how day1's agent is configured — not on tool logic
(that's test_tools.py) and not on LLM behavior (that's test_agent.py).
"""
from day1_single_agent import agent


def test_root_agent_is_defined():
    assert hasattr(agent, "root_agent")


def test_root_agent_has_both_tools_wired():
    """TODO 2 + TODO 4."""
    tool_names = {getattr(t, "__name__", "") for t in agent.root_agent.tools}
    assert {"get_current_time", "get_forecast"} <= tool_names


def test_instruction_mentions_the_forecast_tool():
    """TODO 3."""
    instruction = agent.root_agent.instruction.lower()
    assert "forecast" in instruction or "weather" in instruction
