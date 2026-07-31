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



