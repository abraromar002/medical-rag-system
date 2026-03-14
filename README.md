# Medical Research Assistant — PubMed RAG Pipeline

A **production-grade Retrieval-Augmented Generation (RAG) system** for searching and retrieving **peer-reviewed medical literature from PubMed**, using hybrid retrieval, cross-encoder reranking, and strict citation enforcement.

---

# Overview

This system allows users to ask **natural language questions about medical topics** and receive answers backed by **real, cited research papers from PubMed (2024–2025)**.

### Example Queries

* *What are the latest treatments for diabetes?*
* *What does recent research say about cancer immunotherapy?*
* *How is hypertension managed in elderly patients?*

---

# Interface

<img width="1905" height="866" alt="ميد22" src="https://github.com/user-attachments/assets/848662ee-e315-48aa-9f17-a571c0d2e5b4" />
-------

<img width="1035" height="872" alt="ميد1" src="https://github.com/user-attachments/assets/50881da1-2215-4a24-8df7-17f5ee9c73bc" />

---


# ⚙️ Pipeline Breakdown

## 1️⃣ Data Collection

* Fetches articles from the **PubMed API** (no scraping, fully compliant)
* Covers **5 medical domains**

  * Diabetes
  * Hypertension
  * Cancer
  * Depression
  * COVID-19
* ~**467 cleaned research articles** from **2024–2025**

---

## 2️⃣ Embeddings

Uses **BioBERT**:

```
pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb
```

A **biomedical domain-specific transformer model** trained on scientific and clinical text.

Embeddings are stored in **ChromaDB** for persistent vector search.

---

## 3️⃣ Hybrid Retrieval

Combines two search strategies:

* **BM25** → keyword-based search
* **Vector similarity search** → semantic understanding

Results from both methods are merged and duplicates removed.

---

## 4️⃣ Reranking

Uses a **Cross-Encoder model**:

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

This model evaluates **query + document pairs** and scores relevance to reorder results.

---

## 5️⃣ Citation Enforcement

Every returned result includes:

* Paper title
* Journal name
* Publication year
* PubMed URL
* Relevance score

⚠️ No answer is returned **without a verifiable source**.

---

#  Tech Stack

| Component      | Technology                            |
| -------------- | ------------------------------------- |
| Data Source    | PubMed API (NCBI Entrez)              |
| Embeddings     | BioBERT (sentence-transformers)       |
| Vector Store   | ChromaDB                              |
| Keyword Search | BM25 (rank-bm25)                      |
| Reranking      | Cross-Encoder (sentence-transformers) |
| Backend API    | FastAPI + Uvicorn                     |
| Frontend       | HTML / CSS / JavaScript               |

---

# 📁 Project Structure

```
medical-rag-system/

├── data/
│   ├── medical_articles.json
│   ├── cleaned_articles.json
│   └── chroma_db/

├── fetch_data.py
├── clean_data.py
├── vector_store.py
├── retrieval.py
├── reranker.py
├── citation.py

├── main.py
├── docs/index.html
└── requirements.txt
```

---

#  Setup & Run Locally

## 1️⃣ Clone the repository

```
git clone https://github.com/abraromar002/medical-rag-system.git
cd medical-rag-system
```

---

## 2️⃣ Create a virtual environment

**Windows**

```
python -m venv .venv
.venv\Scripts\activate
```

**Mac / Linux**

```
python -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Fetch and prepare the data

```
python fetch_data.py
python clean_data.py
python vector_store.py
```

---

## 5️⃣ Run the API

```
uvicorn main:app --reload
```

---

## 6️⃣ Open the frontend

Open:

```
docs/index.html
```

Or visit the interactive API:

```
http://127.0.0.1:8000/docs
```

---





