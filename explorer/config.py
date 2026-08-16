# ====================================================================
# config.py
# PhL 07Aug26
# ====================================================================

# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

# MiniLM multilingue
# MODEL_ALIAS = "MiniLM"
# MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# GPT-2 — essai exploratoire avec mean pooling, centrage par scénario
# et normalisation. Modèle génératif anglais, non spécialisé dans les
# embeddings de phrases.
# MODEL_ALIAS = "GPT-2 mean pooling + centering"
# MODEL_NAME = "openai-community/gpt2"

# BERT
MODEL_ALIAS = "BERT"
MODEL_NAME = "sentence-transformers/bert-base-nli-mean-tokens"

# MPNet multilingue, présenté simplement comme "MPNet" dans LlmExpl.
# MODEL_ALIAS = "MPNet"
# MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

# ---------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------

DEFAULT_SCENARIO = "animals"
DEFAULT_PROJECTION = "PCA"
LANGUAGE = "fr"

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
PLANETARIUM_STRENGTH_MODE = "comparable"


# Pour test cluster
CLUSTER_C1 = [
    "Chat",
    "Chien",
    "Coq",
    "Loup",
]
