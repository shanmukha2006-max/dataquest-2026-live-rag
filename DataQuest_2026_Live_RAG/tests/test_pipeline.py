from app.rag.rag_engine import RAGEngine
import pytest
from unittest.mock import MagicMock, patch

def test_rag_engine_init():
    engine = RAGEngine()
    assert "http://" in engine.url

@patch('requests.post')
def test_rag_engine_query(mock_post):
    # Mocking a successful response from Pathway
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = [{"result": "Test Article", "query": "Test"}]
    
    engine = RAGEngine()
    result = engine.query("test query")
    
    assert len(result) == 1
    assert result[0]["result"] == "Test Article"

def test_answer_generation():
    engine = RAGEngine()
    docs = [{"result": "Pathway creates live data pipelines."}]
    answer = engine.generate_answer("What is Pathway?", docs)
    
    assert "Pathway creates live data pipelines" in answer
    assert "dynamically retrieved" in answer
