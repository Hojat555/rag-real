from pathlib import Path

from src.chunker import chunk_documents
from src.embedder import EmbeddingGenerator
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine
from src.text_generator import TextGenerator
from src.document_loader import load_documents


def build_rag_engine(data_path:Path)->RAGEngine :
    documents = load_documents(data_path)
    print(len(documents))
    
    chunks = chunk_documents(documents)
    print(len(chunks))
    
    embedded = EmbeddingGenerator()
    embedded_chunk = embedded.embed_chunks(chunks)
    
    vector_store = VectorStore()
    print(len(embedded_chunk))
    vector_store.add_embeddings(embedded_chunk)
    
    generator = TextGenerator()
    
    rag = RAGEngine(
        embedder = embedded,
        vector_store = vector_store,
        generator = generator
    )
    
    return rag