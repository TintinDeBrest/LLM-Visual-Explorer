''' Fonctions pour LLM VISUAL EXPLORER report '''

def display_report(
    scenario_name,
    model_name,
    concepts,
    embedding_dimension,
    pca,
    similarity_pairs,
):
    """
    Display a summary report of the current exploration.
    """

    explained = pca.explained_variance_ratio_ * 100
    total = explained.sum()

    best = similarity_pairs[0]
    worst = similarity_pairs[-1]

    print()
    print("=" * 60)
    print("LLM VISUAL EXPLORER REPORT")
    print("=" * 60)
    print()

    print(f"Scenario              : {scenario_name}")
    print(f"Model                 : {model_name}")
    print(f"Number of concepts    : {len(concepts)}")
    print(f"Embedding dimension   : {embedding_dimension}")

    print()
    print("-" * 60)
    print("3D PROJECTION (PCA)")
    print("-" * 60)

    print(f"PC1 : {explained[0]:5.1f}%")
    print(f"PC2 : {explained[1]:5.1f}%")
    print(f"PC3 : {explained[2]:5.1f}%")

    print()

    print(
        f"{embedding_dimension} Dim → 3D preserves {total:.1f}% "
        "of the semantic structure"
    )

    print()
    print("-" * 60)
    print("SEMANTIC OBSERVATIONS")
    print("-" * 60)

    print(
        f"Closest concepts : "
        f"{best[0]} ↔ {best[1]} "
        f"({best[2]:.2f})"
    )

    print(
        f"Farthest concepts: "
        f"{worst[0]} ↔ {worst[1]} "
        f"({worst[2]:.2f})"
    )

    print()
