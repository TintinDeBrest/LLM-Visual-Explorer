from pathlib import Path
import json


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parent

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".ipynb_checkpoints",
    ".vscode",
    "node_modules",
    "explorations",
    "exports",
}


# ============================================================
# Helpers
# ============================================================

def is_excluded(path):
    """Return True if the path belongs to an excluded directory."""
    return any(part in EXCLUDED_DIRS for part in path.parts)


def count_text_lines(path):
    """Count non-empty lines in a text file."""
    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    return sum(
        1
        for line in text.splitlines()
        if line.strip()
    )


def count_notebook_lines(path):
    """Count source lines in notebook cells, ignoring outputs."""

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        notebook = json.load(f)

    code_lines = 0
    markdown_lines = 0

    for cell in notebook.get("cells", []):

        source = cell.get("source", [])

        if isinstance(source, str):
            source = source.splitlines()

        count = sum(
            1
            for line in source
            if line.strip()
        )

        if cell.get("cell_type") == "code":
            code_lines += count

        elif cell.get("cell_type") == "markdown":
            markdown_lines += count

    return code_lines, markdown_lines


# ============================================================
# Scan project
# ============================================================

python_lines = 0
yaml_lines = 0

notebook_code_lines = 0
notebook_markdown_lines = 0

python_files = 0
yaml_files = 0
notebook_files = 0


for path in ROOT.rglob("*"):

    if not path.is_file():
        continue

    relative_path = path.relative_to(ROOT)

    if is_excluded(relative_path):
        continue

    # Python
    if path.suffix == ".py":

        python_lines += count_text_lines(path)
        python_files += 1

    # YAML
    elif path.suffix in {".yaml", ".yml"}:

        yaml_lines += count_text_lines(path)
        yaml_files += 1

    # Jupyter notebooks
    elif path.suffix == ".ipynb":

        code, markdown = count_notebook_lines(path)

        notebook_code_lines += code
        notebook_markdown_lines += markdown

        notebook_files += 1


# ============================================================
# Report
# ============================================================

notebook_total = (
    notebook_code_lines
    + notebook_markdown_lines
)

source_total = (
    python_lines
    + yaml_lines
    + notebook_total
)


print()
print("=" * 60)
print("LLM VISUAL EXPLORER — SOURCE CODE STATISTICS")
print("=" * 60)

print(
    f"Python              {python_lines:6d} lines"
    f"   ({python_files} files)"
)

print(
    f"YAML                {yaml_lines:6d} lines"
    f"   ({yaml_files} files)"
)

print(
    f"Notebook code       {notebook_code_lines:6d} lines"
)

print(
    f"Notebook Markdown   {notebook_markdown_lines:6d} lines"
)

print(
    f"Notebooks total     {notebook_total:6d} lines"
    f"   ({notebook_files} files)"
)

print("-" * 60)

print(
    f"TOTAL SOURCE        {source_total:6d} lines"
)

print("=" * 60)
print()