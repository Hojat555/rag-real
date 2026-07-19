# RAG Real

A minimal but complete Retrieval-Augmented Generation pipeline.

## Structure

```
rag-real/
├── data/raw/          # raw text documents
├── src/
│   ├── document_loader.py   # reads .txt files
│   ├── chunker.py           # splits docs into overlapping chunks
│   ├── embedder.py          # sentence-transformers embeddings
│   ├── vector_store.py      # FAISS index
│   ├── rag_engine.py        # orchestrates the full pipeline
│   └── api.py               # FastAPI endpoints
├── notebooks/
│   └── test_rag.ipynb
├── requirements.txt
└── Dockerfile
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn src.api:app --reload
```

## Run with Docker

```bash
docker build -t rag-real .
docker run -p 8000:8000 rag-real
```

## API

- `POST /query` — `{"question": "...", "top_k": 3}`
- `GET  /health` — index status

## Current Status

✅ Document Loading
✅ Chunking
✅ Embedding
✅ Vector Search (FAISS)
✅ Retrieval Pipeline

## Next

⬜ Prompt Construction
⬜ LLM Integration
⬜ Final Answer Generation

این یک آزمایش برای شاخه توسعه است.

