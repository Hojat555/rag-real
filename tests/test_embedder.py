from src.embedder import EmbeddingGenerator

def test_embed_query_returns_vector():
  embedder   = EmbeddingGenerator()
  
  result = embedder.embed_query("what is rag?")
  
  assert isinstance(result,list)
  assert len(result) == 384
  assert all(isinstance(value,float) for value in result)