# ====================================================================
# prompts.py
# ====================================================================

from pathlib import Path

from explorer.config import INTERFACE_LANGUAGE
from explorer.i18n import format_percent


PROMPT_TEMPLATES_DIR = (
    Path(__file__).resolve().parent
    / "prompt_templates"
)


def load_prompt_template(prompt_type):
    """Load a prompt template in the interface language."""

    template_path = (
        PROMPT_TEMPLATES_DIR
        / f"{prompt_type}_{INTERFACE_LANGUAGE}.md"
    )

    if not template_path.exists():
        raise FileNotFoundError(
            f"Prompt template not found: {template_path}"
        )

    return template_path.read_text(encoding="utf-8")


def replace_prompt_values(template, values):
    """Replace explicit placeholders in a prompt template."""

    prompt = template

    for name, value in values.items():
        placeholder = "{{" + name + "}}"
        prompt = prompt.replace(placeholder, str(value))

    return prompt


def create_prompt(
    concept1,
    concept2,
    model_name,
    similarity,
):
    """Create a localized pair-analysis prompt."""

    template = load_prompt_template("pair")

    return replace_prompt_values(
        template,
        {
            "concept1": concept1,
            "concept2": concept2,
            "model_name": model_name,
            "similarity_percent": format_percent(
                similarity,
                decimals=0,
            ),
        },
    )

def create_group_prompt(
    selected_concepts,
    selected_pairs,
    model_name,
):
    """Create a localized four-concept group-analysis prompt."""

    template = load_prompt_template("group")

    concept_lines = "\n".join(
        f"- {concept}"
        for concept in selected_concepts
    )

    similarity_lines = "\n".join(
        (
            f"- {concept_a} ↔ {concept_b}: "
            f"{format_percent(score, decimals=1)}"
        )
        for concept_a, concept_b, score in selected_pairs
    )

    return replace_prompt_values(
        template,
        {
            "concept_lines": concept_lines,
            "model_name": model_name,
            "similarity_lines": similarity_lines,
        },
    )