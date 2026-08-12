from typing import Dict, Any

from day1_single_agent.city import get_current_time, get_forecast, convert_timezone

TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "get_current_time": {
        "func": get_current_time,
        "description": "to get the current time and weather for a specific city."
    },
    "get_forecast": {
        "func": get_forecast,
        "description": "for weather forecast questions."
    },
    "convert_timezone": {
        "func": convert_timezone,
        "description": "to convert a specific time from one city's timezone to another."
    }
}


def format_tool_instructions(available_cities: list) -> str:
    """
    Generates a natural language instruction string based on the tool registry.
    """
    phrases = []

    # Generate usage instructions dynamically
    for name, meta in TOOL_REGISTRY.items():
        phrases.append(f"Use the '{name}' tool {meta['description'].lower()}")

    # Join phrases and append city list
    base_instruction = (
            "You are a helpful assistant that tells the current time and weather in cities. "
            + ". ".join(phrases) + ". "
            + f"Cities currently available: {available_cities}"
    )

    return base_instruction