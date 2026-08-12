"""Behavior test for day2's pipeline — real model call via ../../testutils.py.
Excluded by default; run with `pytest -m integration`.

There are no tools here to assert calls against (writer/reviewer/refactorer
are plain LLM agents), so the behavior signal instead is *which sub-agent
authored each event* and in what order — available on `Conversation.last_events`
after a `.send()`. That's still a behavior assertion, not a wording match: it
doesn't care what the generated code says, only that all three stages ran, in
the fixed order SequentialAgent promises.
"""
import pytest

from day2_pipeline.agent import root_agent
from testutils import start_conversation

pytestmark = pytest.mark.integration


def test_pipeline_runs_writer_then_reviewer_then_refactorer_in_order():
    conversation = start_conversation(root_agent)
    _, final_text = conversation.send("Write a function that reverses a linked list.")

    authors_in_order = [event.author for event in conversation.last_events if event.author]

    writer_idx = authors_in_order.index("CodeWriterAgent")
    reviewer_idx = authors_in_order.index("CodeReviewerAgent")
    refactorer_idx = authors_in_order.index("CodeRefactorerAgent")
    assert writer_idx < reviewer_idx < refactorer_idx

    assert "```" in final_text
