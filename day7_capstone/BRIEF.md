# Day 7 — Governance + Capstone

**Governance (read, don't build):** Agent Registry, Skill Registry, Agent
Gateway, and IAM-based access controls are org-level concerns: who can
create/run/modify agents, how traffic is routed and secured, how tool/skill
access is scoped. There's no meaningful solo exercise for these without an
actual org to govern. Read enough to define each of the four concepts in one
sentence without looking.

**Capstone build:** design and build a real multi-role workflow in pure ADK.
Not a toy example.

1. Pick a workflow with 2-3 distinct roles handing off work, something you'd
   actually want, not a contrived example.
2. Decide whether it's fixed-order or genuinely branches on request type. Use
   `day2_pipeline`'s `SequentialAgent` pattern for the former, `day3_delegation`'s
   dynamic-delegation pattern for the latter. Reuse those folders as templates.
3. Write a short doc in this folder covering:
   - Why you picked `SequentialAgent` vs. dynamic delegation for this specific
     workflow.
   - Where ADK's description-driven routing felt reliable, and where it didn't.
   - Given a week in: worth continuing past a week, and for what specific
     reason? Answer honestly. That's the actual output of the sprint.
