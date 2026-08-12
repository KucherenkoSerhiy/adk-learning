"""Behavior tests for day3's coordinator — real model calls via ../../testutils.py.
Excluded by default; run with `pytest -m integration`.

These three cases are exactly the manual scenarios day3's README asks you to
try by hand in `adk web` — turned into automated assertions so you don't have
to keep re-checking them manually every time you tweak a description.
"""
import pytest

from day3_delegation.agent import root_agent
from testutils import start_conversation

pytestmark = pytest.mark.integration


@pytest.mark.parametrize(
    "message, expected_specialist",
    [
        ("Is it true that 5G causes illness?", "fact_checker"),
        ("Give me background on renewable energy policy.", "research_specialist"),
        ("Make this headline punchier: 'Local Council Meets Tuesday'.", "headline_specialist"),
    ],
)
def test_coordinator_routes_to_the_right_specialist(message, expected_specialist):
    conversation = start_conversation(root_agent)
    conversation.send(message)

    authors = {event.author for event in conversation.last_events if event.author}
    assert expected_specialist in authors, f"expected {expected_specialist} in {authors}"
