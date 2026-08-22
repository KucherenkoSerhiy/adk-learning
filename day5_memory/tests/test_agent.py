import asyncio
import uuid

import pytest
from google.adk.memory import VertexAiMemoryBankService
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.genai import types

from day5_memory.agent import root_agent
from day5_memory.tools.constants import AGENT_ENGINE_ID, LOCATION, PROJECT

pytestmark = pytest.mark.integration

APP_NAME = "day5-memory-test"


def _new_runner():
    session_service = VertexAiSessionService(
        project=PROJECT, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID
    )
    memory_service = VertexAiMemoryBankService(
        project=PROJECT, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID
    )
    return Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )


def _send(runner, user_id, session_id, message):
    content = types.Content(role="user", parts=[types.Part.from_text(text=message)])
    final_text = ""
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text:
                final_text = text
    return final_text


def _explain_known_issue_then_start_new_session():
    """Runs session 1 (explains the known payments-service error), then opens
    a fresh runner + session simulating a process restart. Returns
    (runner, user_id, session_id) ready for the actual test question.

    Fresh user_id per call. Memory Bank scopes memories per user_id, so this
    keeps calls isolated from whatever a previous test run already stored.
    """
    user_id = f"test-user-{uuid.uuid4().hex[:8]}"

    runner1 = _new_runner()
    session1 = asyncio.run(
        runner1.session_service.create_session(app_name=APP_NAME, user_id=user_id)
    )
    _send(
        runner1,
        user_id,
        session1.id,
        "The ConnectionResetError in payments-service around 03:14 UTC is "
        "expected, nightly maintenance restarting connections, not an incident.",
    )

    # New runner and new session, simulates a real process restart. Same
    # agent_engine_id is what makes memory persist across this boundary.
    runner2 = _new_runner()
    session2 = asyncio.run(
        runner2.session_service.create_session(app_name=APP_NAME, user_id=user_id)
    )
    return runner2, user_id, session2.id


def test_agent_recalls_a_previously_explained_known_issue_across_sessions():
    runner, user_id, session_id = _explain_known_issue_then_start_new_session()
    final_text = _send(
        runner, user_id, session_id, "Check payments-service logs, anything to worry about?"
    ).lower()

    acknowledged_known = any(
        word in final_text for word in ["known", "expected", "maintenance", "already"]
    )
    assert acknowledged_known, f"expected an acknowledgment of the known issue, got: {final_text}"


def test_agent_still_flags_a_genuinely_new_issue():
    runner, user_id, session_id = _explain_known_issue_then_start_new_session()
    final_text = _send(
        runner, user_id, session_id, "Check inventory-service logs, anything to worry about?"
    ).lower()

    assert "nullpointerexception" in final_text or "new" in final_text or "attention" in final_text
