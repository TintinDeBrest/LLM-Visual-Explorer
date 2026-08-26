# Display pour tous les affichages du notebook
# ===============================================


from explorer.config import MODEL_ALIAS, MODEL_TYPE, REPRESENTATION_MODE
from explorer.i18n import format_number, tr
from explorer.feedback import display_feedback, feedback_html
from textwrap import fill
from explorer.prompts import create_prompt

import numpy as np


def display_scenario(scenario):
    """
    Build a compact summary of the loaded scenario.
    """
    title = scenario["title"]
    objects = scenario["objects"]
    n_concepts = len(objects)

    details = (
        f"{title} · "
        f"{tr('concept_count')}: {n_concepts}"
    )

    return feedback_html(
        title=tr("scenario_loaded"),
        details=details,
        status="success",
    )


def display_model(model, concept_count):
    """
    Display a compact summary of the computed semantic representations.
    """

    if MODEL_TYPE == "generative":
        if REPRESENTATION_MODE == "common_suffix_middle_delta":
            title_key = "intermediate_state_variations_computed"
        else:
            title_key = "predictive_states_computed"
    else:
        title_key = "embeddings_computed"

    embedding_dimension = model.get_embedding_dimension()

    details = " · ".join(
        [
            MODEL_ALIAS,
            tr("concepts_compact", count=concept_count),
            tr("dimensions_compact", count=embedding_dimension),
        ]
    )

    display_feedback(
        title=tr(title_key),
        details=details,
        status="success",
    )


def display_projection(pca):
    """
    Display a compact summary of the computed 3D PCA projection.

    Parameters
    ----------
    pca : PCA
        PCA object used for the projection.
    """

    explained_variance = (
        pca.explained_variance_ratio_.sum() * 100
    )

    details = " · ".join(
        [
            tr("dimensions_compact", count=pca.n_components_),
            tr("variance_retained", value=explained_variance),
        ]
    )

    display_feedback(
        title=tr("pca_projection_computed"),
        details=details,
        status="success",
    )


