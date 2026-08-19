import pytest

from day4_grounding.agent import root_agent
from testutils import run_agent_turn

pytestmark = pytest.mark.integration


def test_agent_uses_retrieval_for_an_in_corpus_question():
    tool_calls, final_text = run_agent_turn(root_agent, "Are ants edible? How do they taste?")
    called_names = [name for name, _ in tool_calls]
    assert "retrieve_ant_docs" in called_names
    assert "sour" in final_text.lower() or "nutty" in final_text.lower()


def test_agent_declines_an_unrelated_question_instead_of_guessing():
    _, final_text = run_agent_turn(root_agent, "Should I pick Toyota or Renault?")
    assert "toyota" not in final_text.lower()
    assert "renault" not in final_text.lower()
