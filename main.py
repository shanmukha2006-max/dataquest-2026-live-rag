import multiprocessing
import time
import uvicorn
import sys
import os
from app.api.query_api import app as fastapi_app
from app.connectors.live_news import append_news_article
from app.utils.config import API_HOST, API_PORT

def run_pathway():
    """
    Runs the Pathway Pipeline.
    Checks if running on Windows (where Pathway might be a stub) and fails over to mock.
    """
    print(">>> Starting Pathway Streaming Engine...")
    
    try:
        import pathway as pw
        # Check if it's the real pathway
        if not hasattr(pw, 'run'):
             raise ImportError("Pathway stub detected")
             
        from app.pipeline.stream_pipeline import create_pipeline
        create_pipeline()
        pw.run()
        
    except (ImportError, AttributeError, Exception) as e:
        print(f"\n{'!'*50}")
        print(f"WARNING: API Mismatch or Windows Detected ({e}).")
        print("Falling back to WINDOWS COMPATIBILITY MODE (Mock Backend).")
        print("For the real Pathway experience, please run on Linux or WSL.")
        print(f"{'!'*50}\n")
        
        from app.pipeline.mock_backend import run_mock_server
        run_mock_server()

def run_fastapi():
    """
    Runs the FastAPI server.
    """
    print(f">>> Starting FastAPI Query Interface on {API_HOST}:{API_PORT}...")
    uvicorn.run(fastapi_app, host=API_HOST, port=API_PORT, log_level="info")

def simulate_news_stream():
    """
    Simulates a news stream by periodically adding articles.
    """
    print(">>> Starting Live News Simulator...")
    try:
        while True:
            # Simulate a new article every 30 seconds
            time.sleep(30)
            print("\n[LIVE STREAM] Incoming News Alert!")
            article = append_news_article()
            print(f"[LIVE STREAM] New Data Ingested: {article['text'][:50]}...")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    # Create processes
    p_pathway = multiprocessing.Process(target=run_pathway)
    p_api = multiprocessing.Process(target=run_fastapi)
    p_sim = multiprocessing.Process(target=simulate_news_stream)

    try:
        # Start Pathway (needs to come up first ideally, but simultaneous is fine)
        p_pathway.start()
        # Give Pathway a moment to initialize
        time.sleep(5)
        
        # Start API
        p_api.start()
        
        # Start Simulator (optional, user can trigger manually, but this makes it 'live')
        p_sim.start()

        print("\n" + "="*50)
        print(" SYSTEM IS LIVE")
        print(" 1. Pathway Streaming Engine: Active")
        print(" 2. RAG API: http://127.0.0.1:8000/docs")
        print(" 3. News Simulator: Auto-generating content")
        print("="*50 + "\n")
        
        # Keep main process alive
        p_pathway.join()
        p_api.join()
        p_sim.join()

    except KeyboardInterrupt:
        print("\nShutting down system...")
        p_pathway.terminate()
        p_api.terminate()
        p_sim.terminate()
        print("System shutdown complete.")
        sys.exit(0)
