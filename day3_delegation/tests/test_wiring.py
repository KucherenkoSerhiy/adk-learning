"""Structural checks for day3's dynamic-delegation wiring. No LLM call.

Same note as day2_pipeline/test_wiring.py: these are acceptance criteria for
the finished exercise, expected to fail until the TODOs in day3's agent.py
are done.
"""
from day3_delegation import agent


def test_root_agent_is_defined():
    assert hasattr(agent, "root_agent")


def test_all_three_specialists_are_wired_in():
    assert len(agent.root_agent.sub_agents) == 3


def test_research_specialist_description_was_rewritten():
    """The starter description ("Does research stuff.") is intentionally too
    vague to route on — this fails until it's replaced with something specific."""
    assert agent.research_specialist.description.strip().lower() != "does research stuff."
    assert len(agent.research_specialist.description) > 30


def test_fact_checker_has_a_description():
    assert len(agent.fact_checker.description) > 20


def test_specialist_descriptions_are_distinguishable():
    """Routing quality depends on descriptions being different enough for the
    model to pick between — identical/near-empty descriptions can't route."""
    assert agent.research_specialist.description.strip() != agent.fact_checker.description.strip()


def test_coordinator_instruction_gives_routing_guidance_not_just_a_roster():
    instruction = agent.root_agent.instruction
    for name in ["research_specialist", "headline_specialist", "fact_checker"]:
        assert name in instruction
    assert len(instruction) > 200
