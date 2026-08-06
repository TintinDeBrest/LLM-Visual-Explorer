"""
Fonctions pour LLM VISUAL EXPLORER report
"""


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
    print("=" * 70)
    print("🌌 LLM VISUAL EXPLORER REPORT")
    print("=" * 70)
    print()

    # ---------------------------------------------------------
    # General information
    # ---------------------------------------------------------

    print(f"Scenario              : {scenario_name}")
    print(f"Model                 : {model_name}")
    print(f"Number of concepts    : {len(concepts)}")
    print(f"Embedding dimension   : {embedding_dimension}")

    print()

    # ---------------------------------------------------------
    # PCA
    # ---------------------------------------------------------

    print("-" * 70)
    print("📐 3D PROJECTION (PCA)")
    print("-" * 70)

    print(f"PC1 : {explained[0]:5.1f}%")
    print(f"PC2 : {explained[1]:5.1f}%")
    print(f"PC3 : {explained[2]:5.1f}%")

    print()

    print(
        f"{embedding_dimension} dimensions → 3D preserves "
        f"{total:.1f}% of the semantic structure"
    )

    print()

    print("The visualization is a projection of a high-dimensional " "semantic space.")

    # ---------------------------------------------------------
    # Semantic observations
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("🔗 SEMANTIC OBSERVATIONS")
    print("-" * 70)

    print()

    print(f"🥇 Closest concepts : " f"{best[0]} ↔ {best[1]} " f"({best[2]:.0%})")

    print(f"🔻 Farthest concepts: " f"{worst[0]} ↔ {worst[1]} " f"({worst[2]:.0%})")

    # ---------------------------------------------------------
    # Data export
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("💾 DATA EXPORT")
    print("-" * 70)

    print()

    print("The numerical data used during this exploration can be saved:")

    print()
    print("  • concepts.csv      → concepts and categories")
    print("  • embeddings.csv    → semantic vectors")
    print("  • projection.csv    → PCA coordinates")
    print("  • similarities.csv  → semantic distances")

    # ---------------------------------------------------------
    # Going further
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("🚀 GO FURTHER")
    print("-" * 70)

    print()

    print("The most surprising pairs are often the most interesting ones.")

    print(
        "You can copy one of these pairs into a generative LLM "
        "to obtain a qualitative analysis."
    )

    print()

    print("PROMPT TO COPY:")
    print("-" * 70)

    print("""
Hello,

An AI model representing concepts in a semantic vector space
considers the following two concepts:

<Concept1> and <Concept2>

I would like to know whether you consider, a priori, that these
concepts are semantically close or distant.

Could you provide:
- arguments supporting or challenging this relationship;
- concrete examples illustrating your analysis;
- possible nuances or counter-arguments?

The objective is to better understand why these concepts may be
associated (or separated) in a semantic space.
""")

    print("-" * 70)

    print()

    print(
        "Note: the embedding model reveals semantic structures, "
        "but does not provide explanations."
    )

    print("A generative LLM can then help interpret these structures.")

    print()
