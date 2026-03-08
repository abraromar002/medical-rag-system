import json
import chromadb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

print("Loading model and database...")
model = SentenceTransformer("pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb")

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="medical_articles")

with open("data/cleaned_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

corpus = [f"{a['title']}. {a['abstract']}" for a in articles]
tokenized_corpus = [doc.lower().split() for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

def hybrid_search(query, top_k=5):
    query_embedding = model.encode(query).tolist()
    vector_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_top = sorted(range(len(bm25_scores)),
                      key=lambda i: bm25_scores[i], reverse=True)[:top_k]

    seen = set()
    results = []

    for i, doc in enumerate(vector_results["documents"][0]):
        meta = vector_results["metadatas"][0][i]
        if meta["title"] not in seen:
            seen.add(meta["title"])
            results.append({
                "title": meta["title"],
                "journal": meta["journal"],
                "year": meta["year"],
                "url": meta["url"],
                "text": doc,
                "source": "vector"
            })

    for idx in bm25_top:
        title = articles[idx]["title"]
        if title not in seen:
            seen.add(title)
            results.append({
                "title": title,
                "journal": articles[idx]["journal"],
                "year": articles[idx]["year"],
                "url": articles[idx]["url"],
                "text": corpus[idx],
                "source": "bm25"
            })

    return results


query = "What are the latest treatments for diabetes?"
results = hybrid_search(query)

print(f"\nQuery: {query}")
print(f"Found: {len(results)} results\n")
for i, r in enumerate(results):
    print(f"{i+1}. [{r['source']}] {r['title']}")
    print(f"   Journal: {r['journal']} ({r['year']})")
    print(f"   URL: {r['url']}\n")