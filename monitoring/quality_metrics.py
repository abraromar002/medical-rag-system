import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langfuse import Langfuse
from tracing import trace_search

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

def evaluate_search(query: str, top_k: int = 3):
    answer, results = trace_search(query, top_k=top_k)

    trace = langfuse.trace(
        name="medical-rag-quality",
        input={"query": query}
    )

    # Score 1 - Top result reranker confidence
    top_score = results[0]["rerank_score"] if results else 0
    retrieval_quality = min(max(top_score, 0), 1)
    langfuse.score(
        trace_id=trace.id,
        name="retrieval-confidence",
        value=round(retrieval_quality, 4),
        comment=f"Top reranker score: {top_score:.4f}"
    )

    # Score 2 - Coverage
    coverage = len(results) / top_k
    langfuse.score(
        trace_id=trace.id,
        name="result-coverage",
        value=round(coverage, 4),
        comment=f"{len(results)} of {top_k} results returned"
    )

    # Score 3 - Answer completeness
    answer_length = len(answer)
    length_score = min(answer_length / 500, 1.0)
    langfuse.score(
        trace_id=trace.id,
        name="answer-completeness",
        value=round(length_score, 4),
        comment=f"Answer length: {answer_length} chars"
    )

    langfuse.flush()

    print(f"\nQuery: {query}")
    print(f"  retrieval-confidence : {retrieval_quality:.4f}")
    print(f"  result-coverage      : {coverage:.4f}")
    print(f"  answer-completeness  : {length_score:.4f}")

    return answer, results


if __name__ == "__main__":
    queries = [
        "What are the latest treatments for diabetes?",
        "How does immunotherapy work for cancer?",
        "What are the side effects of metformin?",
        "Latest research on Alzheimer's disease",
        "How to treat hypertension naturally?"
    ]
    for q in queries:
        evaluate_search(q)
