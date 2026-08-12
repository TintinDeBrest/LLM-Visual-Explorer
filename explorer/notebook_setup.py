# =========================================================
# notebook_setup.py
# Initialisation de l'environnement du notebook
# =========================================================

import sys
from pathlib import Path

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path.cwd().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print(f"Project root: {PROJECT_ROOT}")


# ---------------------------------------------------------
# External libraries
# ---------------------------------------------------------

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------
# LLM Visual Explorer modules
# ---------------------------------------------------------

from explorer.config import MODEL_NAME, MODEL_ALIAS

from explorer.dataframe import create_dataframe

from explorer.display import (
    display_model,
    display_projection,
    display_scenario,
    display_similarity_ranking,
)

from explorer.embeddings import compute_embeddings, get_model
from explorer.exports import save_similarities_csv

from explorer.projections import compute_pca

from explorer.plotting import (
    plot_scene,
    plot_map,
)

from explorer.report import display_report

from explorer.scenarios import load_scenario

from explorer.similarities import (
    compute_similarity,
    rank_similarity_pairs,
)
