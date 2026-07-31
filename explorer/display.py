# Display pour tous les affichages du notebook
#===============================================

from explorer.config import MODEL_NAME


def display_scenario(scenario):
    """
    Affiche les informations principales du scenario
    """
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


def display_model(model):
    """
    Affiche les informations principales du modèle d'embeddings.
    """

    print("=" * 60)
    print("MODÈLE D'EMBEDDINGS")
    print("=" * 60)
    print()

    print("Architecture :")
    print(f"  {model.__class__.__name__}")
    print()

    print("Modèle :")
    print(f"  {MODEL_NAME}")
    print()

    print("Dimension des embeddings :")
    print(f"  {model.get_embedding_dimension()}")

    print()


def display_projection(explained_variance):
    """
    Affiche l'information conservée par la projection 3D.
    
    Parameters
    ----------
    explained_variance : float
        Pourcentage de variance conservée par les trois premières composantes.
    """

    print("=" * 60)
    print("PROJECTION 3D")
    print("=" * 60)
    print()

    print(
        f"La projection 3D conserve environ "
        f"{explained_variance:.1f}% "
        "de la variance des embeddings."
    )

    print()