def display_similarity_ranking(
    similarity_pairs,
    df_projection,
    icons=None,
    top_n=10,
    bottom_n=10,
):
    """
    Display semantic similarity ranking.

    Shows:
    - top_n closest semantic neighbours
    - bottom_n semantic antipodes
    - distance between concepts in the projected 3D PCA space

    Similarity thresholds are indicative and model-dependent.

    Parameters
    ----------
    similarity_pairs : list
        Sorted list of similarity tuples.

    df_projection : DataFrame
        DataFrame containing Mot, PC1, PC2, PC3.

    icons : dict
        Mapping concept -> emoji.

    top_n : int
        Number of closest pairs displayed.

    bottom_n : int
        Number of least similar pairs displayed.
    """

    if icons is None:
        icons = {}

    display_feedback(
        title=tr("similarity_ranking"),
        details=tr(
            "ranking_details",
            count=len(similarity_pairs),
        ),
        status="success",
    )

    print()

    print(f"{tr('indicative_thresholds')}:")

    print(
        f"🟢 {tr('high_similarity_range'):<10} "
        f"{tr('high_similarity')}"
    )
    print(
        f"🟡 {tr('medium_similarity_range'):<10} "
        f"{tr('medium_similarity')}"
    )
    print(
        f"🔴 {tr('low_similarity_range'):<10} "
        f"{tr('low_similarity')}"
    )

    print()
    print(
        fill(
            tr("similarity_scale_note"),
            width=80,
            subsequent_indent="    ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    )
    print()


    # ---------------------------------------------------
    # Helper functions
    # ---------------------------------------------------

    def compute_3d_distance(a, b):

        pa = df_projection.loc[df_projection["Mot"] == a, ["PC1", "PC2", "PC3"]].values[
            0
        ]

        pb = df_projection.loc[df_projection["Mot"] == b, ["PC1", "PC2", "PC3"]].values[
            0
        ]

        return np.linalg.norm(pa - pb)

    names_a = [a for a, _, _ in similarity_pairs]
    names_b = [b for _, b, _ in similarity_pairs]

    width_a = max(len(name) for name in names_a)
    width_b = max(len(name) for name in names_b)

    def format_pair(rank, pair, highlight=False):

        a, b, score = pair

        emoji_a = icons.get(a, "")
        emoji_b = icons.get(b, "")

        distance_3d = compute_3d_distance(a, b)

        bar_length = int(score * 20)

        bar = "█" * bar_length

        prefix = "🔻 " if highlight else "    "

        print(
            f"{prefix}{rank:>2}. "
            f"{emoji_a} {a:<{width_a}} ↔ "
            f"{emoji_b} {b:<{width_b}} "
            f"{bar:<20} "
            f"{tr('similarity_short')}: {score:.0%}  "
            f"{tr('distance_short')}: {distance_3d:.1f}"
        )

    # ---------------------------------------------------
    # TOP semantic neighbours
    # ---------------------------------------------------


    print(
        f"🟢 "
        f"{tr('top_semantic_neighbours', count=top_n)}"
    )

    print("-" * 80)

    for rank, pair in enumerate(similarity_pairs[:top_n], start=1):
        format_pair(rank, pair)

    # ---------------------------------------------------
    # Separator
    # ---------------------------------------------------

    hidden = len(similarity_pairs) - top_n - bottom_n

    if hidden > 0:

        print()
        print("-" * 80)

        hidden_message = tr(
            "hidden_intermediate_pairs",
            count=hidden,
        )
        print(f"              ⋮ {hidden_message} ⋮")

        print("-" * 80)
        print()

    # ---------------------------------------------------
    # BOTTOM semantic antipodes
    # ---------------------------------------------------

    print(
        f"🔴 "
        f"{tr('semantic_antipodes', count=bottom_n)}"
    )

    print("-" * 80)

    bottom_pairs = similarity_pairs[-bottom_n:]

    # Reverse order:
    # the least similar first
    bottom_pairs = list(reversed(bottom_pairs))

    for rank, pair in enumerate(bottom_pairs, start=1):

        format_pair(rank, pair, highlight=(rank == bottom_n))

    print()


import markdown
import ipywidgets as widgets
from IPython.display import display, HTML

MESSAGES = [
    """
# 1. Les mots (ou "concepts") ont une "géométrie"

Ils ne sont pas rangés dans un dictionnaire.

Ils « vivent » dans un **espace sémantique**,
qui peut comporter plusieurs centaines, voire plusieurs milliers
de nombres (dimensions) pour représenter chaque concept.

Il est même possible de les "voir", mais par un "trou de serrure" avec
**LLM-Visual-Explorer** (LlmExpl).
""",
    """
# 2. La proximité sémantique des concepts est statistique, pas logique

Deux concepts proches ne sont pas nécessairement synonymes.

Ils ont simplement tendance à **apparaître dans des contextes similaires**.
""",
    """
# 3. Les modèles IA « apprennent » notre langage …

… mais pas nécessairement **notre vision du monde**.

Ces modèles IA (ou LLM) analysent statistiquement d'immenses quantités de textes :
nos livres, nos journaux, nos conversations…

Ce sont fondamentalement des systèmes statistiques. Cependant, de mécanismes
statistiques peuvent **émerger** des comportements étonnamment complexes.

Ils construisent avec ces analyses un **espace sémantique**
que **LlmExpl vous permet d'explorer visuellement.**
""",
    """
# 4. Et demain ?

**LLM-Visual-Explorer (LlmExpl) V2** ira plus loin dans l'exploration
de cet espace sémantique.

De nouveaux modèles, de nouveaux scénarios,
et surtout de nouvelles façons de **comparer,
explorer et comprendre les représentations du langage**
(contexte, attention, ...).

---

### Merci pour votre exploration !

**Philippe Launay**  
📧 *pefsysly@gmail.com*
""",
]


def display_messages():
    """
    Display the conclusion messages as an interactive slideshow.
    """

    current = 0
    output = widgets.Output()

    previous_button = widgets.Button(
        description="←",
        tooltip="Message précédent",
        layout=widgets.Layout(width="45px"),
    )

    next_button = widgets.Button(
        description="→", tooltip="Message suivant", layout=widgets.Layout(width="45px")
    )

    def update_display():
        output.clear_output(wait=True)

        html = markdown.markdown(MESSAGES[current])

        with output:
            display(HTML(f"""
                <div style="
                    font-size: 1.2em;
                    line-height: 1.6;
                ">
                    {html}
                </div>
            """))

        previous_button.disabled = current == 0
        next_button.disabled = current == len(MESSAGES) - 1

    def previous_message(button):
        nonlocal current

        if current > 0:
            current -= 1
            update_display()

    def next_message(button):
        nonlocal current

        if current < len(MESSAGES) - 1:
            current += 1
            update_display()

    previous_button.on_click(previous_message)
    next_button.on_click(next_message)

    navigation = widgets.HBox(
        [previous_button, next_button],
        layout=widgets.Layout(justify_content="center", gap="10px"),
    )

    display(output)
    display(navigation)

    update_display()


def create_prompt_button(
    concept1,
    concept2,
    model_name,
    similarity,
):
    """
    Create a button that copies a ready-to-use LLM prompt
    to the user's clipboard.
    """
    import ipywidgets as widgets
    import pyperclip

    prompt = create_prompt(
        concept1,
        concept2,
        model_name,
        similarity,
    )

    button = widgets.Button(
        description=f"📋 {tr('copy_prompt')}",
        tooltip=tr("copy_pair_prompt_tooltip"),
        layout=widgets.Layout(width="180px"),
    )

    def copy_prompt(button):
        try:
            pyperclip.copy(prompt)
        except pyperclip.PyperclipException:
            button.description = "⚠️ Copy failed"
            return

        button.description = f"✓ {tr('prompt_copied')}"

    button.on_click(copy_prompt)

    return button


def create_pair_selector(
    similarity_pairs,
    model_name,
):
    """
    Create a dropdown allowing the user to select any
    concept pair and copy its corresponding LLM prompt.
    """
    import ipywidgets as widgets
    import pyperclip

    options = [
        (
            f"{pair[0]} ↔ {pair[1]} — {pair[2]:.0%}",
            pair,
        )
        for pair in similarity_pairs
    ]

    selector = widgets.Dropdown(
        options=options,
        description="",
        layout=widgets.Layout(width="300px"),
    )

    button = widgets.Button(
        description=f"📋 {tr('copy_prompt')}",
        tooltip=tr("copy_pair_prompt_tooltip"),
        layout=widgets.Layout(width="180px"),
    )

    def copy_selected_prompt(button):
        pair = selector.value

        prompt = create_prompt(
            pair[0],
            pair[1],
            model_name,
            pair[2],
        )

        try:
            pyperclip.copy(prompt)
        except pyperclip.PyperclipException:
            button.description = "⚠️ Copy failed"
            return

        button.description = f"✓ {tr('prompt_copied')}"

    button.on_click(copy_selected_prompt)

    return widgets.VBox([selector, button])


def create_group_selector(
    similarity_pairs,
    model_name,
):
    """
    Create four concept dropdowns and copy a prompt describing
    the six similarities between the selected concepts.
    """

    import ipywidgets as widgets
    from IPython.display import display, Javascript
    import json
    from itertools import combinations

    concepts = []

    for concept_a, concept_b, _ in similarity_pairs:
        for concept in (concept_a, concept_b):
            if concept not in concepts:
                concepts.append(concept)

    if len(concepts) < 4:
        raise ValueError(tr("minimum_four_concepts"))

    similarity_lookup = {
        frozenset((concept_a, concept_b)): score
        for concept_a, concept_b, score in similarity_pairs
    }

    selectors = [
        widgets.Dropdown(
            options=concepts,
            value=concepts[index],
            description=tr(
                "concept_number",
                number=index + 1,
            ),
            layout=widgets.Layout(width="300px"),
            style={"description_width": "80px"},
        )
        for index in range(4)
    ]

    button = widgets.Button(
        description=f"📋 {tr('copy_prompt')}",
        tooltip=tr("copy_group_prompt_tooltip"),
        layout=widgets.Layout(width="180px"),
    )

    def reset_button(change):
        button.description = f"📋 {tr('copy_prompt')}"

    for selector in selectors:
        selector.observe(reset_button, names="value")

    def copy_group_prompt(button):
        selected_concepts = [
            selector.value
            for selector in selectors
        ]

        if len(set(selected_concepts)) < 4:
            button.description = (
                f"⚠ {tr('four_distinct_concepts')}"
            )
            return

        selected_pairs = [
            (
                concept_a,
                concept_b,
                similarity_lookup[
                    frozenset((concept_a, concept_b))
                ],
            )
            for concept_a, concept_b in combinations(
                selected_concepts,
                2,
            )
        ]

        prompt = create_group_prompt(
            selected_concepts=selected_concepts,
            selected_pairs=selected_pairs,
            model_name=model_name,
        )

        prompt_js = json.dumps(prompt)

        display(
            Javascript(
                f"""
                navigator.clipboard.writeText(
                    {prompt_js}
                ).then(function() {{
                    console.log("Prompt copied");
                }});
                """
            )
        )

        button.description = "✓ Prompt copié !"

    button.on_click(copy_group_prompt)

    return widgets.VBox([*selectors, button])

def display_semantic_core(
    core_order,
    semantic_strength,
    strength_mode,
):

    """
    Display the progressive semantic-core construction.
    """

    concept_width = max(
        len(str(concept))
        for concept in core_order
    )

    rank_width = len(str(len(core_order)))

    display_feedback(
        title=tr("semantic_core_constructed"),
        details=tr(
            "progressive_order_details",
            count=len(core_order),
        ),
        status="success",
    )
    definition_key = (
        "semantic_strength_definition_relative"
        if strength_mode == "relative"
        else "semantic_strength_definition_comparable"
    )

    print()
    print(
        fill(
            tr(definition_key),
            width=80,
            subsequent_indent="    ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    )
    print()

    print()

    for rank, concept in enumerate(core_order, start=1):
        strength = semantic_strength[concept]
        formatted_strength = format_number(
            strength,
            decimals=3,
        )

        print(
            f"{rank:>{rank_width}} | "
            f"{concept:<{concept_width}} | "
            f"{tr('semantic_strength_short')}: "
            f"{formatted_strength}"
        )

def scenario_feedback_html(scenario):
    """
    Return the loaded-scenario feedback card as HTML.
    """
    title = scenario["title"]
    objects = scenario["objects"]
    n_concepts = len(objects)

    details = (
        f"{title} · "
        f"{tr('concept_count')}: {n_concepts}"
    )

    return feedback_html(
        title=tr("scenario_loaded"),
        details=details,
        status="success",
    )