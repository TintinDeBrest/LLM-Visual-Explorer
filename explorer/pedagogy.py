# ====================================================================
# pedagogy.py
# Display pedagogical Markdown texts
# ====================================================================

from pathlib import Path

from IPython.display import Markdown, display

from explorer import config


PEDAGOGICAL_TEXTS_DIR = Path(__file__).with_name("pedagogical_texts")


def display_pedagogical_text(section, version="full"):
    """Display a pedagogical Markdown text in the active interface language."""

    language = config.INTERFACE_LANGUAGE

    file_path = (
        PEDAGOGICAL_TEXTS_DIR
        / section
        / f"{language}_{version}.md"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Pedagogical text not found: {file_path}"
        )

    text = file_path.read_text(encoding="utf-8")

    display(Markdown(text))