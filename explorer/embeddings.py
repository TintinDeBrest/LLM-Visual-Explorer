# embeddings
# PhL 28jul26

from sentence_transformers import SentenceTransformer
from explorer.config import MODEL_NAME
from typing import Sequence
import numpy as np

_model = None # used cached model if present

def load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def compute_embeddings(words: Sequence[str]) -> np.ndarray:
    """
    Compute embeddings for a list of words or sentences.
    Parameters
    ----------
    words : list[str]
    Returns
    -------
    numpy.ndarray
    """
    if isinstance(words, str): # Allow single word "chat" or ["chat"]
        words = [words]
                
    print(f"Loading {MODEL_NAME}")
    model = load_model()
    
    return model.encode(
    words,
    convert_to_numpy=True
)
