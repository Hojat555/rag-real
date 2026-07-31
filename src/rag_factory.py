from pathlib import Path

from src.chunker import chunk_documents
from src.embedder import EmbeddingGenerator
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine
from src.text_generator import TextGenerator
from src.document_loader import load_documents


def build_rag_engine(data_path:Path, index_folder:Path = Path("data/index"))->RAGEngine :
    
    embedder = EmbeddingGenerator()
    
    index_file = index_folder/ "vectors.faiss"
    metadata_file = index_folder/ "metadata.json"
    
    if index_file.exists() and metadata_file.exists():
        vectorstore = VectorStore.load(index_folder)
    
    else:
        documents = load_documents(data_path)
        chunks = chunk_documents(documents)
        
        embededd_chunks = embedder.embed_chunks(chunks)
        vectorstore = VectorStore()
        vectorstore.add_embeddings(embededd_chunks)
        vectorstore.save(index_folder)
        
    generator = TextGenerator()
        
    return RAGEngine(
        embedder=embedder,
        vector_store=vectorstore,
        generator=generator
        )
        
        
    