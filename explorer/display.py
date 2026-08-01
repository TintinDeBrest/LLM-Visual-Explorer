# Display pour tous les affichages du notebook
#===============================================

from explorer.config import MODEL_NAME


def display_scenario(scenario):
    """
    Affiche les informations principales du scenario
    """
    print("=" * 60)

    print(f"SCÉNARIO : {scenario['title']}")

    print("=" * 60)

    print()

    print(scenario["description"])

    print()

    print("Objets analysés :")

    print()

    for obj in scenario["objects"]:

        print(f"   • {obj['name']}")

    print()

    print(f"Nombre d'objets : {len(scenario['objects'])}")

    print("=" * 60)


def display_model(model):
    """
    Affiche les informations principales du modèle d'embeddings.
    """

    print("=" * 60)
    print("MODÈLE D'EMBEDDINGS")
    print("=" * 60)
    print()

    print("Architecture :")
    print(f"  {model.__class__.__name__}")
    print()

    print("Modèle :")
    print(f"  {MODEL_NAME}")
    print()

    print("Dimension des embeddings :")
    print(f"  {model.get_embedding_dimension()}")

    print()


def display_projection(explained_variance, pca=None):
    """
    Affiche l'information conservée par la projection 3D.
    
    Parameters
    ----------
    explained_variance : float
        Pourcentage de variance conservée par les trois premières composantes.
    """

    print("=" * 60)
    print("PROJECTION 3D")
    print("=" * 60)
    print()

    print(
        f"La projection 3D conserve environ "
        f"{explained_variance:.1f}% "
        "de la variance des embeddings."
    )

    print()


def display_similarity_ranking(similarity_pairs, icons=None):
    """
    Display a ranked list of semantic similarities.

    Parameters
    ----------
    similarity_pairs : list of tuples
        List of (item1, item2, similarity), sorted from highest to lowest.

    icons : dict, optional
        Dictionary mapping item names to emojis/icons.
    """

    if icons is None:
        icons = {}

    print("=" * 60)
    print("SEMANTIC SIMILARITY RANKING")
    print("=" * 60)
    print()

    for rank, (a, b, score) in enumerate(similarity_pairs, start=1):

        icon_a = icons.get(a, "")
        icon_b = icons.get(b, "")

        label_a = f"{icon_a} {a}".strip()
        label_b = f"{icon_b} {b}".strip()

        bar = "█" * int(score * 30)

        print(
            f"{rank:2d}. "
            f"{label_a:<15} ↔ "
            f"{label_b:<15} "
            f"{bar:<30} "
            f"{score:.2f}"
        )

    print()

    best = similarity_pairs[0]
    worst = similarity_pairs[-1]

    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print()

    print(
        f"Most similar : "
        f"{icons.get(best[0], '')} {best[0]} ↔ "
        f"{icons.get(best[1], '')} {best[1]} "
        f"({best[2]:.2f})"
    )

    print()

    print(
        f"Least similar: "
        f"{icons.get(worst[0], '')} {worst[0]} ↔ "
        f"{icons.get(worst[1], '')} {worst[1]} "
        f"({worst[2]:.2f})"
    )

    print()



