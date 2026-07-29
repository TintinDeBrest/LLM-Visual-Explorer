#====================================================================
# config.py
# PhL 29jul26
#====================================================================

# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ---------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------

DEFAULT_SCENARIO = "mixte"
DEFAULT_PROJECTION = "PCA"
LANGUAGE = "fr"

# ---------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------

PRESENTATION_MODE = True # Autre DEMO_MODE (# Old : CONFERENCE_MODE = True)

SHOW_AXES = False
SHOW_GRID = False
SHOW_LABELS = False
SHOW_ARROWS = True
SHOW_ICONS = True

CATEGORY_COLORS = {
    "Royal": "royalblue",
    "Humain": "forestgreen",
    "Fruit": "crimson",
    "Animal": "darkorange",
}

