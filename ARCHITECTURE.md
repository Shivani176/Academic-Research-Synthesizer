# Architecture

This document explains how the Research Assistant is structured, how data flows end-to-end, and what each major module does.

---

## System goals

1. **Discover** papers from the internet
2. **Store** them locally for reuse
3. **Retrieve** relevant papers reliably for a query
4. **Synthesize** a literature review with citations
5. **Export** citations (BibTeX) for academic workflows

---

## High-level component map

```mermaid
flowchart TD
  UI[Streamlit UI\n(app_ui.py)] --> ROUTER[Query Router + Agent Executor\n(main.py)]
  ROUTER --> TOOLS[Tool Layer\n(tools.py + synthesis_tools.py)]
  TOOLS --> MEM[Hybrid Memory\n(memory_manager.py)]
  MEM --> SQLITE[(SQLite: papers.db)]
  MEM --> CHROMA[(ChromaDB: embeddings)]
  MEM --> BM25[BM25 Index]
  TOOLS --> EXT[External Sources\n(ArXiv / OpenAlex)]
  TOOLS --> SYN[Synthesis Engine\n(synthesis_engine.py)]
  TOOLS --> OUT[Output Manager\n(output_manager.py)]
  OUT --> FS[(Filesystem: exports/)]
```

---

## Modules and responsibilities

### 1) UI layer — `app_ui.py`
- Provides a chat-like interface and settings panel
- Collects user input and calls `execute_routed_query(...)`
- Displays progress messages (search vs synthesis vs export)

### 2) Orchestration — `main.py`
- Configures the LLM + LangChain agent
- Classifies queries into types (database, paper_search, synthesis, export, etc.)
- Executes the correct agent/tool chain
- Injects the `MemoryManager` into tools (dependency injection)

### 3) Tools layer — `tools.py`, `synthesis_tools.py`
- **External discovery tools**: ArXiv + OpenAlex search
- **Local library tools**: stored papers lookup, hybrid search, save/store
- **Analysis tools**: connection/semantic/bridge analysis (graph-ish features)
- **Synthesis tools**: `generate_literature_review`, `quick_summary`
- **Export tools**: BibTeX export from the stored library

### 4) Hybrid Memory — `memory_manager.py`
Single place that owns “memory”:
- **Structured store**: SQLite `papers.db` for paper metadata + logs
- **Vector store**: ChromaDB collections for paper/conversation/analysis embeddings
- **Hybrid retrieval**: BM25 keyword match + embedding similarity

### 5) Synthesis Engine — `synthesis_engine.py`
- Converts the retrieved papers into a **structured literature review**
- Enforces citation usage so statements map to stored paper content
- Produces a review text plus citation list/statistics

### 6) Output layer — `output_manager.py`, `bibtex_export.py`
- Standardizes output paths + timestamping
- Writes BibTeX exports and creates “latest” pointers for fast access

---

## Data flow: end-to-end

### A) “Find new papers about X”
1. UI sends query → router
2. Router classifies as `paper_search`
3. Tool layer calls ArXiv/OpenAlex
4. Results are presented, optionally stored to memory

### B) “What papers do I have about X?”
1. UI sends query → router
2. Router classifies as `database`
3. Tool layer queries SQLite + (optionally) hybrid search
4. Returns stored paper matches

### C) “Generate a literature review on X”
1. UI sends query → router
2. Router classifies as `synthesis`
3. Synthesis tool runs:
   - hybrid search for relevant papers
   - calls synthesis engine for review generation
4. Output is returned to UI (with citations)

### D) “Export BibTeX for X”
1. UI sends query → router
2. Router classifies as `export`
3. Export tool selects papers by title keywords / year filters
4. Writes `.bib` output and returns the path

---

## Storage model

### SQLite (`papers.db`)
- Paper metadata: title, authors, abstract, year, source, ids
- Logs: conversation history, analysis logs

### ChromaDB (persistent)
- `papers` collection (paper embeddings)
- `conversations` collection (chat history embeddings)
- `analyses` collection (semantic/bridge analysis artifacts)

---

## Design choices (why this approach)

- **Tool routing** keeps behavior deterministic and demo-friendly.
- **Hybrid retrieval** improves recall/precision vs. embeddings-only or keyword-only.
- **Separate synthesis tool** isolates “long-form writing” from normal Q&A.

---

## Extension ideas

- PDF ingestion pipeline + page-level citations
- Evaluation harness: nDCG@k / MAP@k for retrieval + citation faithfulness checks
- Dockerized deployment (Streamlit + persistent volumes)
- Tests: routing unit tests, memory regression tests, export snapshot tests
