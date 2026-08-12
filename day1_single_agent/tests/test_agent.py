"""Behavior tests for day1's agent — real calls through the model via
../../testutils.py. Costs tokens, needs GOOGLE_API_KEY set. Excluded by
default; run explicitly:

    pytest -m integration

Assert on which tool got called and with what argument — never on exact
wording, since the model is free to phrase its answer differently each run.
"""
import pytest

from day1_single_agent.agent import root_agent
from testutils import run_agent_turn

pytestmark = pytest.mark.integration


def test_agent_answers_a_direct_time_question_via_get_current_time():
    tool_calls, _ = run_agent_turn(root_agent, "What time is it in Tokyo right now?")

    time_call_args = next(args for name, args in tool_calls if name == "get_current_time")
    assert time_call_args.get("city") == "Tokyo"


def test_agent_answers_a_forecast_question_via_get_forecast():
    """TODO 2/3/4: only passes once get_forecast exists, is wired in, and the
    instruction actually tells the model when to reach for it."""
    tool_calls, _ = run_agent_turn(root_agent, "What's the weather forecast in Berlin?")

    called_names = [name for name, _ in tool_calls]
    assert "get_forecast" in called_names
