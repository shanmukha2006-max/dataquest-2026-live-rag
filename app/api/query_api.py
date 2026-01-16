from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag.rag_engine import RAGEngine
from app.utils.config import NEWS_SOURCE_FILE, BASE_DIR
from typing import List, Dict, Any
import json
import os

app = FastAPI(title="Live News RAG API", version="1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = RAGEngine()

# Serve Static UI
ui_path = os.path.join(BASE_DIR, "UI")
if os.path.exists(ui_path):
    app.mount("/ui", StaticFiles(directory=ui_path, html=True), name="ui")
    # Redirect root to /ui
    from fastapi.responses import RedirectResponse
    @app.get("/")
    async def root():
        return RedirectResponse("/ui/index.html")

class QueryRequest(BaseModel):
    query: str
    k: int = 3

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[Dict[str, Any]]

@app.get("/health")
def health_check():
    return {"status": "online", "system": "Live News Dynamic RAG"}

@app.get("/recents")
def get_recent_news():
    """
    Returns the last 10 news items from the source file.
    """
    if not os.path.exists(NEWS_SOURCE_FILE):
        return []
    
    data = []
    try:
        with open(NEWS_SOURCE_FILE, "r") as f:
            # Read all lines and take last 20
            lines = f.readlines()[-20:]
            for line in reversed(lines): # Newest first
                try:
                    data.append(json.loads(line))
                except:
                    continue
    except Exception as e:
        print(f"Error reading news file: {e}")
    return data

@app.post("/query", response_model=QueryResponse)
def query_knowledge_base(request: QueryRequest):
    """
    Endpoints to query the live RAG system.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    # Get relevant documents from Pathway
    results = rag_engine.query(request.query, request.k)
    
    if isinstance(results, dict) and "error" in results:
        # If real pathway fails/mock backend issue, try to fail gracefully?
        # Actually raise so UI sees error
        pass # Let it proceed or handle error
        
    # Generate a coherent answer
    answer = rag_engine.generate_answer(request.query, results if not isinstance(results, dict) else [])
    
    # Structure sources
    sources = []
    if isinstance(results, list):
         sources = [{"content": r.get("result", "N/A")} for r in results]
    
    return QueryResponse(
        query=request.query,
        answer=answer,
        sources=sources
    )

if __name__ == "__main__":
    import uvicorn
    # This is for standalone testing of the API
    uvicorn.run(app, host="0.0.0.0", port=8000)
