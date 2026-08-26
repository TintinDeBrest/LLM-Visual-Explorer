# =========================================================
# notebook_setup.py
# Initialisation de l'environnement du notebook
# =========================================================

import importlib.util
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path.cwd().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from explorer.feedback import display_feedback
from explorer.i18n import tr



# ---------------------------------------------------------
# Optional notebook dependencies
# ---------------------------------------------------------

def ensure_package(import_name, package_name):
    """Install a small notebook dependency only when it is missing."""

    if importlib.util.find_spec(import_name) is not None:
        return

    print(f"Installing missing dependency: {package_name}")

    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                package_name,
            ]
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Unable to install the required package: {package_name}"
        ) from error


ensure_package("PIL", "pillow")
ensure_package("kaleido", "kaleido")


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

from explorer.config import MODEL_NAME, MODEL_ALIAS, PLANETARIUM_STRENGTH_MODE

from explorer.dataframe import create_dataframe

from explorer.display import (
    display_model,
    display_projection,
    display_scenario,
    display_semantic_core,
    display_similarity_ranking,
)

from explorer.embeddings import compute_embeddings, get_model
from explorer.exports import save_similarities_csv

from explorer.projections import compute_pca

from explorer.semantic_core import build_semantic_core

from explorer.plotting import (
    plot_scene,
    plot_map,
)

from explorer.report import display_report

from explorer.scenarios import load_scenario, scenario_selector

from explorer.similarities import (
    compute_similarity,
    rank_similarity_pairs,
)

display_feedback(
    title=tr("initialization_completed"),
    details=(
        f"{tr('imports_successful')} · "
        f"{tr('environment_ready')}"
    ),
    status="success",
)