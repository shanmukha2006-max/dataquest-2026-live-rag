### Hybrid RAG Strategy
1. **Attempt Local Retrieval**: Query the Pathway Mock Backend (or Real Backend) first.
2. **Confidence Check**: If 0 documents returned or score (if available) is low? (For simplicity: if 0 documents).
3. **Web Fallback**: Use `duckduckgo-search` to fetch real-time results from the web.
4. **Unified Response**: Present web results in the same format but labeled clearly.

#### Changes
- **requirements.txt**: Add `duckduckgo-search`.
- **rag_engine.py**:
    - Import `duckduckgo_search`.
    - Implement `web_search(query)`.
    - Logic: `results = local_results or web_search(query)`.
