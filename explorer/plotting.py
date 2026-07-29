# plotting.py
# PhL 29jul26

import plotly.graph_objects as go

from explorer.config import CATEGORY_COLORS


def plot_scene(df, title):
    """
    Display a 3D Plotly scene from a PCA dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing PC1, PC2, PC3, Catégorie and Mot.
    title : str
        Figure title.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = go.Figure()

    for category, color in CATEGORY_COLORS.items():

        subset = df[df["Catégorie"] == category]

        if subset.empty:
            continue

        fig.add_trace(
            go.Scatter3d(
                x=subset["PC1"],
                y=subset["PC2"],
                z=subset["PC3"],
                mode="markers+text",
                text=subset["Mot"],
                textposition="top center",
                marker=dict(
                    size=7,
                    color=color,
                ),
                name=category,
            )
        )

    fig.update_layout(
        title=title,
        width=900,
        height=700,
        scene=dict(
            xaxis_title="PC1",
            yaxis_title="PC2",
            zaxis_title="PC3",
        ),
    )

    return fig
    
