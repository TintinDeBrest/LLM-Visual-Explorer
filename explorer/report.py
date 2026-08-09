"""
Fonctions pour LLM VISUAL EXPLORER report
"""

from explorer.config import MODEL_ALIAS, MODEL_NAME


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
    print(f"Model alias           : {MODEL_ALIAS}")
    print(f"Technical Model       : {MODEL_NAME}")
    print(f"Number of concepts    : {len(concepts)}")
    print(f"Embedding dimension   : {embedding_dimension}")

    print()

    # ---------------------------------------------------------
    # PCA
    # ---------------------------------------------------------

    print("-" * 70)
    print("📐 PROJECTION 3D (PCA)")
    print("-" * 70)

    # print(f"PC1 : {explained[0]:5.1f}%")
    # print(f"PC2 : {explained[1]:5.1f}%")
    # print(f"PC3 : {explained[2]:5.1f}%")

    print()

    print(
        f"{embedding_dimension} dimensions → 3D préserve "
        f"{total:.1f}% de la structure sémantique"
    )

    print()

    # print("The visualization is a projection of a high-dimensional " "semantic space.")

    # ---------------------------------------------------------
    # Semantic observations
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("🔗 OBSERVATIONS SEMANTIQUES")
    print("-" * 70)

    print()

    print(f"🥇 Paire la plus proche : " f"{best[0]} ↔ {best[1]} " f"({best[2]:.0%})")

    print(
        f"🔻 Paire la plus éloignée: " f"{worst[0]} ↔ {worst[1]} " f"({worst[2]:.0%})"
    )

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
    print("  • similarities.csv  → semantic similarities")

    # ---------------------------------------------------------
    # Going further
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("🚀 ALLEZ PLUS LOIN")
    print("-" * 70)

    print()

    print("Les paires les plus surprenantes sont souvent les plus interessantes.")

    print(
        "Vous pouvez copier une de ces paires de concepts surprenant pour la "
        "soumettre à un LLM génératif afin d'obtenir une analyse qualitative."
    )

    print()

    print("PROMPT A COPIER:")
    print("-" * 70)

    print("""
Bonjour,

Un modèle d'intelligence artificielle représentant les concepts dans un
espace vectoriel sémantique considère que les deux concepts suivants sont
<proches/éloignés> :

<Concept1> et <Concept2>

Je voudrais savoir si vous considérez, à priori, que cette relation est
pertinente.

Pouvez-vous fournir :
- des arguments en faveur de cette proximité ou de cet éloignement ;
- des exemples concrets illustrant votre analyse ;
- des nuances ou contre-arguments éventuels ?

L'objectif est de mieux comprendre pourquoi ces deux concepts peuvent être
associés (ou séparés) dans un espace sémantique.
""")

    print("-" * 70)

    print()

    print("Note: le modèle révèle des structures mais " "ne donne pas d'explications")

    print("Un LLM géneratif peut vous aider à interpreter ces structures.")

    print()
