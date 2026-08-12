"""Shared helper for integration tests that actually drive an agent through
ADK's Runner. Kept at the repo root (imported by every day folder's
test_agent.py) so the tool-call/state extraction logic exists exactly once.

Pattern (InMemoryRunner + async session creation via asyncio.run, then the
synchronous runner.run() generator) verified against ADK docs/community
examples as of 2026-08-12. If this errors on `create_session`, the Runner API
likely shifted between ADK versions — check `python -c "from google.adk.runners
import InMemoryRunner; help(InMemoryRunner)"` against what's installed.
"""
import asyncio
import uuid
from dataclasses import dataclass, field

from google.adk.runners import InMemoryRunner
from google.genai import types


@dataclass
class Conversation:
    """One session against one agent, reusable across multiple turns — use
    this when a test needs the agent to remember an earlier message, or to
    inspect which sub-agents ran, same as watching the Events panel in
    `adk web`."""

    runner: InMemoryRunner
    user_id: str
    session_id: str
    last_events: list = field(default_factory=list)

    def send(self, message: str):
        """Send one message in this conversation. Returns (tool_calls, final_text).
        Full raw events from this turn are also stashed in `self.last_events`
        for tests that need more than tool calls + text — e.g. which
        sub-agent authored a response (`event.author`)."""
        content = types.Content(role="user", parts=[types.Part.from_text(text=message)])

        events = list(
            self.runner.run(user_id=self.user_id, session_id=self.session_id, new_message=content)
        )
        self.last_events = events

        tool_calls = []
        final_text = ""
        for event in events:
            for call in event.get_function_calls() or []:
                tool_calls.append((call.name, dict(call.args or {})))
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text:
                    final_text = text

        return tool_calls, final_text


def start_conversation(agent, *, app_name: str = "adk-learning-tests") -> Conversation:
    runner = InMemoryRunner(agent=agent, app_name=app_name)
    user_id = f"test-user-{uuid.uuid4().hex[:8]}"
    session = asyncio.run(
        runner.session_service.create_session(app_name=app_name, user_id=user_id)
    )
    return Conversation(runner=runner, user_id=user_id, session_id=session.id)


def run_agent_turn(agent, message: str, *, app_name: str = "adk-learning-tests"):
    """Convenience wrapper for a single-turn test — see Conversation for
    multi-turn. Returns (tool_calls, final_text)."""
    return start_conversation(agent, app_name=app_name).send(message)
