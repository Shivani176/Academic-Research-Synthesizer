# Research Assistant (Agentic RAG + Literature Review Synthesizer)

An **interactive research assistant** that helps you **discover, store, and synthesize** academic papers into **structured, citation-backed literature reviews** — with a clean **Streamlit UI**, **hybrid retrieval (BM25 + embeddings)**, and **BibTeX export**.

> Built as a graduate project (M.S. Computer Science). Designed to be **demo-friendly**: clear architecture, end-to-end workflow, and reproducible setup.

---

## ✨ What this project does

- **Search & discover papers** from external sources (ArXiv + OpenAlex).
- **Store papers locally** (structured metadata + vector embeddings).
- **Ask questions over your library** with hybrid retrieval.
- **Generate literature reviews** with **citation enforcement** (`[1] [2] ...`) using only stored paper content.
- **Export BibTeX** for a topic/keyword slice of your library.

---

## Demo (high-level workflow)

1. **Search new papers** (ArXiv/OpenAlex)  
2. **Store** selected papers into your local memory (SQLite + ChromaDB)  
3. Ask: “Generate a literature review on ___”  
4. Get a structured review with citations + optional BibTeX export

---

## Key features

### 1) Tool-routed agent (safe-ish by design)
User requests are **classified and routed** so the agent uses the right tool (paper search vs. local database vs. synthesis vs. export).  
This reduces “random tool usage” and keeps behaviors predictable.

### 2) Hybrid memory for retrieval
A central `MemoryManager` persists:
- **SQLite** for structured paper metadata + logs
- **ChromaDB** for embeddings (papers + conversations + analyses)
- **BM25** index for keyword retrieval (hybrid search)

### 3) Citation-backed synthesis
Literature reviews are generated through a dedicated synthesis tool that:
- pulls relevant papers via hybrid search
- produces a structured review (Intro / Findings / Methods / Gaps / Conclusion)
- enforces citations for each claim

### 4) Streamlit UI
A clean chat-style interface with:
- model selection (Claude variants)
- “show traces” toggle
- memory stats
- progress/status updates

---

## Tech stack

- **Python**, **LangChain**
- **Claude** via `langchain-anthropic`
- **ChromaDB** + **SentenceTransformers** embeddings
- **BM25** (`rank_bm25`) for keyword retrieval
- **SQLite** for structured storage
- **Streamlit** UI
- **NetworkX** for graph-style connection analysis

---

## Repository structure

```
.
├── app_ui.py                # Streamlit UI
├── main.py                  # Agent config + routing + execution
├── tools.py                 # LangChain tools (search, arxiv, openalex, db, export, analysis)
├── memory_manager.py        # Hybrid memory (SQLite + Chroma + BM25)
├── synthesis_tools.py       # Wrapper tool: generate_literature_review + quick_summary
├── synthesis_engine.py      # Review generation logic
├── bibtex_export.py         # BibTeX export utilities
├── output_manager.py        # Timestamped output management
├── requirements.txt
└── (scripts) migration_script.py, upgrade_embeddings.py, ...
```

---

## Setup

### 1) Create environment + install deps
```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

### 2) Configure environment variables
Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY="YOUR_KEY"
# Optional (only if you use the web search tool):
TAVILY_API_KEY="YOUR_KEY"
```

### 3) Run the Streamlit UI
```bash
streamlit run app_ui.py
```

---

## Usage examples (copy/paste into the UI)

### Discover papers (external)
- “Find new papers about retrieval augmented generation”
- “Search ArXiv for transformer interpretability”
- “Search OpenAlex for LLM evaluation benchmarks”

### Query your stored library
- “What papers do I have about BERT?”
- “Search my papers for attention mechanisms”

### Synthesize a literature review
- “Generate a literature review on prompt injection defenses”
- “Synthesize papers about RAG evaluation metrics and research gaps”

### Export BibTeX
- “Export BibTeX for papers about retrieval and reranking (2022+)”

---

## Outputs

Exports are written via an output manager that creates **timestamped output files** and “latest” pointers for convenience (easy to link in demos/screenshots).  
Typical outputs include BibTeX exports and analysis artifacts.

---

## Notes

If you’re reviewing this repo, the best entry points are:

1. **`app_ui.py`** — the product surface / demo UI  
2. **`main.py`** — agent configuration + query routing  
3. **`memory_manager.py`** — hybrid retrieval + persistence layer  
4. **`synthesis_tools.py` / `synthesis_engine.py`** — literature review generation

---

## Roadmap
- Add PDF ingestion + citation-to-PDF-page grounding
- Add evaluation harness for retrieval & citation faithfulness
- Add Dockerfile + one-command startup
- Add tests for routing + memory + export flows

---
