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
    pairs,
    icons=None,
    top_n=10,
    bottom_n=10,
):
    """
    Display the closest and most distant semantic pairs.

    Parameters
    ----------
    pairs : list
        List of tuples (word1, word2, similarity)
        sorted by decreasing similarity.

    icons : dict
        Dictionary mapping concepts to emojis.

    top_n : int
        Number of highest similarity pairs displayed.

    bottom_n : int
        Number of lowest similarity pairs displayed.
    """

    if icons is None:
        icons = {}

    print("=" * 70)
    print("🔗 SEMANTIC SIMILARITY RANKING")
    print("=" * 70)
    print()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def format_concept(word):
        emoji = icons.get(word, "")
        return f"{emoji} {word}".strip()

    def similarity_bar(value):
        # value between -1 and 1
        length = int(value * 24)
        return "█" * length

    def display_pair(rank, pair, highlight=False):

        w1, w2, sim = pair

        prefix = "🔻" if highlight else "   "

        print(
            f"{prefix}{rank:>3}. "
            f"{format_concept(w1):<15} ↔ "
            f"{format_concept(w2):<15} "
            f"{similarity_bar(sim)} "
            f"{sim:.0%}"
        )

    # ---------------------------------------------------------
    # Top semantic neighbours
    # ---------------------------------------------------------

    print("🟢 Les 10 voisins sémantiques")
    print("-" * 70)

    top_pairs = pairs[:top_n]

    for rank, pair in enumerate(top_pairs, start=1):

        if rank == 1:
            display_pair(rank, pair, highlight=False)

        elif rank == 2:
            display_pair(rank, pair)

        elif rank == 3:
            display_pair(rank, pair)

        else:
            display_pair(rank, pair)

    # ---------------------------------------------------------
    # Hidden middle section
    # ---------------------------------------------------------

    hidden = len(pairs) - top_n - bottom_n

    print()
    print("-" * 70)
    print(f"              ⋮ {hidden} paires intermédiaires masquées ⋮")
    print("-" * 70)
    print()

    # ---------------------------------------------------------
    # Bottom semantic antipodes
    # ---------------------------------------------------------

    print("🔴 Les 10 antipodes sémantiques")
    print("-" * 70)

    bottom_pairs = pairs[-bottom_n:]

    start_rank = len(pairs) - bottom_n + 1

    for rank, pair in enumerate(bottom_pairs, start=start_rank):

        display_pair(rank, pair, highlight=(rank == len(pairs)))

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("📌 SUMMARY")
    print("-" * 70)
    print()

    best = pairs[0]
    worst = pairs[-1]

    print(
        f"🥇 Most similar : "
        f"{format_concept(best[0])} ↔ "
        f"{format_concept(best[1])} "
        f"({best[2]:.0%})"
    )

    print()

    print(
        f"🔻 Least similar: "
        f"{format_concept(worst[0])} ↔ "
        f"{format_concept(worst[1])} "
        f"({worst[2]:.0%})"
    )
