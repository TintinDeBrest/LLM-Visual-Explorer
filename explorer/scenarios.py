# scenarios
from pathlib import Path
import yaml


SCENARIOS_DIR = Path(__file__).parent / "scenarios"


def load_scenario(name: str):

    filename = SCENARIOS_DIR / f"{name}.yaml"

    if not filename.exists():
        raise FileNotFoundError(filename)

    with open(filename, "r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)

    return scenario

def get_scenarios():
    return list(SCENARIOS.keys())


def display_scenario(scenario):
    """Affiche proprement le scénario dans le notebook."""

    print("=" * 50)
    print(f"SCÉNARIO : {scenario['name'].upper()}")
    print("=" * 50)

    print("\nObjets analysés :\n")

    for obj in scenario["objects"]:
        print(f"  • {obj}")

    print(f"\nNombre d'objets : {len(scenario['objects'])}")
