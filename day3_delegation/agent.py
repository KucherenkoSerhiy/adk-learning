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
    description="Gathers the data by doing research.",
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
    description="Verifies whether the gathered data is supported, disputed, or unverifiable",
    tools=[lookup_fact],
)

source_checker = Agent(
    name="source_checker",
    model=MODEL,
    instruction=(
        "You look into whether background information on a topic is accurate, "
        "gathering and verifying supporting research as needed. Use the lookup_fact "
        "tool when you need to check specific facts."
    ),
    description="Gathers and verifies background information on a topic.",
    tools=[lookup_fact],
)

root_agent = Agent(
    name="editorial_coordinator",
    model=MODEL,
    description="Routes editorial requests to the right specialist.",
    instruction=(
        "You coordinate an editorial desk with three specialists: "
        "'research_specialist', 'headline_specialist', and either 'fact_checker' "
        "or 'source_checker', since the last two are same just spelled differently inside current scope. "
        "Use them to gather the research data, get a headline, and verify claims "
        "in the research respectively."
    ),
    sub_agents=[research_specialist, headline_specialist, fact_checker, source_checker],
)
