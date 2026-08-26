# ===============================================================
# exports.py
# Fonctions d'export des données d'exploration
# ===============================================================

import csv
from datetime import datetime
from pathlib import Path
from explorer.i18n import tr

def exploration_output_dir(scenario_name, model_alias):
    """Return and create the output directory for an exploration."""

    output_dir = Path("explorations") / scenario_name / model_alias
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir


def save_similarities_csv(
    similarity_pairs,
    scenario_name,
    model_alias,
    model_name,
):
    """
    Save semantic similarity pairs to a CSV file.

    The file is stored locally in:

        explorations/<scenario>/<model_alias>/similarities_<timestamp>.csv

    Parameters
    ----------
    similarity_pairs : list
        List of tuples:
        (concept_a, concept_b, similarity)

    scenario_name : str
        Name of the scenario.

    model_alias : str
        Human-readable model name.

    model_name : str
        Technical model identifier.
    """

    # -----------------------------------------------------------
    # Output path
    # -----------------------------------------------------------

    now = datetime.now()

    exploration_date = now.strftime("%Y-%m-%d")
    exploration_time = now.strftime("%H:%M:%S")
    run_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")

    output_path = (
        exploration_output_dir(scenario_name, model_alias)
        / f"similarities_{run_timestamp}.csv"
    )

    # -----------------------------------------------------------
    # Write CSV
    # -----------------------------------------------------------

    with open(
        output_path,
        "x",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Date",
                "Time",
                "Scenario",
                "Model_Alias",
                "Model_Name",
                "Concept_A",
                "Concept_B",
                "Similarity",
            ]
        )

        for a, b, score in similarity_pairs:

            writer.writerow(
                [
                    exploration_date,
                    exploration_time,
                    scenario_name,
                    model_alias,
                    model_name,
                    a,
                    b,
                    score,
                ]
            )

    print()
    print(f"💾 Similarities saved to:")
    print(f"   {output_path}")

    return output_path


def save_planetarium_png(
    figure,
    scenario_name,
    model_alias,
    width=1600,
    height=1200,
):
    """Save a canonical static PNG of a Plotly planetarium figure."""

    import plotly.graph_objects as go

    # Work on a copy so that the interactive figure keeps the user's
    # current camera, dimensions and text sizes.
    canonical_figure = go.Figure(figure)

    for trace in canonical_figure.data:
        if trace.type != "scatter3d" or trace.mode != "text":
            continue

        texts = list(trace.text) if trace.text is not None else []

        if texts and not all(text == "★" for text in texts):
            trace.textfont.size = 15

    canonical_figure.update_layout(
        margin=dict(l=20, r=20, t=70, b=20),
        title_font=dict(size=22),
        scene_camera=dict(
            eye=dict(x=1.08, y=1.08, z=1.08),
        ),
    )

    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    output_path = (
        exploration_output_dir(scenario_name, model_alias)
        / f"planetarium_{run_timestamp}.png"
    )

    canonical_figure.write_image(
        output_path,
        format="png",
        width=width,
        height=height,
        scale=1,
    )

    return output_path


def create_planetarium_export_button(
    figure,
    scenario_name,
    model_alias,
):
    """Create a notebook button that saves the planetarium on demand."""

    import ipywidgets as widgets

    button = widgets.Button(
        description=f"📷 {tr('save_planetarium')}",
        tooltip=tr("save_planetarium_tooltip"),
        layout=widgets.Layout(width="220px"),
    )

    output = widgets.HTML()


    def export_planetarium(b):
        output.value = ""

        try:
            output_path = save_planetarium_png(
                figure,
                scenario_name,
                model_alias,
            )

        except Exception as error:
            b.description = f"⚠️ {tr('export_failed_short')}"
            output.value = tr("export_failed", error=error)
            return

        b.description = f"✓ {tr('planetarium_saved')}"

        output.value = (
            f"📷 {tr('planetarium_saved_in')}<br>"
            f"&nbsp;&nbsp;&nbsp;{output_path}"
        )


    button.on_click(export_planetarium)

    return widgets.VBox([button, output])
