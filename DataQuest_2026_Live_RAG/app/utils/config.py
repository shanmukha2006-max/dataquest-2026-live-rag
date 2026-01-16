import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Data sources
NEWS_SOURCE_FILE = DATA_DIR / "news_stream.jsonl"

# Pathway configuration
PATHWAY_HOST = "127.0.0.1"
PATHWAY_PORT = 8080

# API configuration
API_HOST = "127.0.0.1"
API_PORT = 8000

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
