import json
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb")

print("Loading articles...")
with open("data/cleaned_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="medical_articles")

print("Creating embeddings and storing...")
batch_size = 50

for i in range(0, len(articles), batch_size):
    batch = articles[i:i+batch_size]
    
    texts = [f"{a['title']}. {a['abstract']}" for a in batch]
    ids   = [a["pmid"] for a in batch]
    metas = [{"title": a["title"], "journal": a["journal"], 
               "year": a["year"], "url": a["url"]} for a in batch]
    
    embeddings = model.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings, 
                   ids=ids, metadatas=metas)
    
    print(f"Stored {min(i+batch_size, len(articles))}/{len(articles)} articles")

print(f"\nDone! Total in DB: {collection.count()}")