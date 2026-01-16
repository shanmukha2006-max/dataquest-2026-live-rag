# Live News Dynamic RAG 🚀
### DataQuest 2026 Hackathon Submission

**Project Title**: Live News Dynamic RAG – Real-Time AI Intelligence System
**Theme**: Dynamic RAG / Live AI using Pathway

## Overview
Traditional RAG systems are static; they know only what was indexed yesterday. **Live News Dynamic RAG** changes this. By leveraging **Pathway**, we built a system that "reads" the news as it happens. When a breaking story drops, our AI knows about it *instantly* — no re-training, no re-indexing batch jobs.

## Key Features
- **Real-Time Ingestion**: Data is processed the millisecond it hits the stream.
- **Live Vector Indexing**: Embeddings are updated incrementally.
- **Dynamic Retrieval**: Answers change as facts change.
- **Modular Design**: Separation of concerns between Ingestion, Logic, and API.

## Architecture
Built on Python 3.10 and powered by:
- **Pathway**: The core streaming engine.
- **Sentence-Transformers**: For high-quality, efficient embeddings.
- **FastAPI**: For a clean, production-ready query interface.

See [Architecture Docs](docs/architecture.md) for details.

## Project Structure
```
DataQuest_2026_Live_RAG/
│── main.py                 # 🚀 One-click entry point
│── requirements.txt        # Dependencies
│── app/
│   ├── connectors/         # Data simulation & sources
│   ├── pipeline/           # Pathway streaming logic
│   ├── rag/                # Embeddings & RAG logic
│   └── api/                # FastAPI Endpoints
```

## How to Run
### Prerequisites
- Python 3.10+
- [Optional] Virtual Environment
- **Note for Windows Users**: The project includes a compatibility mode that automatically activates if the Full Pathway Engine is not detected (common on Windows). It uses a mock in-memory vector store to ensure the demo still works perfectly.

### Setup
1. Clone the repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Demo
We have provided a single orchestration script for the hackathon demo:
```bash
python main.py
```
This command will:
1. Start the **Pathway Streaming Backend**.
2. Launch the **FastAPI Server** (http://localhost:8000).
3. Start the **Live News Simulator** (generates news every 30s).

### Demo Flow
1. **Initial Query**:
   - Go to `http://localhost:8000/docs`.
   - POST to `/query`: `{"query": "What is happening in the AI market?"}`.
   - *Result*: Likely empty or generic if no data generated yet.

2. **Wait for Live Data**:
   - Watch the terminal. You will see `[LIVE STREAM] New Data Ingested`.
   - Wait for a topic like "AI" to appear.

3. **Dynamic Update**:
   - Run the **same query** again.
   - *Result*: The system now answers with the specific breaking news that just arrived! (e.g., "AI market sees a surge...").

## Future Improvements
- Connect to Twitter/X API for real real-world data.
- Integrate a generative LLM (GPT-4 or Llama 3) to synthesize full paragraphs from the retrieved context. (Current implementation focuses on the *retrieval* accuracy and speed).

---
*Built with ❤️ for DataQuest 2026*
