# ============================================================
# Tokenization Explorer
# ============================================================

import html

import ipywidgets as widgets

from IPython.display import display, HTML, clear_output
from transformers import AutoTokenizer

from explorer.config import INTERFACE_LANGUAGE


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
# Interface translations
# ============================================================

TEXTS = {
    "fr": {
        "model": "Modèle :",
        "text": "Texte :",
        "placeholder": "Écrivez un mot ou un texte court...",
        "button": "Tokeniser",
        "empty": "Écrivez un mot ou un texte court.",
        "title": "Tokenisation",
        "token_count": "Nombre de tokens",
        "tokens": "Tokens",
        "word_token": "MOT ≠ TOKEN",
        "explanation": (
            "Un token peut être un mot, "
            "une partie d'un mot, "
            "un caractère ou un signe."
        ),
    },

    "en": {
        "model": "Model:",
        "text": "Text:",
        "placeholder": "Enter a word or a short text...",
        "button": "Tokenize",
        "empty": "Enter a word or a short text.",
        "title": "Tokenization",
        "token_count": "Number of tokens",
        "tokens": "Tokens",
        "word_token": "WORD ≠ TOKEN",
        "explanation": (
            "A token can be a word, "
            "part of a word, "
            "a character or a symbol."
        ),
    },

    "es": {
        "model": "Modelo:",
        "text": "Texto:",
        "placeholder": "Escribe una palabra o un texto breve...",
        "button": "Tokenizar",
        "empty": "Escribe una palabra o un texto breve.",
        "title": "Tokenización",
        "token_count": "Número de tokens",
        "tokens": "Tokens",
        "word_token": "PALABRA ≠ TOKEN",
        "explanation": (
            "Un token puede ser una palabra, "
            "una parte de una palabra, "
            "un carácter o un signo."
        ),
    },
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
# Public UI
# ============================================================

def tokenization_explorer(
    language=None,
    default_model="MiniLM",
    default_text="cocodrilo",
):
    """Display the interactive tokenization explorer."""

    language = (
        language
        or INTERFACE_LANGUAGE
        or "en"
    ).lower()

    if language not in TEXTS:
        language = "en"

    texts = TEXTS[language]

    model_dropdown = widgets.Dropdown(
        options=list(
            TOKENIZER_MODELS.keys()
        ),
        value=default_model,
        description=texts["model"],
        layout=widgets.Layout(
            width="450px"
        ),
    )

    text_input = widgets.Text(
        value=default_text,
        description=texts["text"],
        placeholder=texts["placeholder"],
        layout=widgets.Layout(
            width="450px"
        ),
    )

    tokenize_button = widgets.Button(
        description=texts["button"],
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
                        f'<i>{texts["empty"]}</i>'
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

                        <h4>
                            🔤 {texts["title"]} — {alias}
                        </h4>

                        <p>
                            <b>{texts["text"]}</b>
                            {safe_text}<br>

                            <b>{texts["token_count"]}:</b>
                            {len(tokens)}
                        </p>

                        <p>
                            <b>{texts["tokens"]}:</b><br>
                            {token_display}
                        </p>

                        <p style="margin-top: 16px;">
                            <b>{texts["word_token"]}</b><br>

                            <span style="
                                font-size: 0.95em;
                            ">
                                {texts["explanation"]}
                            </span>
                        </p>

                    </div>
                    """
                )
            )

    tokenize_button.on_click(
        show_tokenization
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