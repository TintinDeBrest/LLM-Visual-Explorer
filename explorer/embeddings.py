# embeddings
# PhL 28jul26
########################################################################

# Std lib
from typing import Sequence 
# 3rd party lib
import numpy as np
from sentence_transformers import SentenceTransformer
# Project lib
from explorer.config import MODEL_NAME

_model = None # Cached SentenceTransformer instance


def load_model():
    """Load the embedding model only once."""

    global _model

    if _model is None:
        print(f"Loading model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def compute_embeddings(words: str | Sequence[str]) -> np.ndarray:
    """
    Compute embeddings for one or more words or sentences.

    Parameters
    ----------
    words : str | Sequence[str]
        Input text(s).

    Returns
    -------
    numpy.ndarray
        One embedding vector per input text.
    """

    if isinstance(words, str):
        words = [words]

    model = load_model()

    return model.encode(
        words,
        convert_to_numpy=True,
    )
