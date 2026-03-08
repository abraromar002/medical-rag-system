import json

with open("data/medical_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"Total articles: {len(articles)}")

cleaned = []
skipped = 0

for article in articles:
    if article["abstract"] == "No abstract" or article["title"] == "No title":
        skipped += 1
        continue
    if len(article["abstract"]) < 50:
        skipped += 1
        continue
    cleaned.append(article)

with open("data/cleaned_articles.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"Cleaned articles: {len(cleaned)}")
print(f"Skipped articles: {skipped}")
print(f"\nSample:")
print(f"Title:    {cleaned[0]['title']}")
print(f"Abstract: {cleaned[0]['abstract'][:200]}...")