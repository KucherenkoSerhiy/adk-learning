"""ADK's eval framework (as opposed to test_agent.py's hand-rolled
tool-call assertions via testutils). Checks tool-call trajectory only
(see evals/test_config.json) -- exact wording of the final response isn't
asserted on, same reasoning as test_agent.py.

Requires the eval extra: pip install "google-adk[eval]"
"""
import asyncio
from pathlib import Path

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytestmark = pytest.mark.integration

EVALS_DIR = Path(__file__).parent / "evals"


def test_day1_agent_tool_trajectory():
    asyncio.run(
        AgentEvaluator.evaluate(
            agent_module="day1_single_agent.agent",
            eval_dataset_file_path_or_dir=str(EVALS_DIR),
            num_runs=1,
        )
    )
