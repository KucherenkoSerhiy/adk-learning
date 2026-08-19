import os

import vertexai
from google.adk import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from day4_grounding.constants import PROJECT, LOCATION

MODEL = "gemini-flash-latest"

vertexai.init(project=PROJECT, location=LOCATION)

retrieval_tool = VertexAiRagRetrieval(
    name="retrieve_ant_docs",
    description="Retrieve ant trivia and facts from the knowledge base",
    rag_resources=[rag.RagResource(rag_corpus=os.environ.get("RAG_CORPUS"))],
    similarity_top_k=10,
    vector_distance_threshold=0.6
)

root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description="Answers questions about ants using a grounded base knowledge",
    instruction=(
        "You are an ant trivia assistant. Use the 'retrieve_ant_docs' tool to "
        "find relevant information before answering questions about ants. "
        "If the retrieved documents don't contain the answer, say you don't know "
        "rather than guessing."
    ),
    tools=[retrieval_tool]
)
