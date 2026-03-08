from reranker import rerank

def format_answer(query, top_k=3):
    results = rerank(query, top_k=top_k)
    
    answer = f"Query: {query}\n"
    answer += "=" * 60 + "\n\n"
    answer += "Answer based on the following sources:\n\n"
    
    for i, r in enumerate(results):
        answer += f"[{i+1}] {r['title']}\n"
        answer += f"    Journal: {r['journal']} ({r['year']})\n"
        answer += f"    URL: {r['url']}\n"
        answer += f"    Relevance Score: {r['rerank_score']:.4f}\n\n"
    
    answer += "=" * 60 + "\n"
    answer += f"Sources: {len(results)} peer-reviewed articles from PubMed\n"
    answer += "All results are cited with their original source.\n"
    
    return answer, results


query = "What are the latest treatments for diabetes?"
answer, results = format_answer(query)
print(answer)