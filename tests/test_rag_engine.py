from src.rag_engine import RAGEngine

class FakeEmbedder:
    def embed_query(self, question):
        return [0.1, 0.2]

    def embed_chunks(self, chunks):
        raise AssertionError("embed_chunks should not be used for the query")



class FakeVectorStore:
    index = None

    def search(self, query_embedding, top_k, max_distance=0.4):
        assert query_embedding == [0.1, 0.2]
        assert max_distance == 0.4
        

        return [
            {
                "text": "RAG retrieves relevant information.",
                "source": "rag.txt",
                "domain": "artificial_intelligence",
                "file_type": ".txt",
                "chunk_id": "0",
                "distance": 0.12,
            }
        ]


class FakeGenerator:
    def generate(self, prompt):
        return "RAG retrieves information before generating an answer."
    



def test_answer_uses_query_embedding_and_preserves_sources():
    rag = RAGEngine(
        embedder=FakeEmbedder(),
        vector_store=FakeVectorStore(),
        generator=FakeGenerator(),
    )

    result = rag.answer("What is RAG?", top_k=1, max_distance= 0.4)

    assert result["answer"] == (
        "RAG retrieves information before generating an answer."
    )

    assert result["sources"] == [
        {
            "source": "rag.txt",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
            "chunk_id": "0",
            "distance": 0.12,
        }
    ]
