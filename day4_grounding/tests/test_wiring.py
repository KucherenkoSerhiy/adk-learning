from day4_grounding import agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval


def test_root_agent_is_defined():
    assert hasattr(agent, "root_agent")


def test_retrieval_tool_is_wired_in():
    tool_types = [type(t) for t in agent.root_agent.tools]
    assert VertexAiRagRetrieval in tool_types


def test_instruction_tells_the_model_to_admit_when_it_does_not_know():
    instruction = agent.root_agent.instruction.lower()
    assert "don't know" in instruction or "doesn't know" in instruction
