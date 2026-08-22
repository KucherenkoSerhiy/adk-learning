from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.load_memory_tool import LoadMemoryTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

MODEL = "gemini-flash-latest"
MOCK_LOGS = {
    "payments-service": ["ConnectionResetError: connection reset by peer at 03:14 UTC"],
    "inventory-service": ["NullPointerException in InventoryCheck.java:142"],
}


def get_logs(service: str) -> list[str]:
    """returns list of logs for specified service"""
    if service not in MOCK_LOGS:
        return [f"No log data available for service {service}"]
    return MOCK_LOGS[service]


async def remember_this_conversation(callback_context: CallbackContext):
    await callback_context.add_events_to_memory(
        events=callback_context.session.events
    )


oncall_triage_agent = Agent(
    name="oncall_triage_agent",
    model=MODEL,
    description=(
        "Reviews service logs and recalls which errors were already explained "
        "as known, non-actionable issues, flagging only genuinely new ones."
    ),
    instruction=(
        "You are an oncall triage agent. You remember past conversations when you had any. "
        "Use get_logs to get logs when a request involves checking if something went wrong. "
        "If a log entry matches something you were previously told is a known, already-explained "
        "issue, say so instead of raising it as new. Only flag entries you have not seen explained before."
    ),
    tools=[get_logs, PreloadMemoryTool(), LoadMemoryTool()],
    after_agent_callback=remember_this_conversation
)

root_agent = oncall_triage_agent
