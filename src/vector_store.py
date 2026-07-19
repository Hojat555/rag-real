import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.index: faiss.IndexFlatL2 | None = None
        self.metadata : list[dict] =[]
    
    def add_embeddings(self,embedded_chunks: list[dict])-> None:
        if not embedded_chunks:
            raise ValueError("No embedded chunk were provided..")
        
        embeddings = [
            chunk["embedding"]
            for chunk in embedded_chunks  
        ]
        
        new_metadata = [
            {
                "text": chunk["text"],
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
                
            }
            for chunk in embedded_chunks
        ]
        
        embeddings_array = np.array(
            embeddings,
            dtype = np.float32
        )
     
        
        if embeddings_array.ndim == 1:
            embeddings_array = np.expand_dims(embeddings_array, axis=0)
            
        if embeddings_array.ndim != 2:
            raise ValueError("Embeddings must be a two-dimensional array.")
        
        incoming_dimension = embeddings_array.shape[1]
    
            
        if self.index is None:
           self.index = faiss.IndexFlatL2(incoming_dimension)
        
        
        elif incoming_dimension != self.index.d:
            raise ValueError(
                
              "Embedding dimension mismatch: "
                f"index expects {self.index.d}, "
                f"but received {incoming_dimension}."
            ) 

        self.index.add(embeddings_array)
        self.metadata.extend(new_metadata)
        
        if self.index.ntotal != len(self.metadata):
            raise RuntimeError(
                "FAISS index and metadata are out of sync: "
                f"{self.index.ntotal} vectors, "
                f"{len(self.metadata)} metadata records."
            )


        
    def search(self, query_embedding: list[float], top_k: int = 3, 
               max_distance :float = 0.4) -> list[dict]:
         
       if self.index is None:
           raise RuntimeError("Index is empty. Call add_embeddings first.")
       
       if top_k <= 0:
         raise ValueError(
         "top_k must be greater than zero"
        )
         
       query_array = np.array([query_embedding]).astype("float32")
       
       
       
       effective_k = min(top_k, self.index.ntotal)
       
       
       distances, indices = self.index.search(query_array, effective_k)
       
       
       
       if max_distance is not None and float(distances[0][0]) > max_distance:
           return []
       
    
       results = []

       for distance, index in zip(distances[0], indices[0]):
           
         if index < 0:
               continue
           
         item = self.metadata[index].copy()
         item["distance"] = float(distance)
         results.append(item)

       return results
    
    
        
        
          
    
    
    
    
        
        
        
        
        
        
        
        
   
       
    
    
    