# Display pour tous les affichages du notebook
#===============================================

def display_model(model):

    print("=" * 60)
    print("MODÈLE D'EMBEDDINGS")
    print("=" * 60)
    print()

    print(model.__class__.__name__)

    print(model.model_card_data.base_model)
    print(model.get_sentence_embedding_dimension())


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

