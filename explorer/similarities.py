#=========================================================
# similarities.py -  To compare inputs 2 by 2
#==========================================================

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def compute_similarity(embeddings: np.ndarray) -> np.ndarray:
    """
    Compute the cosine similarity matrix between all embeddings.

    Parameters
    ----------
    embeddings : numpy.ndarray
        Embedding vectors.

    Returns
    -------
    numpy.ndarray
        NxN similarity matrix.
    """

    return cosine_similarity(embeddings)
