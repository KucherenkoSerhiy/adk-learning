import vertexai
from vertexai.preview import rag

from day4_grounding.constants import PROJECT, LOCATION

vertexai.init(project=PROJECT, location=LOCATION)

rag.update_rag_engine_config(  # switch RAG engine to serverless mode
    rag_engine_config=rag.RagEngineConfig(
        name="projects/skucherenko-226dd/locations/us-central1/ragEngineConfig",
        rag_managed_db_config=rag.RagManagedDbConfig(mode=rag.Serverless()),
    )
)

embedding_model_config = rag.EmbeddingModelConfig(
    publisher_model="publishers/google/models/text-embedding-005"
)

corpus = rag.create_corpus(
    display_name="ant-trivia-corpus",
    embedding_model_config=embedding_model_config
)

print("Corpus name:", corpus.name)

rag.import_files(
    corpus_name=corpus.name,
    paths=["gs://skucherenko-226dd-adk-corpus/ant-docs/"],
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
    )
)

with open("day4_grounding/.env", "a") as f:
    f.write(f"\nRAG_CORPUS={corpus.name}\n")
