# ============================================================
# Context & Polysemy Explorer
# ============================================================

import numpy as np
import torch
import ipywidgets as widgets
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import cosine_similarity
from IPython.display import display, HTML, clear_output

from explorer import config


MODEL_ID = "sentence-transformers/LaBSE"

_tokenizer = None
_model = None
_device = None


# ============================================================
# Interface translations
# ============================================================

TEXTS = {
    "fr": {
        "word": "Mot :",
        "button": "Explorer le contexte",
        "title": "Contexte et polysémie",
        "model": "Modèle",
        "computing": "Calcul des représentations contextuelles...",
        "prototypes": "Prototypes sémantiques contextuels",
        "prototype_explanation": (
            "À chaque couche, les représentations contextuelles "
            "du mot cible dans les trois phrases d'exemple de "
            "chaque famille sont moyennées pour former un prototype."
        ),
        "initial": "Représentation initiale",
        "layer": "Couche",
        "state_layer": "État / couche",
        "preference": "Préférence contextuelle",
        "equal": "similarité égale",
        "figure_title": "Représentation contextuelle de",
        "hover_preference": "Préférence",
    },

    "en": {
        "word": "Word:",
        "button": "Explore context",
        "title": "Context & Polysemy",
        "model": "Model",
        "computing": "Computing contextual representations...",
        "prototypes": "Contextual semantic prototypes",
        "prototype_explanation": (
            "At each layer, the contextual representations "
            "of the target word in the three example sentences "
            "of each family are averaged to form a prototype."
        ),
        "initial": "Initial representation",
        "layer": "Layer",
        "state_layer": "State / layer",
        "preference": "Contextual preference",
        "equal": "equal similarity",
        "figure_title": "Contextual representation of",
        "hover_preference": "Preference",
    },

    "es": {
        "word": "Palabra:",
        "button": "Explorar contexto",
        "title": "Contexto y polisemia",
        "model": "Modelo",
        "computing": "Calculando representaciones contextuales...",
        "prototypes": "Prototipos semánticos contextuales",
        "prototype_explanation": (
            "En cada capa, las representaciones contextuales "
            "de la palabra objetivo en las tres frases de ejemplo "
            "de cada familia se promedian para formar un prototipo."
        ),
        "initial": "Representación inicial",
        "layer": "Capa",
        "state_layer": "Estado / capa",
        "preference": "Preferencia contextual",
        "equal": "similitud igual",
        "figure_title": "Representación contextual de",
        "hover_preference": "Preferencia",
    },
}


# ============================================================
# Experiments
# ============================================================

EXPERIMENTS = {

    # --------------------------------------------------------
    # French — avocat
    # --------------------------------------------------------

    "avocat": {
        "word": "avocat",

        "contexts": {
            "⚖️ Justice":
                "L'avocat plaide devant le tribunal.",

            "🥑 Cuisine":
                "Elle ajoute de l'avocat dans la salade.",
        },

        "prototypes": {
            "⚖️ Juridique": [
                "L'avocat défend son client.",
                "Cet avocat prépare le procès.",
                "L'avocat conseille la défense.",
            ],

            "🥑 Alimentaire": [
                "Cet avocat est bien mûr.",
                "Je prépare un guacamole avec l'avocat.",
                "Elle coupe l'avocat pour le déjeuner.",
            ],
        },
    },

    # --------------------------------------------------------
    # English — mouse
    # --------------------------------------------------------

    "mouse": {
        "word": "mouse",

        "contexts": {
            "🐭 Animal":
                "The mouse ran across the floor.",

            "🖱️ Computer":
                "She clicked the icon with the mouse.",
        },

        "prototypes": {
            "🐭 Animal": [
                "A small mouse ran through the house.",
                "The cat chased the mouse.",
                "The mouse hid under the table.",
            ],

            "🖱️ Computer": [
                "She moved the pointer with the mouse.",
                "This wireless mouse connects to the computer.",
                "He used the mouse to select the file.",
            ],
        },
    },

    # --------------------------------------------------------
    # Spanish — banco
    # --------------------------------------------------------

    "banco": {
        "word": "banco",

        "contexts": {
            "🏦 Finanzas":
                "Fui al banco para sacar dinero.",

            "🪑 Parque":
                "Me senté en un banco del parque.",
        },

        "prototypes": {
            "🏦 Financiero": [
                "El banco presta dinero a sus clientes.",
                "Deposité mis ahorros en el banco.",
                "El banco aprobó el préstamo.",
            ],

            "🪑 Asiento": [
                "Un anciano descansaba en un banco de la plaza.",
                "El banco de madera está junto al árbol.",
                "Nos sentamos juntos en un banco.",
            ],
        },
    },
}


# ============================================================
# Model loading
# ============================================================

