import faiss
import numpy as np
import json
from pathlib import Path 
from typing import Any

class VectorStore:
    def __init__(self):
        self.index: Any | None = None
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
                "domain": chunk.get("domain"),
                "file_type": chunk.get("file_type"),
                "chunk_id": chunk["chunk_id"],  
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
               max_distance :float | None = 0.4) -> list[dict]:
         
       if self.index is None:
           raise RuntimeError("Index is empty. Call add_embeddings first.")
       
       if top_k <= 0:
         raise ValueError(
         "top_k must be greater than zero"
        )
         
       query_array = np.array([query_embedding]).astype("float32")
       
       effective_k = min(top_k, self.index.ntotal)
       
       distances, indices = self.index.search(query_array, effective_k)
       
       results = []

       for distance, index in zip(distances[0], indices[0]):
           
        if index < 0:
               continue
           
        if max_distance is not None and distance > max_distance:
            continue
           
        item = self.metadata[index].copy()
        item["distance"] = float(distance)
        results.append(item)

       return results
   
   
   
    def save(self, folder_path: Path) -> None:
        if self.index is None:
            raise RuntimeError("Index is empty")
        
        folder_path.mkdir(parents=True, exist_ok=True)
        
        index_path = folder_path / "vectors.faiss"
        metadata_path = folder_path / "metadata.json"
        
        faiss.write_index(self.index, str(index_path))
        
        with metadata_path.open("w", encoding ="utf-8")as file:
            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent = 2
            )
            
    @classmethod
    def load(cls, folder_path: Path) -> "VectorStore":
     index_path = folder_path / "vectors.faiss"
     metadata_path = folder_path / "metadata.json"

     if not index_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(
            "Saved vector store files were not found."
        )

     store = cls()
     
     loaded_index = faiss.read_index(str(index_path))
     
     store.index = loaded_index

     with metadata_path.open("r", encoding="utf-8") as file:
        store.metadata = json.load(file)

     if store.index.ntotal != len(store.metadata):
        raise ValueError(
            "Index and metadata size do not match."
        )

     return store
   
    

        
        
          
    
    
    
    
        
        
        
        
        
        
        
        
   
       
    
    
    