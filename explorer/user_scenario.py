# ====================================================================
# user_scenario.py
# ====================================================================
from html import escape

import ipywidgets as widgets
import yaml
from IPython.display import display

from explorer import config
from explorer.i18n import tr
from explorer.scenarios import (
    SCENARIOS_DIR,
    load_scenario,
    object_icon,
    scenario_preview_html,
)


MIN_CONCEPTS = 4
MAX_CONCEPTS = 30


def _user_scenario_name():
    """Return the persistent scenario name for the interface language."""

    language = config.INTERFACE_LANGUAGE

    if language not in {"fr", "en", "es"}:
        raise ValueError(f"Unsupported interface language: {language!r}")

    return f"user_{language}"


def _load_existing_concepts(name):
    """Load an existing user scenario, or start with an empty list."""

    path = SCENARIOS_DIR / f"{name}.yaml"

    if not path.exists():
        return []

    scenario = load_scenario(name)
    return [obj["name"] for obj in scenario["objects"]]


def _set_selection(selection, name):
    """Prepare the notebook selection dictionary for the saved scenario."""

    scenario = load_scenario(name)
    objects = scenario["objects"]

    selection["scenario_name"] = name
    selection["scenario"] = scenario
    selection["concepts"] = [obj["name"] for obj in objects]
    selection["objects"] = objects
    selection["icons"] = {
        obj["name"]: object_icon(obj)
        for obj in objects
    }
    selection["short_names"] = {
        obj["name"]: obj.get("short_name", obj["name"])
        for obj in objects
    }


def user_scenario_editor(selection=None, display_function=None):
    """Create or update the minimal user scenario for the current language."""

    name = _user_scenario_name()
    path = SCENARIOS_DIR / f"{name}.yaml"
    concepts = _load_existing_concepts(name)

    title = widgets.HTML(
        value=f"<h3>🧪 {escape(tr('user_scenario_title'))}</h3>"
    )
    introduction = widgets.HTML(
        value=f"<p>{escape(tr('user_scenario_intro'))}</p>"
    )

    concept_input = widgets.Text(
        placeholder=tr("user_scenario_placeholder"),
        layout=widgets.Layout(width="420px"),
    )
    add_button = widgets.Button(
        description=tr("user_scenario_add"),
        button_style="primary",
        layout=widgets.Layout(width="130px"),
    )
    concept_list = widgets.SelectMultiple(
        options=[],
        rows=10,
        description="",
        layout=widgets.Layout(width="420px"),
    )
    remove_button = widgets.Button(
        description=tr("user_scenario_remove"),
        layout=widgets.Layout(width="190px"),
    )
    save_button = widgets.Button(
        description=tr("user_scenario_save"),
        button_style="success",
        layout=widgets.Layout(width="210px"),
    )
    counter = widgets.HTML()
    message = widgets.HTML()
    preview = widgets.HTML()

    def refresh():
        concept_list.options = [
            (concept, index)
            for index, concept in enumerate(concepts)
        ]
        counter.value = (
            f"<b>{len(concepts)}/{MAX_CONCEPTS}</b> "
            f"{escape(tr('user_scenario_concepts'))}"
        )

    def show_message(text, color):
        message.value = (
            f"<p style='color:{color}; margin:8px 0'>"
            f"{escape(text)}</p>"
        )

    def add_concept(_):
        concept = concept_input.value.strip()

        if not concept:
            show_message(tr("user_scenario_empty"), "#b00020")
            return

        if any(existing.casefold() == concept.casefold() for existing in concepts):
            show_message(tr("user_scenario_duplicate"), "#b00020")
            return

        if len(concepts) >= MAX_CONCEPTS:
            show_message(
                tr("user_scenario_maximum", count=MAX_CONCEPTS),
                "#b00020",
            )
            return

        concepts.append(concept)
        concept_input.value = ""
        message.value = ""
        refresh()

    def remove_concepts(_):
        selected_indices = sorted(concept_list.value, reverse=True)

        if not selected_indices:
            show_message(tr("user_scenario_select_remove"), "#b00020")
            return

        for index in selected_indices:
            del concepts[index]

        message.value = ""
        refresh()

    def save_scenario(_):
        if len(concepts) < MIN_CONCEPTS:
            show_message(
                tr("user_scenario_minimum", count=MIN_CONCEPTS),
                "#b00020",
            )
            return

        data = {"concepts": concepts}
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                data,
                file,
                allow_unicode=True,
                sort_keys=False,
            )

        if selection is not None:
            _set_selection(selection, name)

        scenario = load_scenario(name)
        preview.value = scenario_preview_html(scenario)

        if display_function is not None:
            display_function(scenario)

        show_message(
            tr("user_scenario_saved", filename=path.name),
            "#1b6e2e",
        )

    add_button.on_click(add_concept)
    remove_button.on_click(remove_concepts)
    save_button.on_click(save_scenario)
    refresh()

    display(
        widgets.VBox(
            [
                title,
                introduction,
                widgets.HBox([concept_input, add_button]),
                counter,
                concept_list,
                remove_button,
                save_button,
                message,
                preview,
            ],
            layout=widgets.Layout(width="100%"),
        )
    )

