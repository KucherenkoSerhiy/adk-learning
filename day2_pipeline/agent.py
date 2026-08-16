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
    output_key="generated_code",
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
    output_key="review_comments"
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
    {review_comments}
    
    Apply the suggestions. If review comments say "No major issues found," return
    the original code unchanged. Output *only* the final code block.
    """,
    description="Refactors code based on review comments.",
    output_key="refactored_code",
)

code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
)

root_agent = code_pipeline_agent
