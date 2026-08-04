# Display pour tous les affichages du notebook
# ===============================================

from explorer.config import MODEL_NAME


def display_scenario(scenario):
    """
    Affiche les informations principales du scénario.
    """
    print("=" * 60)

    print(f"SCÉNARIO : {scenario['title']}")

    print("=" * 60)

    print()

    print(scenario["description"])

    print()

    print("📋 Concepts analysés :")

    print()

    for obj in scenario["objects"]:

        emoji = obj.get("emoji", "")

        if emoji:
            print(f"   {emoji}  {obj['name']}")
        else:
            print(f"   •  {obj['name']}")

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

    print("=" * 70)
    print("🔗 SEMANTIC SIMILARITY RANKING")
    print("=" * 70)
    print()

    # Width of concept names
    name_width = max(max(len(a), len(b)) for a, b, _ in similarity_pairs) + 3

    bar_width = 25

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for rank, (a, b, score) in enumerate(similarity_pairs, start=1):

        icon_a = icons.get(a, "")
        icon_b = icons.get(b, "")

        percent = round(score * 100)

        filled = int(score * bar_width)
        bar = "█" * filled + " " * (bar_width - filled)

        medal = medals.get(rank, "  ")

        print(
            f"{medal} {rank:2d}. "
            f"{icon_a} {a:<{name_width}} ↔ "
            f"{icon_b} {b:<{name_width}} "
            f"{bar:<{bar_width}} "
            f"{percent:3d}%"
        )

    print()

    # Summary
    best = similarity_pairs[0]
    worst = similarity_pairs[-1]

    print("-" * 70)
    print("📌 SUMMARY")
    print("-" * 70)
    print()

    print(
        f"🥇 Most similar : "
        f"{icons.get(best[0], '')} {best[0]} ↔ "
        f"{icons.get(best[1], '')} {best[1]} "
        f"({round(best[2] * 100)}%)"
    )

    print()

    print(
        f"🔻 Least similar: "
        f"{icons.get(worst[0], '')} {worst[0]} ↔ "
        f"{icons.get(worst[1], '')} {worst[1]} "
        f"({round(worst[2] * 100)}%)"
    )

    print()
