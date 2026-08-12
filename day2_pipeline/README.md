# Day 2 — SequentialAgent (fixed pipeline)

**Concept:** `SequentialAgent` runs a list of sub-agents in a strict, unchanging
order. Data moves between them via `output_key` (where an agent's answer gets
stored) and `{that_key}` template references inside a downstream agent's
`instruction` string. No agent is "deciding" anything about control flow — the
list order is the whole program.

**Do this:**
1. `cp .env.example .env`, add your key
2. Fill in the 3 TODOs in `agent.py`
3. From the repo root: `pytest day2_pipeline` (free structural checks)
4. `adk web --port 8000` from repo root, pick `day2_pipeline`, ask it to
   "write a function that reverses a linked list"
   — watch the trace/state panel in the web UI to see `generated_code` and
   `review_comments` actually populate between stages.
5. Optional, costs tokens: `pytest -m integration day2_pipeline` runs
   `test_agent.py`, which checks the three stages actually ran in order —
   the automated version of step 4's manual trace-panel check.

**Stretch goal:** ADK also has `ParallelAgent` (runs sub-agents concurrently,
useful when stages don't depend on each other) and `LoopAgent` (repeats until a
condition or max-iterations). Skim their docs pages on adk.dev and sketch — in
the README, not code — how you'd restructure this pipeline if the reviewer
should be allowed to send the code back to the writer for another pass instead
of always moving forward once. (This is a real limitation of a pure
SequentialAgent — LoopAgent is usually how people solve it.)

**Where this sits vs. what you built before:** if a task in that system ever
moved through a fixed set of roles in the same order every time (e.g., draft ->
fact-check -> edit), this is ADK's named, first-class version of that — instead
of it being an emergent property of how you wrote the prompts/handoffs.
