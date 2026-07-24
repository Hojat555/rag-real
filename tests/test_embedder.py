from src.embedder import EmbeddingGenerator

def test_embed_query_returns_vector():
  embedder   = EmbeddingGenerator()
  
  result = embedder.embed_query("what is rag?")
  
  assert isinstance(result,list)
  assert len(result) == 384
  assert all(isinstance(value,float) for value in result)


def test_embed_chunks_preserves_metadata():
    embedder = EmbeddingGenerator()

    chunks = [
        {
            "text": "Retrieval augmented generation",
            "source": "rag.txt",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
            "chunk_id": "0"
        }
    ]

    result = embedder.embed_chunks(chunks)

    assert len(result) == 1
    assert result[0]["text"] == "Retrieval augmented generation"
    assert result[0]["source"] == "rag.txt"
    assert result[0]["domain"] == "artificial_intelligence"
    assert result[0]["file_type"] == ".txt"
    assert result[0]["chunk_id"] == "0"
    assert isinstance(result[0]["embedding"], list)
    assert len(result[0]["embedding"]) == 384