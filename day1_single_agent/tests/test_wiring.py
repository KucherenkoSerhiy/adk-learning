from day1_single_agent import agent


def test_root_agent_is_defined():
    assert hasattr(agent, "root_agent")


def test_root_agent_has_the_three_expected_tools():
    tool_names = {getattr(t, "__name__", "") for t in agent.root_agent.tools}
    assert {"get_current_time", "get_forecast", "convert_timezone"} <= tool_names


def test_instruction_mentions_every_wired_tool_by_name():
    instruction = agent.root_agent.instruction.lower()
    for tool in agent.root_agent.tools:
        assert tool.__name__.lower() in instruction, f"{tool.__name__} not mentioned in instruction"
