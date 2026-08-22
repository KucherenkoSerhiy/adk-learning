from google.adk.tools.load_memory_tool import LoadMemoryTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from day5_memory import agent


def test_root_agent_is_defined():
    assert hasattr(agent, "root_agent")


def test_memory_tools_are_wired_in():
    tool_types = [type(t) for t in agent.root_agent.tools]
    assert PreloadMemoryTool in tool_types
    assert LoadMemoryTool in tool_types


def test_after_agent_callback_is_wired_in():
    assert agent.root_agent.after_agent_callback is not None


def test_instruction_operationalizes_known_vs_new():
    """Remembering something is useless if the agent isn't told what to do
    with it similar to 'say I don't know' line."""
    instruction = agent.root_agent.instruction.lower()
    assert "known" in instruction
    assert "new" in instruction


def test_get_logs_known_service_returns_expected_error():
    result = agent.get_logs("payments-service")
    assert any("ConnectionResetError" in line for line in result)


def test_get_logs_unknown_service_does_not_raise():
    result = agent.get_logs("nonexistent-service")
    assert isinstance(result, list)
    assert "no log data" in result[0].lower()
