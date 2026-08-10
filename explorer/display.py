# Display pour tous les affichages du notebook
# ===============================================

import numpy as np

from explorer.config import MODEL_ALIAS, MODEL_NAME


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

    print("Modèle :")
    print(f"Nom Générique: {MODEL_ALIAS}")
    print()

    print("Dimension des embeddings :")
    print(f"  {model.get_embedding_dimension()}")

    print()


def display_projection(pca):
    """
    Affiche l'information conservée par la projection 3D.

    Parameters
    ----------
    pca : PCA
        Objet PCA utilisé pour la projection.
    """

    explained_variance = pca.explained_variance_ratio_.sum() * 100

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

    print()
    print("=" * 80)
    print("🔗 SEMANTIC SIMILARITY vs 3D PROJECTION DISTANCE")
    print("=" * 80)
    print()

    print("Seuils indicatifs:")
    print("🟢 60–100 %   Similarité élevée")
    print("🟡 30–59 %    Similarité moyenne")
    print("🔴 0–29 %     Similarité faible")
    print()
    print(
        "NB: L'échelle des similarités dépend du modèle. Les valeurs sont "
        "surtout comparables à l'intérieur d'un même modèle; le classement "
        "est plus significatif que la valeur absolue."
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
            f"{emoji_a} {a:<12} ↔ "
            f"{emoji_b} {b:<12} "
            f"{bar:<20} "
            f"Sim: {score:.0%}  "
            f"Dist: {distance_3d:.1f}"
        )

    # ---------------------------------------------------
    # TOP semantic neighbours
    # ---------------------------------------------------

    print("🟢 Les " f"{top_n} voisins sémantiques")

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
        print(f"              ⋮ {hidden} paires intermédiaires masquées ⋮")
        print("-" * 80)
        print()

    # ---------------------------------------------------
    # BOTTOM semantic antipodes
    # ---------------------------------------------------

    print(f"🔴 Les {bottom_n} antipodes sémantiques")

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


def create_prompt_button(concept1, concept2, relation):
    """
    Create a button that copies a ready-to-use LLM prompt
    to the user's clipboard.
    """

    import ipywidgets as widgets
    from IPython.display import display, HTML
    from IPython.display import Javascript

    prompt = f"""Bonjour,

Un modèle d'intelligence artificielle représentant les concepts dans un
espace vectoriel sémantique considère que les deux concepts suivants sont
{relation} :

{concept1} et {concept2}

Je voudrais savoir si vous considérez, à priori, que cette relation est pertinente.

Pouvez-vous fournir :
- des arguments en faveur de cette proximité ou de cet éloignement ;
- des exemples concrets illustrant votre analyse ;
- des nuances ou contre-arguments éventuels ?

L'objectif est de mieux comprendre pourquoi ces deux concepts peuvent être
associés (ou séparés) dans un espace sémantique.
"""

    button = widgets.Button(
        description="📋 Copier le prompt",
        tooltip="Copier le prompt pour cette paire",
        layout=widgets.Layout(width="160px"),
    )

    def copy_prompt(button):
        # Échapper les caractères pour JavaScript
        import json

        prompt_js = json.dumps(prompt)

        display(Javascript(f"""
            navigator.clipboard.writeText({prompt_js}).then(function() {{
                console.log("Prompt copied");
            }});
            """))

        button.description = "✓ Prompt copié !"

    button.on_click(copy_prompt)

    return button


def create_pair_selector(similarity_pairs):
    """
    Create a dropdown allowing the user to select any
    concept pair and copy its corresponding LLM prompt.
    """

    import ipywidgets as widgets
    from IPython.display import display
    import json

    # Create the list displayed in the dropdown
    options = [
        (f"{pair[0]} ↔ {pair[1]} — {pair[2]:.0%}", pair) for pair in similarity_pairs
    ]

    selector = widgets.Dropdown(
        options=options, description="", layout=widgets.Layout(width="300px")
    )

    button = widgets.Button(
        description="📋 Copier le prompt",
        tooltip="Copier le prompt pour cette paire",
        layout=widgets.Layout(width="160px"),
    )

    def copy_selected_prompt(button):
        pair = selector.value

        prompt = f"""Bonjour,

Un modèle d'intelligence artificielle représentant les concepts dans un
espace vectoriel sémantique considère que les deux concepts suivants sont
proches/éloignés :

{pair[0]} et {pair[1]}

Je voudrais savoir si vous considérez, à priori, que cette relation est pertinente.

Pouvez-vous fournir :
- des arguments en faveur de cette proximité ou de cet éloignement ;
- des exemples concrets illustrant votre analyse ;
- des nuances ou contre-arguments éventuels ?

L'objectif est de mieux comprendre pourquoi ces deux concepts peuvent être
associés (ou séparés) dans un espace sémantique.
"""

        prompt_js = json.dumps(prompt)

        display(__import__("IPython").display.Javascript(f"""
                navigator.clipboard.writeText({prompt_js});
                """))

        button.description = "✓ Prompt copié !"

    button.on_click(copy_selected_prompt)

    return widgets.VBox([selector, button])
