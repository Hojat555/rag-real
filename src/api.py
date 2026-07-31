from contextlib import asynccontextmanager

from fastapi  import FastAPI
from pydantic import BaseModel
from pathlib import Path

from src.rag_factory import build_rag_engine


class AskRequest(BaseModel):
    question : str
    include_sources : bool = False

@asynccontextmanager
async def life_span(app: FastAPI):
    app.state.rag =build_rag_engine(Path("data/raw"))
    
    yield
    app.state.rag = None
    
app = FastAPI(lifespan=life_span)

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post('/ask')
def ask(request :AskRequest):
    result = app.state.rag.answer(request.question, max_distance = 1.2)
    response = {
        "answer" : result["answer"]
    }
    if request.include_sources:
        response["sources"] = list(
            dict.fromkeys(
                item["source"]
                for item in result["sources"]
            )
        )
    return response