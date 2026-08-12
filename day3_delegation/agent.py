"""
Day 3 — dynamic delegation via sub_agents.

This is the one closest to what you already built before: a coordinator
that looks at a request and hands it to the right specialist, rather than running
a fixed script. The mechanism is genuinely worth understanding precisely, because
it's easy to misuse:

The model decides who to delegate to by reading each sub-agent's `description`
field plus the coordinator's own `instruction`. There is no routing config, no
keyword matcher — it's all natural language the model reasons over. That means a
vague description silently produces bad routing, with no error to catch it.
That's the failure mode this exercise is built to make you feel.

Scenario: an editorial desk (sound familiar) with three specialists.
"""

from google.adk.agents import Agent

MODEL = "gemini-flash-latest"


def lookup_fact(claim: str) -> dict:
    """Looks up whether a factual claim is well-supported (mocked)."""
    shaky = {"the earth is flat", "5g causes illness"}
    return {
        "claim": claim,
        "verdict": "disputed" if claim.lower() in shaky else "plausible",
    }


def suggest_headline(topic: str) -> dict:
    """Suggests a punchier headline for a given topic (mocked)."""
    return {"topic": topic, "headline": f"{topic}: What Nobody's Telling You"}


research_specialist = Agent(
    name="research_specialist",
    model=MODEL,
    instruction=(
        "You research background context and verify claims. Use the lookup_fact "
        "tool whenever a request involves checking whether something is true."
    ),
    # TODO 1: this description is what the coordinator reads to decide whether to
    # route here. Right now it's too vague to distinguish this agent from
    # fact_checker below. Rewrite it to be specific about WHAT KIND of research
    # (background/context gathering) vs. fact_checker's job (verdict on a claim).
    description="Does research stuff.",
    tools=[lookup_fact],
)

headline_specialist = Agent(
    name="headline_specialist",
    model=MODEL,
    instruction="You write and sharpen headlines using the suggest_headline tool.",
    description=(
        "Writes and rewrites headlines to be sharper and more attention-grabbing "
        "without changing the underlying facts. Use for requests specifically "
        "about titles, headlines, or hooks."
    ),
    tools=[suggest_headline],
)

fact_checker = Agent(
    name="fact_checker",
    model=MODEL,
    instruction=(
        "You give a clear verdict — supported, disputed, or unverifiable — on a "
        "specific claim, using the lookup_fact tool. You don't gather general "
        "background; you rule on one claim at a time."
    ),
    # TODO 2: write this one yourself, following the pattern above. Make it
    # different enough from research_specialist's description that a human
    # skimming both could tell which to pick without reading the agent names.
    description="",
    tools=[lookup_fact],
)

root_agent = Agent(
    name="editorial_coordinator",
    model=MODEL,
    description="Routes editorial requests to the right specialist.",
    instruction=(
        "You coordinate an editorial desk with three specialists: "
        "'research_specialist', 'headline_specialist', and 'fact_checker'. "
        # TODO 3: this instruction currently only tells the model the specialists
        # exist — it doesn't say WHEN to use each one. Add 2-3 sentences of
        # explicit routing guidance (e.g., "if the user asks to verify a specific
        # claim, delegate to fact_checker; if they want background context on a
        # topic, delegate to research_specialist; ..."). Without this, routing
        # quality depends entirely on the sub-agent descriptions above — which is
        # exactly the fragility worth noticing.
    ),
    # TODO 4: wire all three specialists in here.
    sub_agents=[],
)
