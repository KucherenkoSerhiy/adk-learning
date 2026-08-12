# ADK Learning Sprint (1 week)

Hands-on path through Google's Agent Development Kit (ADK), built for someone who's
already shipped a multi-agent "company of agents with roles" system with a mentor.
The goal isn't to relearn multi-agent concepts — it's to see Google's
specific, standardized/enterprise take on them, and decide how far it's worth going.

Every exercise code sample in `day1_*`–`day3_*` was pulled from the current official
ADK docs (adk.dev) on 2026-08-10 and cross-checked against a second independent source,
not invented — but ADK is a fast-moving framework, so if `adk run` errors on an import
or class name, that's the framework having moved since, not you doing it wrong. Check
`adk.dev/agents` for the current API before troubleshooting your own logic.

`day4`–`day7` are scoped as guided research+build briefs rather than pre-written code:
they touch GCP-hosted services (RAG Engine, Memory Bank, Agent Runtime, IAM) that need
your own GCP project and where docs details would be more likely to drift/hallucinate
if I hand-wrote exact API calls. Use those days to pull the real docs into a NotebookLM
notebook (see bottom) and build from grounded answers instead of my guesses.

## Setup (do this before Day 1)

```bash
python -m venv .venv
source .venv/Scripts/activate   # git-bash on Windows; use .venv\Scripts\Activate.ps1 in PowerShell
pip install -r requirements.txt
```

Get a Gemini API key at https://aistudio.google.com/apikey, then in each day's folder:

```bash
cp .env.example .env   # then paste your key into GOOGLE_API_KEY
```

Run a day's agent interactively (from the repo root):

```bash
adk web --port 8000
```

This serves every day-folder as a selectable agent in a chat UI at `localhost:8000`.
Prefer terminal-only? `adk run day1_single_agent` targets one agent directly.

Each day folder holds its own `tests/` subfolder, self-contained — no separate
top-level test tree to jump between:

```
day1_single_agent/
    agent.py, city.py, prompt.py
    tests/
        test_tools.py    # pure Python, no API calls, no cost
        test_wiring.py   # pure Python, no API calls, no cost
        test_agent.py    # real model call — costs tokens, needs GOOGLE_API_KEY
```

`test_tools.py` / `test_wiring.py` are free sanity checks — run those before
burning a real model call. `test_agent.py` goes through the shared
`testutils.py` Runner wrapper at the repo root and is excluded by default.

```bash
pytest                        # every day's free tests
pytest day1_single_agent      # just one day's free tests
pytest -m integration         # the real-model-call tests too (all days)
```

## The week

| Day | Folder | ADK concept | Your prior-project parallel |
|---|---|---|---|
| 1 | `day1_single_agent` | `Agent` + a tool function | One agent with one job — the atomic unit you already know |
| 2 | `day2_pipeline` | `SequentialAgent`, `output_key` state-passing | A fixed hand-off pipeline between roles, no improvising |
| 3 | `day3_delegation` | `sub_agents=[...]` dynamic routing | Closest to what you actually built — a coordinator picking a specialist by intent, not a script |
| 4 | `day4_grounding` | RAG Engine (retrieval over your own docs) | Giving an agent a shared knowledge base instead of just prompt context |
| 5 | `day5_memory` | Memory Bank (persistent memory across sessions) | State that survives past one run — did your agents remember anything long-term? |
| 6 | `day6_deploy_eval` | Deploy to Cloud Run / Agent Runtime + evaluation | Going from "runs on my machine" to something with SLAs and regression tests |
| 7 | `day7_capstone` | Governance (IAM/Registry) + capstone rebuild | Rebuild a thin slice of your earlier agent-company in pure ADK, compare notes |

## NotebookLM companion

The plan was to seed a NotebookLM notebook with the ADK docs so you have grounded
Q&A/quizzes while working through `day4`–`day7`. The automated Google-login handshake
from this session didn't complete (browser popup closed/cancelled before you could
sign in — likely not supported headless in this environment). Manual path instead:

1. Go to https://notebooklm.google.com, sign in, create a notebook.
2. Add these as sources: `https://adk.dev`, `https://google.github.io/adk-docs`,
   and the specific page for whatever day you're on (RAG Engine, Memory Bank docs, etc).
3. Optional: generate the Studio outputs you actually want there directly — Audio
   Overview, Quiz, Mind Map are all in the NotebookLM UI itself.
4. If you want, paste the notebook's share link back to me later and I'll retry
   the automated hook-up (add sources / pull grounded answers) from this session.
