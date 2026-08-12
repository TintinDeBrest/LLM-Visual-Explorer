# ===================================================================
#   scenarios.py
# ===================================================================
from pathlib import Path
import yaml
import ipywidgets as widgets
from IPython.display import display

SCENARIOS_DIR = Path(__file__).parent / "scenarios"


def load_scenario(name: str):
    """
    Charge un scénario YAML et retourne ses données sous forme de dictionnaire
    """
    filename = SCENARIOS_DIR / f"{name}.yaml"

    if not filename.exists():
        raise FileNotFoundError(filename)

    with open(filename, "r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)

    return scenario


def scenario_selector(display_function, selection):
    """
    Affiche le sélecteur de scénario et charge le scénario choisi.
    """

    scenario_files = sorted(SCENARIOS_DIR.glob("*.yaml"))

    label_choose = widgets.Label(value="1 Choisir le scénario")

    scenario_dropdown = widgets.Dropdown(
        options=[f.stem for f in scenario_files],
        value="super_scenario",
        description="",
    )

    row_choose = widgets.HBox([label_choose, scenario_dropdown])

    button_load = widgets.Button(description="2 Charger le scénario")

    output = widgets.Output()

    def load_selected_scenario(b):

        selection["scenario_name"] = scenario_dropdown.value

        selection["scenario"] = load_scenario(selection["scenario_name"])

        selection["concepts"] = [
            obj["name"] for obj in selection["scenario"]["objects"]
        ]

        selection["objects"] = selection["scenario"]["objects"]

        selection["icons"] = {
            obj["name"]: obj.get("emoji", "") for obj in selection["objects"]
        }

        with output:
            output.clear_output()
            print("Scénario chargé :", selection["scenario_name"])
            print("Nombre de concepts :", len(selection["concepts"]))

            display_function(selection["scenario"])

    button_load.on_click(load_selected_scenario)

    display(row_choose, button_load, output)
