import pytest

from day1_single_agent.agent import root_agent
from testutils import run_agent_turn, start_conversation

pytestmark = pytest.mark.integration


def test_agent_answers_a_direct_time_question_via_get_current_time():
    tool_calls, _ = run_agent_turn(root_agent, "What time is it in Tokyo right now?")

    time_call_args = next(args for name, args in tool_calls if name == "get_current_time")
    assert time_call_args.get("city") == "Tokyo"


def test_agent_chains_current_time_and_timezone_conversion_across_a_followup():
    conversation = start_conversation(root_agent)

    first_calls, _ = conversation.send("I am in Berlin, what time is it there?")
    assert "get_current_time" in [name for name, _ in first_calls]

    second_calls, second_text = conversation.send("and what time would that be in Tokyo?")

    called_names = [name for name, _ in second_calls]
    assert "convert_timezone" in called_names

    convert_args = next(args for name, args in second_calls if name == "convert_timezone")
    assert convert_args.get("city_from") == "Berlin"
    assert convert_args.get("city_to") == "Tokyo"

    assert "Tokyo" in second_text
