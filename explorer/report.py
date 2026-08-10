"""
Fonctions pour LLM VISUAL EXPLORER report
"""

from pathlib import Path
import base64

from IPython.display import display, HTML

from explorer.config import MODEL_ALIAS, MODEL_NAME
from explorer.display import create_prompt_button, create_pair_selector


def display_report(
    scenario_name,
    model_name,
    concepts,
    embedding_dimension,
    pca,
    similarity_pairs,
):
    logo_path = Path(__file__).resolve().parent.parent / "images" / "LlmExpl_logo.png"

    with open(logo_path, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()

    """
    Display a summary report of the current exploration.
    """

    explained = pca.explained_variance_ratio_ * 100
    total = explained.sum()

    best = similarity_pairs[0]
    worst = similarity_pairs[-1]

    print()
    print("=" * 70)
    ###############################################
    display(HTML(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <img
                src="data:image/png;base64,{logo_data}"
                width="55"
            >
            <span style="
                font-size: 1.5em;
                font-weight: bold;
            ">
                LLM VISUAL EXPLORER REPORT
            </span>
        </div>
        """))
    ###############################################
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

    print()

    print(
        f"{embedding_dimension} dimensions → 3D préserve "
        f"{total:.1f}% de la structure sémantique"
    )

    print()

    # ---------------------------------------------------------
    # Semantic observations
    # ---------------------------------------------------------

    print("-" * 70)
    print("🔗 OBSERVATIONS SEMANTIQUES")
    print("-" * 70)

    print()

    print(f"🥇 Paire la plus proche : " f"{best[0]} ↔ {best[1]} ({best[2]:.0%})")

    print(f"🔻 Paire la plus éloignée : " f"{worst[0]} ↔ {worst[1]} ({worst[2]:.0%})")

    print()

    # ---------------------------------------------------------
    # Going further
    # ---------------------------------------------------------

    print("-" * 70)
    print("🚀 ALLEZ PLUS LOIN")
    print("-" * 70)

    print()

    print("Une proximité ou un éloignement peut être surprenant.")

    print("Choisissez une paire qui vous intrigue et soumettez-la grâce à ces ")
    print("prompt à un LLM génératif pour obtenir une analyse qualitative.")

    print()

    # Closest pair

    print(f"🥇 Paire la plus proche : " f"{best[0]} ↔ {best[1]} ({best[2]:.0%})")

    display(
        create_prompt_button(
            best[0],
            best[1],
            "proches",
        )
    )

    print()

    # Farthest pair

    print(f"🔻 Paire la plus éloignée : " f"{worst[0]} ↔ {worst[1]} ({worst[2]:.0%})")

    display(
        create_prompt_button(
            worst[0],
            worst[1],
            "éloignés",
        )
    )

    print()

    # Any pair

    print("🔎 EXPLORER UNE AUTRE PAIRE")

    display(create_pair_selector(similarity_pairs))

    print()

    print(
        "Note : LlmExpl révèle des structures dans l'espace sémantique, "
        "mais ne donne pas d'explications."
    )

    print(
        "Coller ces prompts pour interroger un LLM génératif (ChatGPT, Gemini, Claude ...)"
    )
    print("peut vous aider à expliquer ces structures ")

    print()
    """
    # ---------------------------------------------------------
    # Data export
    # ---------------------------------------------------------

    print("-" * 70)
    print("💾 EXPORT DES DONNÉES")
    print("-" * 70)

    print()

    print(
        "Les données numériques utilisées pendant cette exploration "
        "peuvent être sauvegardées :"
    )

    print()

    print("  • concepts.csv      → concepts et catégories")
    print("  • embeddings.csv    → vecteurs sémantiques")
    print("  • projection.csv    → coordonnées PCA")
    print("  • similarities.csv  → similarités sémantiques")
    """
    print()
