import requests
import json
from app.utils.config import PATHWAY_HOST, PATHWAY_PORT
try:
    from duckduckgo_search import DDGS
    HAS_DDG = True
except ImportError:
    HAS_DDG = False

class RAGEngine:
    def __init__(self):
        self.url = f"http://{PATHWAY_HOST}:{PATHWAY_PORT}"

    def query(self, text: str, k: int = 3):
        """
        Sends a query to the Pathway pipeline.
        If no results, falls back to Web Search.
        """
        payload = {"query": text, "k": k}
        local_results = []
        
        # 1. Try Local Pathway/Mock Index
        try:
            response = requests.post(self.url, json=payload, timeout=2)
            if response.status_code == 200:
                local_results = response.json()
        except Exception as e:
            print(f"Local RAG Error: {e}")

        if local_results:
            return local_results
            
        # 2. Fallback to Web Search
        if HAS_DDG:
            # print(f"Local index miss for '{text}'. Searching web...") # Debug logs
            try:
                # Use a fresh instance correctly or handle context manager
                # Using context manager is safesty for DDGS
                with DDGS() as ddgs:
                    results = list(ddgs.text(text, max_results=k))
                    
                web_docs = []
                if results:
                    for res in results:
                        web_docs.append({
                            "query": text,
                            "result": f"[WEB: {res.get('title', '')}] {res.get('body', '')}",
                            "source": "Internet"
                        })
                    return web_docs
            except Exception as e:
                # Print error but return empty list so next query works
                print(f"Web Search Error (non-fatal): {e}")
                return []
        
        return []

    def generate_answer(self, query: str, retrieved_docs: list):
        """
        Simulates an LLM generation step based on retrieved context.
        """
        if not retrieved_docs:
            return "Searching knowledge base... No relevant data found locally or online."
        
        # Check source type for intro
        is_web = any("WEB:" in doc.get('result', '') for doc in retrieved_docs)
        source_label = "LIVE WEB RESULTS" if is_web else "LOCAL NEURAL STREAM"
        
        intro = f"**[{source_label}]** Found relevant updates for '{query}':"
        points = []
        for i, doc in enumerate(retrieved_docs, 1):
            text = doc.get('result', 'N/A')
            points.append(f"{i}. {text}")
            
        return f"{intro}\n\n" + "\n".join(points)
