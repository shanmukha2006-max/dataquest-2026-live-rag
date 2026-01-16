# Live News Dynamic RAG - Implementation Plan

## Goal Description
Build a real-time Retrieval-Augmented Generation (RAG) system using Pathway that updates its knowledge base instantly as new data arrives. The system will simulate a live news feed and serve answers via a FastAPI interface.

## User Review Required
- **Pathway Integration**: We will use Pathway's file system connector to simulate streaming by watching a CSV/JSONL file. This is robust for demos.
- **Embeddings**: Using `sentence-transformers/all-MiniLM-L6-v2` for speed and efficiency.

## Proposed Changes

### Configuration
#### [NEW] [config.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/app/utils/config.py)
- Settings for embedding model, data paths, and API host/port.

### Data Ingestion & Pipeline
#### [NEW] [live_news.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/app/connectors/live_news.py)
- Defines the schema for news articles.
- Helper function to simulate adding data to the source file.

#### [NEW] [stream_pipeline.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/app/pipeline/stream_pipeline.py)
- Configures the Pathway table.
- Reads from the source using `pw.io.fs.read`.
- Computes embeddings using the RAG module.
- Indexes the data into a KNN index.

### RAG Engine
#### [NEW] [embeddings.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/app/rag/embeddings.py)
- Wrapper around `sentence_transformers`.
- Pathway UDF (User Defined Function) for embedding generation.

#### [NEW] [rag_engine.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/app/rag/rag_engine.py)
- Query processing logic.
- Finds nearest neighbors from the Pathway index.
- (Optional) Simple LLM generation or just context retrieval to prove RAG works. *User asked for RAG, so we will include a simple prompt construction or mocked LLM response if no key is provided, or use a local LLM if possible, but for a 3-min demo, context retrieval + simple answer generation is key.*

### API & Main
#### [NEW] [query_api.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/app/api/query_api.py)
- FastAPI app exposing `/query` endpoint.
- Connects to the Pathway query server.
- [UPDATE] Add `/recents` endpoint to fetch streaming news for the dashboard.
- [UPDATE] Mount `/` to serve the static `UI/` folder.

### Web Interface (UI)
#### [NEW] [index.html](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/UI/index.html)
- Main dashboard structure.
- Sections: "Live Neural Stream" and "Intelligence Query".

#### [NEW] [style.css](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/UI/style.css)
- Dark, futuristic, "Neon/Glassmorphism" aesthetic.

#### [NEW] [app.js](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/UI/app.js)
- Polls `/recents` every 2s to update the feed.
- Handles search form submission.

### Main
#### [NEW] [main.py](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/main.py)
- CLI entry point to start the Pathway backend and the FastAPI frontend.
- Includes a "demo mode" to simulate data updates.

### Documentation
#### [NEW] [README.md](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/README.md)
#### [NEW] [architecture.md](file:///C:/Users/shanm/.gemini/antigravity/playground/volatile-crab/DataQuest_2026_Live_RAG/docs/architecture.md)

## Verification Plan
### Automated Tests
- `pytest tests/test_pipeline.py`

### Manual Verification
1. Start the system.
2. Query "What is the latest on X?" -> "No info".
3. Add news about X to the source file.
4. Query again -> System returns the new info immediately.
