# Day 7 — Governance + Capstone

**Governance, briefly (read, don't build):** Agent Registry, Skill Registry,
Agent Gateway, and IAM-based access controls are org-level concerns — who's
allowed to create/run/modify agents, how traffic is routed and secured, how
tool/skill access is scoped. There's no meaningful solo hands-on exercise for
these without an actual org to govern; the useful move today is reading enough
to recognize the vocabulary later (e.g., in a job description or an internal
GCP setup at a future employer), which is exactly the kind of thing your
NotebookLM notebook is good for — ask it to quiz you on these four concepts
until you can define each in one sentence without looking.

**Capstone build:** rebuild a thin, real slice of your earlier agent-company
in pure ADK — not a toy, an actual comparison.

1. Pick ONE real workflow from that earlier system (2-3 roles handing off
   work is plenty — don't rebuild the whole company).
2. Rebuild it using what you now have: `day2_pipeline`'s SequentialAgent style if
   the real workflow is fixed-order, or `day3_delegation`'s dynamic style if it
   genuinely branches on request type. Reuse those two folders as templates.
3. Write a short comparison doc in this folder covering, concretely:
   - What was more/less code in ADK vs. your original?
   - What did ADK make you specify explicitly that your earlier system left
     implicit (or vice versa)?
   - Where did ADK's routing (description-driven) feel more or less reliable
     than however your earlier system decided who handled what?
   - Given a week in: is this worth continuing past a week, and for what
     specific reason (a GCP-shop job requirement, wanting the managed
     RAG/Memory/eval tooling, something else)? Answer this one honestly — it's
     the actual output of the sprint, not the code.
