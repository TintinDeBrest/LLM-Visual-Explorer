# ====================================================================
# i18n.py
# ====================================================================

from pathlib import Path

import yaml

from explorer.config import INTERFACE_LANGUAGE


TRANSLATIONS_FILE = Path(__file__).with_name("translations.yaml")


def load_translations():
    """Load interface translations from the YAML file."""

    with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


TRANSLATIONS = load_translations()


def tr(key, **values):
    """Return an interface text in the configured language."""

    if INTERFACE_LANGUAGE not in TRANSLATIONS:
        raise ValueError(
            f"Unsupported interface language: {INTERFACE_LANGUAGE!r}"
        )

    language_translations = TRANSLATIONS[INTERFACE_LANGUAGE]

    if key not in language_translations:
        raise KeyError(
            f"Missing translation key {key!r} "
            f"for language {INTERFACE_LANGUAGE!r}"
        )

    return language_translations[key].format(**values)

def format_number(value, decimals=1):
    """Format a number according to the interface language."""

    formatted = f"{value:.{decimals}f}"

    if INTERFACE_LANGUAGE in {"fr", "es"}:
        formatted = formatted.replace(".", ",")

    return formatted

def format_percent(value, decimals=0):
    """Format a decimal value as a localized percentage."""

    number = format_number(
        value * 100,
        decimals=decimals,
    )

    separator = "" if INTERFACE_LANGUAGE == "en" else " "

    return f"{number}{separator}%"