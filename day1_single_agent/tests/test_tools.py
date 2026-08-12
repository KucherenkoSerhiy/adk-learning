"""Pure-function tests for day1's tool implementations. No LLM call, no
network, no API key — these should run in milliseconds and pass/fail
deterministically every time.
"""
from day1_single_agent import agent


def test_get_current_time_varies_by_city():
    """TODO 1: right now this always returns "10:30 AM" no matter the city."""
    r1 = agent.get_current_time("Berlin")
    r2 = agent.get_current_time("Tokyo")
    assert r1["time"] != r2["time"]


def test_get_current_time_errors_on_unknown_city():
    """TODO 1."""
    assert agent.get_current_time("Nowhereville")["status"] == "error"


def test_get_forecast_exists_and_returns_a_status():
    """TODO 2: write get_forecast(city: str) -> dict in agent.py."""
    assert hasattr(agent, "get_forecast"), "get_forecast is not defined yet (TODO 2)"
    result = agent.get_forecast("Berlin")
    assert isinstance(result, dict)
    assert "status" in result
