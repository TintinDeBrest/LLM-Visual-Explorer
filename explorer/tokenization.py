# ============================================================
# Tokenization Explorer
# ============================================================

import base64
import html

from pathlib import Path

import ipywidgets as widgets

from IPython.display import display, HTML, clear_output
from transformers import AutoTokenizer

from explorer import config
from explorer.i18n import tr


# ============================================================
# LlmExpl logo
# ============================================================

LOGO_PATH = (
    Path(__file__).resolve().parent.parent
    / "images"
    / "LlmExpl_logo.png"
)

LOGO_DATA_URI = (
    "data:image/png;base64,"
    + base64.b64encode(
        LOGO_PATH.read_bytes()
    ).decode("ascii")
)

# ============================================================
# Models available for tokenization
# ============================================================

TOKENIZER_MODELS = {
    "MiniLM":
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",

    "MPNet":
        "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",

    "BERT":
        "sentence-transformers/bert-base-nli-mean-tokens",

    "LaBSE":
        "sentence-transformers/LaBSE",
}


# ============================================================
# Tokenizer cache
# ============================================================

_tokenizer_cache = {}


def _get_tokenizer(alias):
    """Load each tokenizer only once."""

    if alias not in _tokenizer_cache:

        model_name = TOKENIZER_MODELS[
            alias
        ]

        _tokenizer_cache[alias] = (
            AutoTokenizer.from_pretrained(
                model_name,
                use_fast=True,
            )
        )

    return _tokenizer_cache[alias]


# ============================================================
# Comparative tokenization table
# ============================================================

TOKENIZATION_EXAMPLES = [
    "crocodile",
    "alligator",
    "wolf",
    "coyote",
    "dog",
    "blueberries",
]

def display_tokenization_comparison(words=None):
    """Compare selected words across all available tokenizers."""

    words = words or TOKENIZATION_EXAMPLES

    header_cells = "".join(
        f"<th>{html.escape(alias)}</th>"
        for alias in TOKENIZER_MODELS
    )

    table_rows = []

    for word in words:
        token_cells = []

        for alias in TOKENIZER_MODELS:
            tokenizer = _get_tokenizer(alias)
            tokens = tokenizer.tokenize(word)

            formatted_tokens = " · ".join(
                html.escape(token)
                for token in tokens
            )

            token_cells.append(
                f"""
                <td>
                    <code>{formatted_tokens}</code>

                    <div class="token-count">
                        {len(tokens)}
                        {"token" if len(tokens) == 1 else "tokens"}
                    </div>
                </td>
                """
            )

        table_rows.append(
            f"""
            <tr>
                <th class="concept-cell">
                    {html.escape(word)}
                </th>

                {"".join(token_cells)}
            </tr>
            """
        )

    display(
        HTML(
            f"""
            <style>
                .tokenization-comparison {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 12px;
                    margin-bottom: 10px;
                    font-size: 0.94em;
                }}

                .tokenization-comparison th,
                .tokenization-comparison td {{
                    border: 1px solid #d9dee7;
                    padding: 10px 12px;
                    text-align: left;
                    vertical-align: top;
                }}

                .tokenization-comparison thead th {{
                    background: #eef3f8;
                    text-align: center;
                }}

                .tokenization-comparison .concept-cell {{
                    background: #f7f9fb;
                    white-space: nowrap;
                }}

                .tokenization-comparison code {{
                    white-space: normal;
                    overflow-wrap: anywhere;
                }}

                .tokenization-comparison .token-count {{
                    margin-top: 5px;
                    color: #6b7280;
                    font-size: 0.82em;
                }}
            </style>

            <div>
                <h3 style="
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <img
                        src="{LOGO_DATA_URI}"
                        alt="LlmExpl"
                        style="
                            height: 42px;
                            width: auto;
                            object-fit: contain;
                        "
                    >

                    <span>
                        {tr("tokenization_comparison_title")}
                    </span>
                </h3>

                <p>
                    {tr("tokenization_comparison_intro")}
                </p>

                <table class="tokenization-comparison">
                    <thead>
                        <tr>
                            <th>
                                {tr("tokenization_concept")}
                            </th>

                            {header_cells}
                        </tr>
                    </thead>

                    <tbody>
                        {"".join(table_rows)}
                    </tbody>
                </table>

                <p style="
                    color: #5f6670;
                    font-size: 0.90em;
                    margin-top: 8px;
                ">
                    <b>▁ / ##</b>
                    —
                    {tr("tokenization_marker_note")}
                </p>
            </div>
            """
        )
    )


# ============================================================
# Public UI
# ============================================================

def tokenization_explorer(
    default_model="MiniLM",
    default_text="crocodile",
):
    """Display the interactive tokenization explorer."""


    model_dropdown = widgets.Dropdown(
        options=list(
            TOKENIZER_MODELS.keys()
        ),
        value=default_model,
        description=tr("tokenization_model"),
        layout=widgets.Layout(
            width="450px"
        ),
    )

    text_input = widgets.Text(
        value=default_text,
        description=tr("tokenization_text"),
        placeholder=tr("tokenization_placeholder"),
        layout=widgets.Layout(
            width="450px"
        ),
    )

    tokenize_button = widgets.Button(
        description=tr("tokenization_button"),
        button_style="primary",
        layout=widgets.Layout(
            width="150px"
        ),
    )

    output = widgets.Output()

    def show_tokenization(_=None):

        alias = model_dropdown.value
        text = text_input.value.strip()

        with output:

            clear_output(
                wait=True
            )

            if not text:

                display(
                    HTML(
                        f'<i>{tr("tokenization_empty")}</i>'
                    )
                )

                return

            tokenizer = _get_tokenizer(
                alias
            )

            tokens = tokenizer.tokenize(
                text
            )

            token_display = (
                " &nbsp; | &nbsp; ".join(
                    f"<code>{html.escape(token)}</code>"
                    for token in tokens
                )
            )

            safe_text = html.escape(
                text
            )


            display(
                HTML(
                    f"""
                    <div style="margin-top: 12px;">

                        <h4 style="
                            display: flex;
                            align-items: center;
                            gap: 9px;
                        ">
                            <img
                                src="{LOGO_DATA_URI}"
                                alt="LlmExpl"
                                style="
                                    height: 38px;
                                    width: auto;
                                    object-fit: contain;
                                "
                            >
                            <span>
                                {tr("tokenization_title")} — {alias}
                            </span>
                        </h4>

                        <p>
                            <b>{tr("tokenization_text")}:</b>
                            {safe_text}<br>

                            <b>{tr("tokenization_token_count")}:</b>
                            {len(tokens)}
                        </p>

                        <p>
                            <b>{tr("tokenization_tokens")}:</b><br>
                            {token_display}
                        </p>

                        <p style="margin-top: 16px;">
                            <b>{tr("tokenization_word_not_token")}</b><br>

                            <span style="font-size: 0.95em;">
                                {tr("tokenization_explanation")}
                            </span>
                        </p>

                    </div>
                    """
                )
            )


    tokenize_button.on_click(
        show_tokenization
    )

    # Transition between observation and free experimentation.
    display(
        HTML(
            f"""
            <h3 style="
                margin-top: 28px;
                margin-bottom: 16px;
            ">
                🧪 {tr("tokenization_experiment_title")}
            </h3>
            """
        )
    )

    display(
        widgets.VBox([
            model_dropdown,
            text_input,
            tokenize_button,
            output,
        ])
    )

    # Show the default example immediately.
    show_tokenization()
