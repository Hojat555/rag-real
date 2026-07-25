import numpy as np

class RAGEngine:
    def __init__(self, embedder, vector_store, generator):
        self.embedder = embedder
        self.vector_store = vector_store
        self.generator = generator
        
    
    def build_prompt(self, question: str, context: str) -> str:
        prompt = f"""
        Use the following context to answer the question.
        
       Context:
       {context}

       Question:
       {question}

       Answer:
       """
        return prompt

    def answer(self, question: str, top_k: int = 3, max_distance: float | None = None) -> dict:
        
        query_embedding = self.embedder.embed_query(question)
    
        retrieved_chunks = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )
        
        if not retrieved_chunks:
            
            return{
            "question": question,
            "context": "",
            "prompt": "",
            "sources": [],
            "retrieved_chunks": [],
            "answer": "I don't have information about this in my documents."
            }
            
        context = "\n\n".join(
            chunk["text"] for chunk in retrieved_chunks
        )

        sources = [
           
           {
            "source": chunk["source"],
            "domain": chunk.get("domain"),
            "file_type": chunk.get("file_type"),
            "chunk_id": chunk["chunk_id"],
            "distance": chunk["distance"],
           }

            for chunk in retrieved_chunks
        ]
        
        prompt = self.build_prompt(question, context)
        answer = self.generator.generate(prompt)

        return {
            "question": question,
            "context": context,
            "prompt": prompt,
            "sources": sources,
            "retrieved_chunks": retrieved_chunks,
            "answer": answer 
        }