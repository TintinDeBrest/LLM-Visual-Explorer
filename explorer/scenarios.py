from pathlib import Path
import yaml


SCENARIOS_DIR = Path(__file__).parent / "scenarios"


def load_scenario(name: str):
    """
    Charge un scénario YAML et retourne un objet Scenario.
    """
    filename = SCENARIOS_DIR / f"{name}.yaml"

    if not filename.exists():
        raise FileNotFoundError(filename)

    with open(filename, "r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)

    return scenario


def display_scenario(scenario):

    print("=" * 60)

    print(f"SCÉNARIO : {scenario['title']}")

    print("=" * 60)

    print()

    print(scenario["description"])

    print()

    print("Objets analysés :")

    print()

    for obj in scenario["objects"]:

        print(f"   • {obj['name']}")

    print()

    print(f"Nombre d'objets : {len(scenario['objects'])}")

    print("=" * 60)
