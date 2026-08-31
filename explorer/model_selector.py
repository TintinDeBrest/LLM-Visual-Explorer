######################################################
# Model Selector
######################################################

import ipywidgets as widgets
from IPython.display import display

import explorer.config as config


def model_selector():
    """Display the model selector and update the active model."""

    selector = widgets.Dropdown(
        options=[
            ("MiniLM — fast & compact", "MiniLM"),
            ("MPNet — semantic representation", "MPNet"),
            ("BERT — historical reference", "BERT"),
            ("LaBSE — multilingual", "LaBSE"),
        ],
        value=config.ACTIVE_MODEL,
        description="Model:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="430px"),
    )

    def update_active_model(change):
        if change["name"] == "value":
            config.ACTIVE_MODEL = change["new"]

    selector.observe(
        update_active_model,
        names="value",
    )

    display(selector)

    # return selector

def language_selector():

    """Display the interface language selector and update the active language."""

    selector = widgets.Dropdown(

        options=[
            ("English", "en"),
            ("Français", "fr"),
            ("Español", "es"),
        ],

        value=config.INTERFACE_LANGUAGE,

        description="Language:",

        style={"description_width": "initial"},

        layout=widgets.Layout(width="260px"),
    )

    def update_interface_language(change):

        if change["name"] == "value":
            config.INTERFACE_LANGUAGE = change["new"]

    selector.observe(
        update_interface_language,
        names="value",
    )

    display(selector)

    # return selector