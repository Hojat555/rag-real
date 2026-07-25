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
            "domain": "artificial_intelligence",
            "file_type": ".txt",
            "embedding": [0.0, 0.0]
        },
        {
            "text": "Second document",
            "source": "second.txt",
            "domain": "modern_medicine",
            "file_type": ".txt",
            "chunk_id": "1",
            "embedding": [1.0, 1.0]
        }
    ]
    store.add_embeddings(embedded_chunks)
      
    assert store.index is not None
    assert store.index.ntotal == 2
    assert len(store.metadata )== 2
    


def test_search_preserves_metadata():
    store = VectorStore()
     
    embedded_chunks = [
        {
            "text": "First document",
            "source": "ai.txt",
            "chunk_id": "0",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
            "embedding": [0.0, 0.0]
        },
        {
            "text": "Second document",
            "source": "second.txt",
            "chunk_id": "1",
            "domain": "modern_medicine",
            "file_type": ".txt",
            "embedding": [10.0, 10.0]
        }
    ]
    store.add_embeddings(embedded_chunks)
    
    result = store.search(
        query_embedding=[0.1, 0.1],
        top_k=1,
    )
    
    assert len(result) == 1
    assert result[0]["text"] == "First document"
    assert result[0]["source"] == "ai.txt"
    assert result[0]["domain"] == "artificial_intelligence"
    assert result[0]["file_type"] == ".txt"
    assert result[0]["chunk_id"] == "0"
    assert isinstance(result[0]["distance"], float)  
    
      
      
    
    
      
    