"""
Day 2 — SequentialAgent: a fixed, scripted pipeline.

Three specialist agents run in a strict order every time: writer -> reviewer ->
refactorer. No agent decides "should I run" or "who's next" — that's the whole
point of contrast with Day 3, where a coordinator picks a specialist dynamically.

Mechanism to notice: agents pass data to each other via `output_key` + the
session state it lands in, referenced downstream as `{that_key}` inside another
agent's instruction string. There's no manual plumbing — ADK does the substitution.

TASK: fill in the TODOs so state actually flows writer -> reviewer -> refactorer.
"""

from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent

MODEL = "gemini-flash-latest"

code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model=MODEL,
    instruction="""
    You are a Python Code Generator.
    Based *only* on the user's request, write Python code that fulfills the requirement.
    Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```).
    Do not add any other text before or after the code block.
    """,
    description="Writes initial Python code based on a specification.",
    output_key="generated_code",  # this is done for you — TODO 1 below needs to match it
)

code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model=MODEL,
    instruction="""
    You are an expert Python Code Reviewer.
    Your task is to provide constructive feedback on the provided code.

    **Code to Review:**
    ```python
    {generated_code}
    ```

    **Review Criteria:**
    1. Correctness  2. Readability  3. Efficiency  4. Edge cases  5. Best practices

    Output *only* a concise bulleted list of feedback, or "No major issues found."
    """,
    description="Reviews code and provides feedback.",
    # TODO 1: give this agent an output_key of "review_comments" so the next
    # stage can reference {review_comments}. (Look at code_writer_agent above
    # for the syntax — it's one keyword argument.)
)

code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model=MODEL,
    instruction="""
    You are a Python Code Refactoring AI.
    Your goal is to improve the given code based on the review comments.

    **Original Code:**
    ```python
    {generated_code}
    ```

    **Review Comments:**
    # TODO 2: this instruction is missing the template reference to the
    # reviewer's output. Add `{review_comments}` on its own line here so this
    # agent actually sees the feedback instead of guessing.

    Apply the suggestions. If review comments say "No major issues found," return
    the original code unchanged. Output *only* the final code block.
    """,
    description="Refactors code based on review comments.",
    output_key="refactored_code",
)

# TODO 3: assemble the pipeline. sub_agents order matters — it's the execution
# order. Should be: writer, then reviewer, then refactorer.
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[],  # TODO 3: fill this in
    description="Executes a sequence of code writing, reviewing, and refactoring.",
)

root_agent = code_pipeline_agent
