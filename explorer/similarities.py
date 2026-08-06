# =========================================================
# similarities.py -  To compare inputs 2 by 2
# ==========================================================

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


def rank_similarity_pairs(concepts, similarities):
    """
    Return all concept pairs sorted by decreasing similarity.

    Parameters
    ----------
    concepts : list
        List of concept names.

    similarities : numpy.ndarray
        Similarity matrix.

    Returns
    -------
    list of tuples
        [(concept1, concept2, similarity), ...]
        sorted from highest to lowest similarity.
    """

    pairs = []

    n = len(concepts)

    for i in range(n):
        for j in range(i + 1, n):

            pairs.append((concepts[i], concepts[j], similarities[i, j]))

    # Highest similarity first
    pairs.sort(key=lambda x: x[2], reverse=True)

    return pairs
