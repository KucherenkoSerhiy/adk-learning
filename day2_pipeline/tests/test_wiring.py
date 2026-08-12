"""Structural checks for day2's SequentialAgent wiring. No LLM call.

These are written to hold once the day2 TODOs are filled in — right now, on
an unsolved exercise, they're expected to fail. That's the point: they're
acceptance criteria, not a status report on work already done.
"""
from day2_pipeline import agent


def test_root_agent_is_defined():
    assert hasattr(agent, "root_agent")


def test_pipeline_has_exactly_three_sub_agents():
    assert len(agent.root_agent.sub_agents) == 3


def test_sub_agents_run_writer_then_reviewer_then_refactorer():
    names = [a.name for a in agent.root_agent.sub_agents]
    assert names == ["CodeWriterAgent", "CodeReviewerAgent", "CodeRefactorerAgent"]


def test_reviewer_output_key_is_review_comments():
    assert agent.code_reviewer_agent.output_key == "review_comments"


def test_refactorer_instruction_references_review_comments():
    assert "{review_comments}" in agent.code_refactorer_agent.instruction
