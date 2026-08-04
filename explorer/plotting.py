# plotting.py
# PhL 29jul26

import plotly.graph_objects as go

CATEGORY_PALETTE = [
    "royalblue",
    "darkorange",
    "purple",
    "forestgreen",
    "crimson",
    "gold",
    "deeppink",
    "teal",
]


def plot_scene(df, title, icons=None):
    """
    Display a 3D Plotly scene from a PCA dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing PC1, PC2, PC3, Catégorie and Mot.
    title : str
        Figure title.

    icons : dict, optional
        Dictionary mapping item names to emojis/icons.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = go.Figure()

    if icons is None:
        icons = {}

    # -----------------------------------------------------------------
    # Automatic color assignment for categories
    # -----------------------------------------------------------------

    categories = list(df["Catégorie"].unique())

    
    category_colors = {
        category: CATEGORY_PALETTE[i % len(CATEGORY_PALETTE)]
        for i, category in enumerate(categories)
    }
    
    # -----------------------------------------------------------------
    # Plot one trace per category
    # -----------------------------------------------------------------

    for category in categories:

        subset = df[df["Catégorie"] == category]

        subset_labels = [
            f"{icons.get(mot, '')} {mot}".strip()
            for mot in subset["Mot"]
        ]

        fig.add_trace(
            go.Scatter3d(
                x=subset["PC1"],
                y=subset["PC2"],
                z=subset["PC3"],
                mode="markers+text",
                text=subset_labels,
                textposition="top center",
                marker=dict(
                    size=9,
                    color=category_colors[category],
                ),
                name=category,
            )
        )

    fig.update_layout(
        title=title,
        width=900,
        height=700,
        scene=dict(
            aspectmode="data",
            xaxis_title="PC1",
            yaxis_title="PC2",
            zaxis_title="PC3",
        ),
    )

    return fig
    
