from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name : str = "all-MiniLM-L6-V2"):
        self.model = SentenceTransformer(model_name)
    
    
    def embed_query(self, question: str) -> list[float]:
        
       query_embedding = self.model.encode(question).tolist()
       return query_embedding
   
    def embed_chunks(self, chunks:list[dict]) -> list[dict]:
        embedded_chunks = []
        
        all_text = [chunk["text"] for chunk in chunks]
        all_embeddings = self.model.encode(all_text).tolist()
        
        if len(chunks) != len(all_embeddings):
            raise ValueError("The number of chunks and embeddings must match")
        
        
        for chunk , embedding in zip(chunks , all_embeddings):
        
         embedded_chunks.append({
            "text" : chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "embedding": embedding 
            })
    
        return embedded_chunks
    
    
            
            
        
        
     