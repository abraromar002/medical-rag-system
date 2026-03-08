from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from citation import format_answer

app = FastAPI(title="Medical RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
def root():
    return {"message": "Medical RAG API is running!"}

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