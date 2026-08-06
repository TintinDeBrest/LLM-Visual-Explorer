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


def rank_similarity_pairs(
    concepts,
    similarities,
    top_n=None,
    bottom_n=None,
):
    """
    Rank all concept pairs by cosine similarity.

    Parameters
    ----------
    concepts : list[str]
        Concept names.

    similarities : ndarray
        Cosine similarity matrix.

    top_n : int | None
        Number of most similar pairs to return.
        If None, keep all pairs.

    bottom_n : int | None
        Number of least similar pairs to append.
        Ignored if top_n is None.

    Returns
    -------
    list of tuple
        (concept1, concept2, similarity)
    """

    pairs = []

    n = len(concepts)

    for i in range(n):
        for j in range(i + 1, n):
            pairs.append(
                (
                    concepts[i],
                    concepts[j],
                    similarities[i, j],
                )
            )

    pairs.sort(
        key=lambda x: x[2],
        reverse=True,
    )

    # Default behaviour: return all pairs
    if top_n is None:
        return pairs

    top_pairs = pairs[:top_n]

    if bottom_n is None:
        return top_pairs

    bottom_pairs = pairs[-bottom_n:]

    return top_pairs + bottom_pairs