def _load_model():
    """Load LaBSE once and keep it cached."""

    global _tokenizer, _model, _device

    if _model is not None:
        return

    _device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    _tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        use_fast=True,
    )

    _model = AutoModel.from_pretrained(
        MODEL_ID
    ).to(_device)

    _model.eval()


# ============================================================
# Target word location
# ============================================================

def _prepare(sentence, word):
    """Tokenize a sentence and locate the target word tokens."""

    encoded = _tokenizer(
        sentence,
        return_tensors="pt",
        return_offsets_mapping=True,
    )

    offsets = encoded.pop(
        "offset_mapping"
    )[0].tolist()

    start = sentence.lower().index(
        word.lower()
    )

    end = start + len(word)

    indices = [
        i
        for i, (a, b) in enumerate(offsets)
        if b > start and a < end
    ]

    if not indices:
        raise ValueError(
            f"The word {word!r} was not found."
        )

    return encoded, indices


# ============================================================
# Contextual trajectory
# ============================================================

def _contextual_trajectory(sentence, word):
    """Return the target representation at every model state."""

    encoded, indices = _prepare(
        sentence,
        word,
    )

    inputs = {
        name: value.to(_device)
        for name, value in encoded.items()
    }

    with torch.inference_mode():

        output = _model(
            **inputs,
            output_hidden_states=True,
            return_dict=True,
        )

    # Initial representation + one vector after each
    # Transformer layer. If the target spans several
    # tokens, their representations are averaged.

    trajectory = torch.stack([
        state[0, indices, :]
        .mean(dim=0)
        .cpu()

        for state in output.hidden_states
    ])

    return trajectory


# ============================================================
# Experiment computation
# ============================================================

def _compute_experiment(experiment):
    """Compute contextual trajectories and semantic preference."""

    word = experiment["word"]
    contexts = experiment["contexts"]
    prototypes = experiment["prototypes"]

    # Context trajectories

    trajectories = {
        context_name:
            _contextual_trajectory(
                sentence,
                word,
            )

        for context_name, sentence
        in contexts.items()
    }

    # Contextual semantic prototypes:
    # average of three target-word trajectories
    # belonging to the same semantic family.

    prototype_states = {
        family:
            torch.stack([
                _contextual_trajectory(
                    sentence,
                    word,
                )

                for sentence in examples
            ]).mean(dim=0)

        for family, examples
        in prototypes.items()
    }

    # Similarity to both prototypes at every layer.

    scores = {
        context_name: {
            family:
                cosine_similarity(
                    trajectory,
                    prototype,
                    dim=1,
                ).numpy()

            for family, prototype
            in prototype_states.items()
        }

        for context_name, trajectory
        in trajectories.items()
    }

    prototype_names = list(
        prototypes.keys()
    )

    positive_family = prototype_names[0]
    negative_family = prototype_names[1]

    # Contextual preference =
    # similarity to first prototype
    # minus similarity to second prototype.

    preferences = {
        context_name:
            context_scores[positive_family]
            - context_scores[negative_family]

        for context_name, context_scores
        in scores.items()
    }

    return {
        "scores": scores,
        "preferences": preferences,
        "positive_family": positive_family,
        "negative_family": negative_family,
    }


# ============================================================
# Prototype display
# ============================================================

def _display_prototypes(
    experiment,
    texts,
):
    """Display the sentences used to construct the prototypes."""

    prototypes = experiment["prototypes"]

    prototype_names = list(
        prototypes.keys()
    )

    left_family = prototype_names[0]
    right_family = prototype_names[1]

    left_examples = "".join(
        f"<li>{sentence}</li>"
        for sentence in prototypes[left_family]
    )

    right_examples = "".join(
        f"<li>{sentence}</li>"
        for sentence in prototypes[right_family]
    )

    display(
        HTML(
            f"""
            <div style="
                margin-top: 18px;
                margin-bottom: 22px;
            ">

                <h4>
                    {texts["prototypes"]}
                </h4>

                <p>
                    {texts["prototype_explanation"]}
                </p>

                <div style="
                    display: flex;
                    gap: 50px;
                ">

                    <div style="flex: 1;">
                        <b>{left_family}</b>
                        <ul>
                            {left_examples}
                        </ul>
                    </div>

                    <div style="flex: 1;">
                        <b>{right_family}</b>
                        <ul>
                            {right_examples}
                        </ul>
                    </div>

                </div>

            </div>
            """
        )
    )


# ============================================================
# Plot
# ============================================================

