# ====================================================================
# config.py
# ====================================================================

# ---------------------------------------------------------------------
# Former experimental models — kept for reference
# ---------------------------------------------------------------------

# Petit modèle génératif — état interne utilisé avant la prédiction suivante
# MODEL_ALIAS = "PMG"
# MODEL_NAME = "Qwen/Qwen2.5-0.5B"
# MODEL_TYPE = "generative"
# REPRESENTATION_MODE = "common_suffix_middle_delta"
# PREDICTIVE_STATE_SUFFIX = "\n:"


# GPT-2 — essai exploratoire avec mean pooling, centrage par scénario
# et normalisation. Modèle génératif anglais, non spécialisé dans les
# embeddings de phrases.
# MODEL_ALIAS = "GPT-2 mean pooling + centering"
# MODEL_NAME = "openai-community/gpt2"
# MODEL_TYPE = "embedding"
# REPRESENTATION_MODE = "mean_pooling_centered"
# PREDICTIVE_STATE_SUFFIX = ""

# ---------------------------------------------------------------------
# Model profiles
# ---------------------------------------------------------------------

MODEL_PROFILES = {
    "MiniLM": {
        "alias": "MiniLM",
        "name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "type": "embedding",
        "representation_mode": "sentence_embedding",
        "predictive_state_suffix": "",
    },

    "MPNet": {
        "alias": "MPNet",
        "name": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        "type": "embedding",
        "representation_mode": "sentence_embedding",
        "predictive_state_suffix": "",
    },

    "BERT": {
        "alias": "BERT",
        "name": "sentence-transformers/bert-base-nli-mean-tokens",
        "type": "embedding",
        "representation_mode": "sentence_embedding",
        "predictive_state_suffix": "",
    },

    "LaBSE": {
        "alias": "LaBSE",
        "name": "sentence-transformers/LaBSE",
        "type": "embedding",
        "representation_mode": "sentence_embedding",
        "predictive_state_suffix": "",
    },
}


# ---------------------------------------------------------------------
# Active model
# ---------------------------------------------------------------------

ACTIVE_MODEL = "MiniLM"


def get_model_config():
    """Return the configuration of the currently selected model."""
    return MODEL_PROFILES[ACTIVE_MODEL]


# ---------------------------------------------------------------------
# Backward-compatible constants
# ---------------------------------------------------------------------

_model_config = get_model_config()

MODEL_ALIAS = _model_config["alias"]
MODEL_NAME = _model_config["name"]
MODEL_TYPE = _model_config["type"]
REPRESENTATION_MODE = _model_config["representation_mode"]
PREDICTIVE_STATE_SUFFIX = _model_config["predictive_state_suffix"]

# ---------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------

DEFAULT_SCENARIO = "super_scenario_en"
DEFAULT_PROJECTION = "PCA"

# Scenario language filter: "all", "fr", "en", or "es"
SCENARIO_LANGUAGE = "all"

# Interface language: "fr", "en", or "es"
INTERFACE_LANGUAGE = "es"

# ---------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------

PRESENTATION_MODE = True  # Autre DEMO_MODE (# Old : CONFERENCE_MODE = True)

SHOW_AXES = False
SHOW_GRID = False
SHOW_LABELS = False
SHOW_ARROWS = False
SHOW_ICONS = True

# Planetarium: "relative" maximise le contraste dans un scénario ;
# "comparable" conserve les forces absolues pour comparer des scénarios.
PLANETARIUM_STRENGTH_MODE = "relative"


