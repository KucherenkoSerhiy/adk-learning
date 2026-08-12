"""
Day 1 — one Agent, one tool.

This is the atomic unit everything else in ADK is built from: a single LLM-backed
agent with a plain Python function as a "tool" it can decide to call.

TASK: fill in the TODOs below. Nothing here needs internet/GCP concepts you don't
already know — it's a Python function + a config object.
"""
from google.adk.agents import Agent

MODEL = "gemini-flash-latest"  # check aistudio.google.com/apikey for current model names


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    TODO 1: This is a mock — it always says "10:30 AM" no matter the city.
    Replace the body so it actually returns different times for at least 3 cities
    you hardcode (a dict lookup is fine — no need for a real timezone library yet).
    Keep the return shape: {"status": "success", "city": ..., "time": ...}.
    On an unknown city, return {"status": "error", "message": f"no data for {city}"}.
    """
    return {"status": "success", "city": city, "time": "10:30 AM"}


# TODO 2: Write a second tool function, `get_forecast(city: str) -> dict`, that
# mock-returns a one-word weather condition for the same cities you used above.
# Same rules: type-hinted, has a docstring (ADK uses it to help the model decide
# when to call the tool), returns a dict with a "status" key.


root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description="Tells the current time and weather in a specified city.",
    instruction=(
        "You are a helpful assistant that tells the current time and weather in "
        "cities. Use the 'get_current_time' tool for time questions."
        # TODO 3: extend this instruction so the model also knows to call your
        # new get_forecast tool for weather questions. Be explicit — ADK routes
        # tool calls off of what you say here plus each tool's docstring.
    ),
    tools=[get_current_time],  # TODO 4: add get_forecast once you've written it
)
