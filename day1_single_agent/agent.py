"""
Day 1 — one Agent, one tool.

This is the atomic unit everything else in ADK is built from: a single LLM-backed
agent with a plain Python function as a "tool" it can decide to call. You've done
the multi-agent-roles version of this before; today is just seeing
ADK's specific syntax for the single-agent case before stacking more on top.

TASK: fill in the TODOs below. Nothing here needs internet/GCP concepts you don't
already know — it's a Python function + a config object.
"""
from google.adk.agents import Agent

from day1_single_agent.city import get_current_time, get_forecast, convert_timezone, CITIES
from day1_single_agent.prompt import format_tool_instructions

MODEL = "gemini-flash-latest"  # check aistudio.google.com/apikey for current model names

# improvement: a dictionary with tool name and method name, then
# a function to format that into a set of phrases for prompt
root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description="Tells the current time and weather in a specified city.",
    instruction=(
        format_tool_instructions(CITIES)
    ),
    tools=[get_current_time, get_forecast, convert_timezone],
)
