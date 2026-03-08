import requests
import json
import time

def search_pubmed(query, max_results=100):
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(search_url, params=search_params)
    ids = response.json()["esearchresult"]["idlist"]
    print(f"Found {len(ids)} articles")

    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
        "rettype": "abstract"
    }
    fetch_response = requests.get(fetch_url, params=fetch_params)
    return fetch_response.text

def parse_articles(xml_text):
    from xml.etree import ElementTree as ET
    root = ET.fromstring(xml_text)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        try:
            title    = article.findtext(".//ArticleTitle", default="No title")
            abstract = article.findtext(".//AbstractText", default="No abstract")
            year     = article.findtext(".//PubDate/Year", default="Unknown")
            journal  = article.findtext(".//Journal/Title", default="Unknown")
            pmid     = article.findtext(".//PMID", default="")

            articles.append({
                "title": title,
                "abstract": abstract,
                "year": year,
                "journal": journal,
                "pmid": pmid,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })
        except:
            continue
    return articles

queries = [
    "diabetes treatment[Title/Abstract] AND (2024[pdat] OR 2025[pdat])",
    "hypertension management[Title/Abstract] AND (2024[pdat] OR 2025[pdat])",
    "cancer immunotherapy[Title/Abstract] AND (2024[pdat] OR 2025[pdat])",
    "mental health depression[Title/Abstract] AND (2024[pdat] OR 2025[pdat])",
    "COVID long term effects[Title/Abstract] AND (2024[pdat] OR 2025[pdat])"
]

all_articles = []
seen_pmids = set()

for i, query in enumerate(queries):
    print(f"\nQuery {i+1}/{len(queries)}: {query[:50]}...")
    
    xml_data = search_pubmed(query, max_results=100)
    articles = parse_articles(xml_data)
    
    for article in articles:
        if article["pmid"] not in seen_pmids:
            seen_pmids.add(article["pmid"])
            all_articles.append(article)
    
    print(f"Total so far: {len(all_articles)} articles")
    
    if i < len(queries) - 1:
        print("Waiting 3 seconds...")
        time.sleep(3)

with open("data/medical_articles.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print(f"\nDone! Saved {len(all_articles)} unique articles")