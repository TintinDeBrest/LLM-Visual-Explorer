# ====================================================================
# report.py
# ====================================================================

import textwrap
import base64

from pathlib import Path

from IPython.display import display, HTML


from explorer.config import (
    MODEL_ALIAS,
    MODEL_NAME,
    MODEL_TYPE,
    REPRESENTATION_MODE,
)

from explorer.display import (
    create_group_selector,
    create_pair_selector,
    create_prompt_button,
)

from explorer.exports import create_planetarium_export_button
from explorer.i18n import tr


def print_wrapped(text, width=88):
    """
    Print long report text with controlled line wrapping.
    """
    print(
        textwrap.fill(
            text,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def display_report(
    scenario,
    concepts,
    embedding_dimension,
    pca,
    similarity_pairs,
    scenario_name=None,
    planetarium_figure=None,
):
    """
    Display a summary report of the current exploration.
    """

    export_scenario_name = scenario_name or scenario.get("_name")

    if planetarium_figure is not None and not export_scenario_name:
        raise ValueError(
            tr("scenario_name_required_for_planetarium")
        )

    logo_path = (
        Path(__file__).resolve().parent.parent
        / "images"
        / "LlmExpl_logo.png"
    )

    with open(logo_path, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()

    explained = pca.explained_variance_ratio_ * 100
    total = explained.sum()

    best = similarity_pairs[0]
    worst = similarity_pairs[-1]

    print()
    print("=" * 70)

    display(
        HTML(
            f"""
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
                    {tr("report_title")}
                </span>
            </div>
            """
        )
    )

    print("=" * 70)
    print()

    # ---------------------------------------------------------
    # General information
    # ---------------------------------------------------------

    print(
        f"{tr('report_scenario'):<22}: "
        f"{scenario['title']}"
    )

    print(scenario["description"])
    print()

    print(
        f"{tr('report_model_alias'):<22}: "
        f"{MODEL_ALIAS}"
    )

    print(
        f"{tr('report_technical_model'):<22}: "
        f"{MODEL_NAME}"
    )

    print(
        f"{tr('report_concept_count'):<22}: "
        f"{len(concepts)}"
    )

    if MODEL_TYPE == "generative":
        dimension_label = (
            tr("report_intermediate_state_delta_dimension")
            if REPRESENTATION_MODE == "common_suffix_middle_delta"
            else tr("report_predictive_state_dimension")
        )
    else:
        dimension_label = tr("report_embedding_dimension")

    print(
        f"{dimension_label:<22}: "
        f"{embedding_dimension}"
    )

    print()

    # ---------------------------------------------------------
    # PCA
    # ---------------------------------------------------------

    print("-" * 70)
    print(f"📐 {tr('report_projection_3d')}")
    print("-" * 70)
    print()

    print(
        tr(
            "report_pca_summary",
            dimension=embedding_dimension,
            variance=f"{total:.1f}",
        )
    )

    print()

    # ---------------------------------------------------------
    # Semantic observations
    # ---------------------------------------------------------

    print("-" * 70)
    print(f"🔗 {tr('report_semantic_observations')}")
    print("-" * 70)
    print()

    print(
        f"🥇 {tr('closest_pair')} : "
        f"{best[0]} ↔ {best[1]} ({best[2]:.0%})"
    )

    print(
        f"🔻 {tr('farthest_pair')} : "
        f"{worst[0]} ↔ {worst[1]} ({worst[2]:.0%})"
    )

    print()

    # ---------------------------------------------------------
    # Going further
    # ---------------------------------------------------------

    print("-" * 70)
    print(f"🚀 {tr('report_go_further')}")
    print("-" * 70)
    print()

    print_wrapped(tr("report_pair_intro"))
    print()

    # Closest pair

    print(
        f"🥇 {tr('closest_pair')} : "
        f"{best[0]} ↔ {best[1]} ({best[2]:.0%})"
    )

    display(
        create_prompt_button(
            best[0],
            best[1],
            MODEL_NAME,
            best[2],
        )
    )

    print()

    # Farthest pair

    print(
        f"🔻 {tr('farthest_pair')} : "
        f"{worst[0]} ↔ {worst[1]} ({worst[2]:.0%})"
    )

    display(
        create_prompt_button(
            worst[0],
            worst[1],
            MODEL_NAME,
            worst[2],
        )
    )

    print()

    # Any pair

    print(f"🔎 {tr('explore_another_pair')}")

    display(
        create_pair_selector(
            similarity_pairs,
            MODEL_NAME,
        )
    )

    print()

    # Concept group

    print_wrapped(tr("report_group_intro"))
    print()

    print(f"🧩 {tr('explore_group_four')}")

    display(
        create_group_selector(
            similarity_pairs,
            MODEL_NAME,
        )
    )

    print()

    # Planetarium export

    if planetarium_figure is not None:
        print(
            f"📷 {tr('save_planetarium').upper()}"
        )

        display(
            create_planetarium_export_button(
                planetarium_figure,
                export_scenario_name,
                MODEL_ALIAS,
            )
        )

        print()

    # ---------------------------------------------------------
    # Interpretation note
    # ---------------------------------------------------------


    print_wrapped(tr("report_interpretation_note"))
    print_wrapped(tr("report_llm_prompt_note"))
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