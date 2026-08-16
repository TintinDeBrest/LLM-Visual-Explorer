# ========================================================
# semantic_core.py
# ========================================================

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def build_semantic_core(embeddings, concepts, strength_mode="relative"):
    """
    Construit progressivement un noyau sémantique.

    Principe :
    1. On commence par la paire de concepts la plus similaire.
    2. À chaque étape, on ajoute le concept qui est le plus similaire
       au noyau déjà constitué.
    3. On calcule une force sémantique, soit relative à la paire initiale,
       soit comparable entre scénarios pour un même modèle.

    Retourne :
        core_order : liste des concepts dans l'ordre d'intégration
        semantic_strength : dictionnaire {concept: force}
    """

    if strength_mode not in {"relative", "comparable"}:
        raise ValueError("strength_mode must be 'relative' or 'comparable'")

    # Matrice des similarités
    similarity_matrix = cosine_similarity(embeddings)

    n = len(concepts)

    # ------------------------------------------------------------
    # 1. Trouver la paire initiale la plus similaire
    # ------------------------------------------------------------

    max_similarity = -1
    first_pair = None

    for i in range(n):
        for j in range(i + 1, n):

            similarity = similarity_matrix[i, j]

            if similarity > max_similarity:
                max_similarity = similarity
                first_pair = (i, j)

    i, j = first_pair

    core_indices = [i, j]

    # En mode relatif, la paire majeure vaut toujours 1. En mode comparable,
    # sa force est sa similarité réelle, ce qui conserve l'échelle 0..1 entre
    # scénarios exécutés avec le même modèle.
    initial_strength = 1.0 if strength_mode == "relative" else max_similarity
    semantic_strength = {concepts[i]: initial_strength, concepts[j]: initial_strength}

    core_order = [concepts[i], concepts[j]]

    # ------------------------------------------------------------
    # 2. Construction progressive du noyau
    # ------------------------------------------------------------

    while len(core_indices) < n:

        best_index = None
        best_similarity = -1

        for candidate in range(n):

            if candidate in core_indices:
                continue

            # Similarité du candidat avec les concepts déjà
            # présents dans le noyau.
            similarities_to_core = [
                similarity_matrix[candidate, core] for core in core_indices
            ]

            # On utilise la moyenne :
            # le candidat doit être proche de l'ensemble du noyau.
            mean_similarity = np.mean(similarities_to_core)

            if mean_similarity > best_similarity:
                best_similarity = mean_similarity
                best_index = candidate

        # Ajout du nouveau concept
        core_indices.append(best_index)
        core_order.append(concepts[best_index])

        # Force relative au noyau initial, ou force comparable directement
        # exprimée par la similarité moyenne avec le noyau.
        if strength_mode == "relative":
            strength = best_similarity / max_similarity
        else:
            strength = best_similarity

        semantic_strength[concepts[best_index]] = strength

    return core_order, semantic_strength
