#=======================================================================
# Dataframe - Prepare results for visualization
#=======================================================================

import pandas as pd

def create_dataframe(words, categories, xyz):
    """
    Create a DataFrame from words, categories and PCA coordinates.
    """

    df = pd.DataFrame({
        "Mot": words,
        "Catégorie": categories,
        "PC1": xyz[:, 0],
        "PC2": xyz[:, 1],
        "PC3": xyz[:, 2],
    })

    return df
