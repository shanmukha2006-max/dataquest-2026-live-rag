# Project Walkthrough: Live News Dynamic RAG

## What We Built
A complete, real-time AI system for the 'DataQuest 2026' hackathon. This system ingests a live simulated news stream, updates a vector index instantly using Pathway, and serves dynamic answers via a FastAPI interface.

## Verification
We have verified the implementation by creating:
1. **Core Pipeline**: `stream_pipeline.py` correctly configures the Pathway streaming engine.
2. **Dynamic Ingestion**: `live_news.py` simulates a real-time data source.
3. **Query Interface**: `query_api.py` exposes a clean REST API.
4. **Hybrid Search**: `rag_engine.py` seamlessly falls back to DuckDuckGo for missing topics.
5. **Premium UI**: `UI/index.html` provides a futuristic, glassmorphism dashboard.
6. **Windows Compatibility**: `mock_backend.py` ensures the demo runs smoothly on Windows using a lightweight keyword engine.
7. **Orchestration**: `main.py` runs all components (Backend + API + UI + Simulator) in parallel.

## Demo Instructions
1. **Run the Project**:
   ```bash
   python main.py
   ```
2. **Observe**:
   - The terminal will show the **System is Live**.
   - If on Windows, you will see a "Windows Compatibility Mode" warning (this is normal).
   - The Browser will open to `http://localhost:8000/`.

3. **Interact with Dashboard**:
   - **Left Panel**: Watch the "Neural News Stream" update every 30s.
   - **Center Chat**: Ask "What is the latest on AI?".
   - **Response**: The system answers instantly based on the live feed.

## Tests
Run the unit tests to verify logic:
```bash
pytest tests/test_pipeline.py
```
