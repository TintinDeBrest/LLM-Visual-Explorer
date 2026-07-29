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


def rank_similarity_pairs(words, similarities):
    """
    Return word pairs sorted by decreasing similarity.
    """

    pairs = []

    n = len(words)

    for i in range(n):
        for j in range(i + 1, n):
            pairs.append(
                (
                    words[i],
                    words[j],
                    similarities[i, j]
                )
            )

    pairs.sort(
        key=lambda x: x[2],
        reverse=True
    )

    return pairs
