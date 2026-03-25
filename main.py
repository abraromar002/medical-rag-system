from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from citation import format_answer
import os

app = FastAPI(title="Medical RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="docs"), name="static")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
async def read_index():
    return FileResponse('docs/index.html')

@app.post("/search")
def search(request: QueryRequest):
    answer, results = format_answer(request.query, top_k=request.top_k)
    
    return {
        "query": request.query,
        "sources": [
            {
                "rank": i + 1,
                "title": r["title"],
                "journal": r["journal"],
                "year": r["year"],
                "url": r["url"],
                "score": round(r["rerank_score"], 4)
            }
            for i, r in enumerate(results)
        ]
    }
