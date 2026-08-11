# =======================================================================
# Dataframe - Prepare results for visualization
# =======================================================================

import pandas as pd


def create_dataframe(concepts, xyz):
    """
    Create a DataFrame from concepts and PCA coordinates.
    """

    df = pd.DataFrame(
        {
            "Mot": concepts,
            "PC1": xyz[:, 0],
            "PC2": xyz[:, 1],
            "PC3": xyz[:, 2],
        }
    )

    df[["PC1", "PC2", "PC3"]] = df[["PC1", "PC2", "PC3"]].round(2)

    return df
