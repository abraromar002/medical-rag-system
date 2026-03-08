Medical Research Assistant — PubMed RAG Pipeline
A production-grade Retrieval-Augmented Generation (RAG) system for searching and retrieving peer-reviewed medical literature from PubMed, with hybrid retrieval, cross-encoder reranking, and citation enforcement.

Overview
This system allows users to ask natural language questions about medical topics and receive answers backed by real, cited research papers from PubMed (2024–2025).
Example queries:

"What are the latest treatments for diabetes?"
"What does recent research say about cancer immunotherapy?"
"How is hypertension managed in elderly patients?"

<img width="1905" height="866" alt="ميد22" src="https://github.com/user-attachments/assets/848662ee-e315-48aa-9f17-a571c0d2e5b4" />
<img width="1035" height="872" alt="ميد 1" src="https://github.com/user-attachments/assets/50881da1-2215-4a24-8df7-17f5ee9c73bc" />

Pipeline Breakdown
1. Data Collection

Fetches articles from the PubMed API (no scraping, fully legal)
Covers 5 medical domains: diabetes, hypertension, cancer, depression, COVID
~467 cleaned articles from 2024–2025

2. Embeddings

Uses BioBERT (pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb) — a domain-specific model trained on biomedical text
Stored in ChromaDB for persistent vector search

3. Hybrid Retrieval

Combines BM25 (keyword matching) and vector search (semantic similarity)
Merges results from both, removing duplicates

4. Reranking

Uses a Cross-Encoder (cross-encoder/ms-marco-MiniLM-L-6-v2) to score each result against the query
Returns the most relevant articles first

5. Citation Enforcement

Every result includes: title, journal, year, PubMed URL, and relevance score
No answer is returned without a traceable source


Tech Stack
ComponentTechnologyData SourcePubMed API (NCBI Entrez)EmbeddingsBioBERT (sentence-transformers)Vector StoreChromaDBKeyword SearchBM25 (rank-bm25)RerankingCross-Encoder (sentence-transformers)Backend APIFastAPI + UvicornFrontendHTML / CSS / JavaScript

Project Structure
medical-rag-system/
├── data/
│   ├── medical_articles.json      # Raw fetched articles
│   ├── cleaned_articles.json      # Filtered articles
│   └── chroma_db/                 # Vector database
├── fetch_data.py                  # PubMed data collection
├── clean_data.py                  # Data cleaning
├── vector_store.py                # BioBERT embeddings + ChromaDB
├── retrieval.py                   # Hybrid search (BM25 + vector)
├── reranker.py                    # Cross-encoder reranking
├── citation.py                    # Citation formatting
├── main.py                        # FastAPI backend
├── docs/index.html                # Frontend UI
└── requirements.txt

Setup & Run Locally
1. Clone the repo
bashgit clone https://github.com/abraromar002/medical-rag-system.git
cd medical-rag-system
2. Create virtual environment
bashpython -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
3. Install dependencies
bashpip install -r requirements.txt
4. Fetch and prepare data
bashpython fetch_data.py
python clean_data.py
python vector_store.py
5. Run the API
bashuvicorn main:app --reload
6. Open the frontend
Open docs/index.html in your browser, or visit http://127.0.0.1:8000/docs for the interactive API.

