import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

def trace_search(query: str, top_k: int = 3):
    from retrieval import hybrid_search
    from reranker import rerank
    from citation import format_answer

    trace = langfuse.trace(
        name="medical-rag-search",
        input={"query": query, "top_k": top_k}
    )

    # Step 1 - Hybrid Search
    span_retrieval = trace.span(name="hybrid-search")
    start = time.time()
    results = hybrid_search(query, top_k=top_k * 2)
    retrieval_time = round(time.time() - start, 3)
    span_retrieval.end(
        output={"chunks_retrieved": len(results)},
        metadata={"latency_sec": retrieval_time}
    )

    # Step 2 - Reranking
    span_rerank = trace.span(name="reranking")
    start = time.time()
    reranked = rerank(query, top_k=top_k)
    rerank_time = round(time.time() - start, 3)
    span_rerank.end(
        output={"chunks_after_rerank": len(reranked)},
        metadata={"latency_sec": rerank_time}
    )

    # Step 3 - Format Answer
    span_format = trace.span(name="format-answer")
    answer, _ = format_answer(query, top_k=top_k)
    span_format.end(
        output={"answer_length": len(answer)}
    )

    trace.update(
        output={
            "sources_count": len(reranked),
            "retrieval_latency": retrieval_time,
            "rerank_latency": rerank_time
        }
    )

    langfuse.flush()
    return answer, reranked


if __name__ == "__main__":
    queries = [
        "What are the latest treatments for diabetes?",
        "How does immunotherapy work for cancer?",
        "What are the side effects of metformin?",
        "Latest research on Alzheimer's disease",
        "How to treat hypertension naturally?"
    ]
    for q in queries:
        print(f"\nTracing: {q}")
        answer, results = trace_search(q)
        print(f"Done — {len(results)} results")