def _plot_experiment(
    experiment,
    result,
    texts,
):
    """Plot contextual semantic preference layer by layer."""

    contexts = list(
        experiment["contexts"].keys()
    )

    positive_family = result[
        "positive_family"
    ]

    negative_family = result[
        "negative_family"
    ]

    scores = result["scores"]
    preferences = result["preferences"]

    state_count = len(
        next(iter(preferences.values()))
    )

    layers = np.arange(
        state_count
    )

    layer_labels = np.array(
        [texts["initial"]]
        + [
            f'{texts["layer"]} {i}'
            for i in range(1, state_count)
        ]
    )

    # Shared semantic-preference scale

    ymin = -0.35
    ymax = 0.35
    margin = 0.05

    fig = make_subplots(
        rows=1,
        cols=2,

        subplot_titles=[
            experiment["contexts"][context]
            for context in contexts
        ],
    )

    # One context per subplot

    for col, context in enumerate(
        contexts,
        start=1,
    ):

        hover = [
            [
                layer_labels[i],
                scores[context][positive_family][i],
                scores[context][negative_family][i],
            ]

            for i in layers
        ]

        fig.add_trace(
            go.Scatter(
                x=layers,
                y=preferences[context],

                mode="lines+markers",

                showlegend=False,

                marker=dict(
                    size=8
                ),

                line=dict(
                    width=3
                ),

                customdata=hover,

                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    + f"{positive_family}="
                    "%{customdata[1]:.4f}<br>"
                    + f"{negative_family}="
                    "%{customdata[2]:.4f}<br>"
                    + f'{texts["hover_preference"]}='
                    "%{y:+.4f}"
                    + "<extra></extra>"
                ),
            ),

            row=1,
            col=col,
        )

        fig.add_hline(
            y=0,
            line_dash="dot",
            line_width=1,
            row=1,
            col=col,
        )

    # Axes

    fig.update_xaxes(
        title_text=texts["state_layer"],
        dtick=1,
    )

    fig.update_yaxes(
        title_text=texts["preference"],
        range=[ymin, ymax],
        col=1,
    )

    fig.update_yaxes(
        range=[ymin, ymax],
        matches="y",
        col=2,
    )

    # Semantic zones

    for col in (1, 2):

        xref = (
            "x domain"
            if col == 1
            else "x2 domain"
        )

        yref = (
            "y"
            if col == 1
            else "y2"
        )

        fig.add_annotation(
            x=0.02,
            y=ymax - margin * 0.25,
            xref=xref,
            yref=yref,
            text=f"↑ {positive_family}",
            showarrow=False,
            xanchor="left",
            font=dict(size=13),
        )

        fig.add_annotation(
            x=0.02,
            y=ymin + margin * 0.25,
            xref=xref,
            yref=yref,
            text=f"↓ {negative_family}",
            showarrow=False,
            xanchor="left",
            font=dict(size=13),
        )

        fig.add_annotation(
            x=0.98,
            y=0,
            xref=xref,
            yref=yref,
            text=texts["equal"],
            showarrow=False,
            xanchor="right",
            yshift=10,
            font=dict(size=11),
        )

    fig.update_layout(
        template="plotly_white",

        height=540,
        autosize=True,

        title=(
            f'{texts["figure_title"]} '
            f'“{experiment["word"]}”'
        ),

        margin=dict(
            l=80,
            r=40,
            t=100,
            b=70,
        ),
    )

    display(fig)


# ============================================================
# Public UI
# ============================================================

def context_explorer(language=None):
    """Display the interactive Context & Polysemy explorer."""

    language = (
        language
        or config.INTERFACE_LANGUAGE
        or "en"
    ).lower()

    if language not in TEXTS:
        language = "en"

    texts = TEXTS[language]

    word_dropdown = widgets.Dropdown(
        options=[
            ("🇫🇷 avocat", "avocat"),
            ("🇬🇧 mouse", "mouse"),
            ("🇪🇸 banco", "banco"),
        ],

        value="avocat",
        description=texts["word"],

        layout=widgets.Layout(
            width="350px"
        ),
    )

    explore_button = widgets.Button(
        description=texts["button"],
        button_style="primary",

        layout=widgets.Layout(
            width="190px"
        ),
    )

    output = widgets.Output()

    def show_context_experiment(_=None):

        experiment = EXPERIMENTS[
            word_dropdown.value
        ]

        with output:

            clear_output(
                wait=True
            )

            display(
                HTML(
                    f"""
                    <h4>
                        🧠 {texts["title"]}
                        — {experiment["word"]}
                    </h4>

                    <p>
                        <b>{texts["model"]}:</b> LaBSE
                    </p>

                    <p>
                        <i>
                            {texts["computing"]}
                        </i>
                    </p>
                    """
                )
            )

        _load_model()

        result = _compute_experiment(
            experiment
        )

        with output:

            clear_output(
                wait=True
            )

            display(
                HTML(
                    f"""
                    <h4>
                        🧠 {texts["title"]}
                        — {experiment["word"]}
                    </h4>

                    <p>
                        <b>{texts["model"]}:</b> LaBSE
                    </p>
                    """
                )
            )

            _display_prototypes(
                experiment,
                texts,
            )

            _plot_experiment(
                experiment,
                result,
                texts,
            )

    explore_button.on_click(
        show_context_experiment
    )

    display(
        widgets.VBox([
            word_dropdown,
            explore_button,
            output,
        ])
    )