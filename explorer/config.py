# ====================================================================
# config.py
# PhL 07Aug26
# ====================================================================

# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

# MiniLM
MODEL_ALIAS = "MiniLM"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# BERT
# MODEL_ALIAS = "BERT"
# MODEL_NAME = "sentence-transformers/bert-base-nli-mean-tokens"

# MPNet
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


# Pour test cluster
CLUSTER_C1 = [
    "Chat",
    "Chien",
    "Coq",
    "Loup",
]
