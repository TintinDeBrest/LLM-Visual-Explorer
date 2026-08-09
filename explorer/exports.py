# ===============================================================
# exports.py
# Fonctions d'export des données expérimentales
# ===============================================================

import csv
from datetime import datetime
from pathlib import Path


def save_similarities_csv(
    similarity_pairs,
    scenario_name,
    model_alias,
    model_name,
):
    """
    Save semantic similarity pairs to a CSV file.

    The file is stored locally in:

        experiments/<scenario>/<model_alias>/similarities.csv

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

    output_path = Path("experiments") / scenario_name / model_alias / "similarities.csv"

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------------------------
    # Experiment timestamp
    # -----------------------------------------------------------

    now = datetime.now()

    experiment_date = now.strftime("%Y-%m-%d")
    experiment_time = now.strftime("%H:%M:%S")

    # -----------------------------------------------------------
    # Write CSV
    # -----------------------------------------------------------

    with open(
        output_path,
        "w",
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
                    experiment_date,
                    experiment_time,
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
