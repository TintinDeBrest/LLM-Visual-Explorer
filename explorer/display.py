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


def display_similarity_ranking(
    similarity_pairs,
    icons=None,
    top_n=10,
    bottom_n=10,
):
    """
    Display semantic similarity ranking.

    Shows:
    - top_n closest semantic neighbours
    - bottom_n semantic antipodes

    Parameters
    ----------
    similarity_pairs : list
        Sorted list of similarity tuples.

    icons : dict
        Mapping concept -> emoji.

    top_n : int
        Number of closest pairs displayed.

    bottom_n : int
        Number of least similar pairs displayed.
    """

    if icons is None:
        icons = {}

    print()
    print("=" * 70)
    print("🔗 SEMANTIC SIMILARITY RANKING")
    print("=" * 70)
    print()

    # ---------------------------------------------------
    # Helper function
    # ---------------------------------------------------

    def format_pair(rank, pair, highlight=False):

        a, b, score = pair

        emoji_a = icons.get(a, "")
        emoji_b = icons.get(b, "")

        bar_length = int(score * 20)

        bar = "█" * bar_length

        prefix = "🔻 " if highlight else "    "

        print(
            f"{prefix}{rank:>2}. "
            f"{emoji_a} {a:<12} ↔ "
            f"{emoji_b} {b:<12} "
            f"{bar:<20} "
            f"{score:.0%}"
        )

    # ---------------------------------------------------
    # TOP semantic neighbours
    # ---------------------------------------------------

    print("🟢 Les " f"{top_n} voisins sémantiques")

    print("-" * 70)

    for rank, pair in enumerate(similarity_pairs[:top_n], start=1):
        format_pair(rank, pair)

    # ---------------------------------------------------
    # Separator
    # ---------------------------------------------------

    hidden = len(similarity_pairs) - top_n - bottom_n

    if hidden > 0:

        print()
        print("-" * 70)
        print(f"              ⋮ {hidden} paires intermédiaires masquées ⋮")
        print("-" * 70)
        print()

    # ---------------------------------------------------
    # BOTTOM semantic antipodes
    # ---------------------------------------------------

    print(f"🔴 Les {bottom_n} antipodes sémantiques")

    print("-" * 70)

    bottom_pairs = similarity_pairs[-bottom_n:]

    # reverse order:
    # the least similar first
    bottom_pairs = list(reversed(bottom_pairs))

    for rank, pair in enumerate(bottom_pairs, start=1):

        format_pair(rank, pair, highlight=(rank == bottom_n))

    print()
