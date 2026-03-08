import json
from sentence_transformers import CrossEncoder
from retrieval import hybrid_search

print("Loading reranker model...")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, top_k=5):
    results = hybrid_search(query, top_k=10)
    
    pairs = [[query, r["text"]] for r in results]
    scores = reranker.predict(pairs)
    
    for i, result in enumerate(results):
        result["rerank_score"] = float(scores[i])
    
    reranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
    
    return reranked[:top_k]


query = "What are the latest treatments for diabetes?"
results = rerank(query)

print(f"\nQuery: {query}")
print(f"Top {len(results)} results after reranking:\n")
for i, r in enumerate(results):
    print(f"{i+1}. {r['title']}")
    print(f"   Score:   {r['rerank_score']:.4f}")
    print(f"   Journal: {r['journal']} ({r['year']})")
    print(f"   URL:     {r['url']}\n")