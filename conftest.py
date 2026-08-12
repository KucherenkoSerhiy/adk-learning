"""pytest session startup: load each day folder's .env into the process
environment before any test runs.

`adk run` / `adk web` do this automatically (it's built into the ADK CLI —
see google.adk.cli.utils.envs in the installed package). pytest has no
equivalent, so integration tests (tests/test_agent.py, real model calls via
testutils.py) would otherwise need GOOGLE_API_KEY exported manually every
session. This closes that gap the same way, just for the pytest path instead
of the CLI path.
"""
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).parent

for env_file in sorted(REPO_ROOT.glob("day*/.env")):
    # override=False: a value already in the environment (e.g. set manually
    # in your shell) always wins over whatever's in these files.
    load_dotenv(env_file, override=False)
