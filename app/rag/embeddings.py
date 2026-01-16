import pathway as pw
from sentence_transformers import SentenceTransformer
import numpy as np
from app.utils.config import EMBEDDING_MODEL_NAME

# Initialize the model once
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

@pw.udf
def embed_text(text: str) -> np.ndarray:
    """
    Pathway User-Defined Function to generate embeddings for a given text.
    """
    if not text:
        # Return a zero vector or handle appropriately if empty
        return np.zeros(384) # 384 is the dimension for all-MiniLM-L6-v2
    return model.encode(text)
