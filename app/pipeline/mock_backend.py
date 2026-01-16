import uvicorn
from fastapi import FastAPI, Request
import json
import os
import time
import threading
import re
from app.utils.config import NEWS_SOURCE_FILE, PATHWAY_HOST, PATHWAY_PORT

# Lightweight In-Memory Store
DOC_STORE = []

app = FastAPI()

def tokenize(text):
    return set(re.findall(r'\w+', text.lower()))

def load_data():
    """
    Continually watches the file for new lines.
    Lightweight: No ML models, just text loading.
    """
    last_pos = 0
    print("[LightweightBackend] Watching for data stream...")
    
    while True:
        try:
            if os.path.exists(NEWS_SOURCE_FILE):
                with open(NEWS_SOURCE_FILE, "r") as f:
                    f.seek(last_pos)
                    lines = f.readlines()
                    last_pos = f.tell()
                    
                    if lines:
                        count = 0
                        for line in lines:
                            try:
                                data = json.loads(line)
                                DOC_STORE.append(data)
                                count += 1
                            except:
                                continue
                        
                        if count > 0:
                            print(f"[LightweightBackend] Ingested {count} new particles.")
        except Exception as e:
            print(f"[Error] {e}")
            
        time.sleep(0.5)

@app.post("/")
async def query_index(request: Request):
    """
    Keyword-based retrieval. Fast and strict.
    """
    data = await request.json()
    query_text = data.get("query", "")
    k = data.get("k", 3)
    
    if not query_text or not DOC_STORE:
        return []

    # Simple Keyword Scoring
    query_tokens = tokenize(query_text)
    
    scored_docs = []
    for doc in DOC_STORE:
        doc_tokens = tokenize(doc['text'])
        # Score = number of overlapping words
        score = len(query_tokens.intersection(doc_tokens))
        if score > 0:
            scored_docs.append((score, doc))
            
    # Sort by score descending
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # Take top K
    top_docs = [doc for score, doc in scored_docs[:k]]
    
    # Format for RAG
    results = []
    for doc in top_docs:
        results.append({
            "query": query_text,
            "result": doc['text']
        })
        
    return results

def run_mock_server():
    print(">>> ACTIVE: Lightweight Search Engine (Windows Optimized)")
    # Start data loader
    t = threading.Thread(target=load_data, daemon=True)
    t.start()
    
    # Run server
    uvicorn.run(app, host=PATHWAY_HOST, port=PATHWAY_PORT, log_level="error")

if __name__ == "__main__":
    run_mock_server()
