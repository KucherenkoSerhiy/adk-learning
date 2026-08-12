# Day 6 — Deploy + Evaluation

**Why this is a brief:** deployment targets (Agent Runtime vs. Cloud Run vs. GKE)
and the eval framework both assume a real GCP project + `gcloud` CLI setup that
I can't provision from here, and the exact commands are easy to get subtly wrong
from memory. Grounded lookup > guessing, same as Days 4-5.

**Concept to walk in with:** two separate concerns that are easy to conflate —
"does my agent run somewhere other than my laptop" (deploy) and "does my agent
still work correctly after I change it" (eval). ADK gives you a dedicated
evaluation framework specifically because "still works" is much fuzzier to test
for an LLM-driven agent than for normal code — the same input can validly
produce different-but-correct outputs.

**Build task:**
1. Pick the smallest of your three agents (probably `day1_single_agent`) and, via
   NotebookLM-grounded docs, deploy it to Cloud Run. Get a real URL you can hit.
2. Separately: ADK's eval framework runs an agent against a set of test cases and
   scores response quality/tool-call correctness, not just exact-string-match.
   Write 3-5 eval cases for `day1_single_agent` (e.g., "asks about Tokyo weather
   → should call get_forecast with city='Tokyo'") and run them.
3. Break something on purpose (e.g., rename a tool without updating the
   instruction) and confirm your eval cases actually catch it. An eval suite
   that doesn't fail when you break the thing it's testing isn't testing
   anything — this step is the actual point of the exercise.

**Where this sits vs. what you built before:** how did you know an agent in
that system was still working after a prompt/config change — manual
spot-checks, or something more systematic? If it was manual, that's the gap
ADK's eval tooling is aimed at.
