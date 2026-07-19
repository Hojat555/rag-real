from src.vector_store import VectorStore

embedded_chunks = [
    {
        "text": "What is RAG?",
        "source": "test.txt",
        "chunk_id": "0",
        "embedding": [0.0, 0.0]
    }
]

vector_store = VectorStore()
vector_store.add_embeddings(embedded_chunks)

print(len(vector_store.metadata))

if vector_store.index is not None:
   print(vector_store.index.ntotal)