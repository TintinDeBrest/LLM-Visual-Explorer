# Display pour tous les affichages du notebook
#===============================================

from explorer.config import MODEL_NAME


def display_model(model):

    print("=" * 60)
    print("MODÈLE D'EMBEDDINGS")
    print("=" * 60)
    print()

    print(f"Nom        : {MODEL_NAME}")
    print(f"Dimension  : {model.get_embedding_dimension()}")

    print()


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

