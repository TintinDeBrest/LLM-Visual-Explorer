# ===================================================================
#   scenarios.py
# ===================================================================
from pathlib import Path
from html import escape
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


def object_icon(obj):
    """Return the current emoji field or the legacy icon field."""

    return obj.get("emoji", obj.get("icon", ""))


def scenario_preview_html(scenario):
    """Create a compact visual preview of a scenario's concepts."""

    concepts = "<br>".join(
        f"{escape(str(object_icon(obj)))} &nbsp; {escape(str(obj['name']))}"
        for obj in scenario["objects"]
    )

    return f"""
    <div style="background: white; color: #161616; font-family: monospace;
                font-size: 16px; line-height: 1.45; padding: 14px 18px;">
        <div style="font-family: sans-serif; font-size: 18px; font-weight: 600;">
            {escape(str(scenario['title']))}
        </div>
        <div style="font-family: sans-serif; font-size: 13px; margin: 4px 0 10px;">
            {escape(str(scenario['description']))}
        </div>
        {concepts}
    </div>
    """


def scenario_selector(display_function, selection):
    """
    Affiche le sélecteur de scénario et charge le scénario choisi.
    """
    # --- Réglages d'interface du sélecteur ---
    #
    #   <-------- LEFT_WIDTH -------->
    #
    #   ┌──────────────────────┐     <--- PREVIEW_MARGIN --->  ┌──────────────────────────────┐
    #   │ 1 Choisir scénario   │                               │ Aperçu du scénario           │
    #   │ ┌──────────────────┐ │                               │                              │
    #   │ │ scénario       ▼ │ │                               │ Titre                        │
    #   │ └──────────────────┘ │                               │ Description                  │
    #   │   DROPDOWN_WIDTH     │                               │ 🐱 Chat                      │
    #   │                      │                               │ 🐶 Chien                     │
    #   │ [2 Charger scénario] │                               │ 🦁 Lion                      │
    #   └──────────────────────┘                               └──────────────────────────────┘
    #                                                                  PREVIEW_WIDTH
    #
    # LEFT_WIDTH      = largeur totale de la colonne de gauche
    # DROPDOWN_WIDTH  = largeur de la liste déroulante
    # PREVIEW_WIDTH   = largeur de la zone d'aperçu à droite
    # PREVIEW_MARGIN  = marges CSS : haut droite bas gauche
    #
    # Exemple "0 0 0 15px" = aucune marge sauf 15 px à gauche
    #
    LEFT_WIDTH = "220px"
    DROPDOWN_WIDTH = "200px"
    PREVIEW_WIDTH = "320px"
    PREVIEW_MARGIN = "0 0 0 15px"

    scenario_files = sorted(SCENARIOS_DIR.glob("*.yaml"))

    label_choose = widgets.Label(value="1 Choisir le scénario")

    scenario_options = [
        (load_scenario(file.stem)["title"], file.stem) for file in scenario_files
    ]

    # Tri alphabétique selon le titre affiché, et non selon le nom du fichier YAML
    scenario_options.sort(key=lambda x: x[0].casefold())

    scenario_dropdown = widgets.Dropdown(
        options=scenario_options,
        value="super_scenario",
        description="",
        layout=widgets.Layout(width=DROPDOWN_WIDTH),
    )

    preview = widgets.HTML(
        layout=widgets.Layout(
            width=PREVIEW_WIDTH,
            margin=PREVIEW_MARGIN,
        )
    )

    def preview_selected(change=None):
        preview.value = scenario_preview_html(load_scenario(scenario_dropdown.value))

    scenario_dropdown.observe(preview_selected, names="value")
    preview_selected()

    row_choose = widgets.VBox([label_choose, scenario_dropdown])

    button_load = widgets.Button(description="2 Charger le scénario")

    output = widgets.Output()

    def set_selection(name):

        selection["scenario_name"] = name
        selection["scenario"] = load_scenario(name)
        selection["concepts"] = [
            obj["name"] for obj in selection["scenario"]["objects"]
        ]
        selection["objects"] = selection["scenario"]["objects"]
        selection["icons"] = {
            obj["name"]: object_icon(obj) for obj in selection["objects"]
        }

    def load_selected_scenario(b):

        set_selection(scenario_dropdown.value)

        with output:
            output.clear_output()
            display_function(selection["scenario"])

    button_load.on_click(load_selected_scenario)

    set_selection(scenario_dropdown.value)

    controls = widgets.VBox(
        [row_choose, button_load],
        layout=widgets.Layout(width=LEFT_WIDTH),
    )

    display(
        widgets.HBox(
            [controls, preview],
            layout=widgets.Layout(
                width="100%",
                align_items="flex-start",
            ),
        ),
        output,
    )
