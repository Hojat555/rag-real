from src.vector_store import VectorStore

def test_search_does_not_return_more_results_than_vectors():
    
    store = VectorStore()
    
    embedded_chunks = [
        {
            "text": "First document",
            "source": "first.txt",
            "chunk_id": "0",
            "embedding": [0.0, 0.0]
        },
        {
            "text": "Second document",
            "source": "second.txt",
            "chunk_id": "1",
            "embedding": [1.0, 1.0]
        }
    ]
    store.add_embeddings(embedded_chunks)
    
    results = store.search(
        query_embedding=[0.0, 0.0],
        top_k = 3
    )
    
    assert len(results) == 2
    
    chunk_ids = [result["chunk_id"] for result in results]
    assert len(chunk_ids) == len(set(chunk_ids))
    
    
def test_add_embeddings_adds_vectors_and_metadata():
    store = VectorStore()
    
    embedded_chunks = [
        {
            "text": "First document",
            "source": "first.txt",
            "chunk_id": "0",
            "embedding": [0.0, 0.0]
        },
        {
            "text": "Second document",
            "source": "second.txt",
            "chunk_id": "1",
            "embedding": [1.0, 1.0]
        }
    ]
    store.add_embeddings(embedded_chunks)
      
    assert store.index is not None
    assert store.index.ntotal == 2
    assert len(store.metadata )== 2
     
      
      
      
    
    
      
    