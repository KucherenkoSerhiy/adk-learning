# Day 5 — Memory Bank

**Why this is a brief:** Memory Bank is another hosted Vertex AI service (session
storage + a memory-extraction/retrieval layer across sessions). Same reasoning
as Day 4 — pull the exact wiring from grounded docs, not from me guessing.

**Concept to walk in with:** everything through Day 3 forgets everything the
moment the process restarts — session state (like `output_key` values) lives
only within one run. Memory Bank is specifically for the next level up: facts
that should persist *across* separate conversations/sessions with the same user
or agent (e.g., "this user prefers concise answers," "we already covered X last
time"). This is the same shape of problem as Claude's own memory-file system
you've been using this whole conversation, worth noting as a direct comparison.

**Build task:**
1. Ask your NotebookLM notebook for the current pattern: how a session's
   important facts get written to Memory Bank, and how a later session retrieves
   them before responding.
2. Extend `day3_delegation`'s scenario (or a fresh small agent) so it remembers
   one fact about you across two separate `adk run` invocations — e.g., ask it
   your preferred headline style in session 1, restart, and in session 2 ask it
   to write a headline without re-telling it your preference. Does it use the
   remembered fact unprompted?
3. Write down in this folder's notes: what did Memory Bank decide was "worth
   remembering" on its own vs. what did you have to explicitly tell it to store?
   That boundary is usually the interesting/frustrating part of any memory
   system, not the happy path.

**Where this sits vs. what you built before:** did your agent-company have anything like
this, or did every session start cold? If cold-start was fine for that use case,
that's worth naming explicitly — Memory Bank isn't free, and "do we actually
need cross-session memory" is a real design question, not a given.
