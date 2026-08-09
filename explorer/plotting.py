# =========================================================
# plotting.py
# =========================================================

import plotly.graph_objects as go


def build_labels(names, icons, show_labels, show_icons):

    labels = []

    for name in names:

        icon = icons.get(name, "")

        if show_labels and show_icons:
            labels.append(f"{icon} {name}".strip())

        elif show_labels:
            labels.append(name)

        elif show_icons:
            labels.append(icon)

        else:
            labels.append("")

    return labels


def plot_map(
    df,
    title,
    icons=None,
    show_labels=False,
    show_icons=False,
):

    if icons is None:
        icons = {}

    fig = go.Figure()

    # ---------------------------------------------------------
    # Labels
    # ---------------------------------------------------------

    labels = df["Mot"].tolist()

    hover = [
        f"{icons.get(m, '')} <b>{m}</b><br>" f"PC1 : {x:.2f}<br>" f"PC2 : {y:.2f}"
        for m, x, y in zip(
            df["Mot"],
            df["PC1"],
            df["PC2"],
        )
    ]

    # ---------------------------------------------------------
    # ⭐ Étoiles 2D
    # ---------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["PC1"],
            y=df["PC2"],
            mode="markers",
            marker=dict(
                symbol="star",
                size=16,
                color="gold",
            ),
            hovertext=hover,
            hoverinfo="text",
            showlegend=False,
        )
    )

    # ---------------------------------------------------------
    # Noms des concepts
    # ---------------------------------------------------------

    if show_labels:

        for x, y, name in zip(
            df["PC1"],
            df["PC2"],
            df["Mot"],
        ):

            fig.add_annotation(
                x=x,
                y=y,
                text=name,
                showarrow=False,
                yshift=18,
                xanchor="center",
                yanchor="bottom",
            )

    fig.update_layout(
        title=title,
        width=850,
        height=650,
        xaxis_title="PC1",
        yaxis_title="PC2",
        template="simple_white",
    )

    return fig


def plot_scene(
    df,
    title,
    icons=None,
    show_labels=False,
    show_icons=False,
):

    if icons is None:
        icons = {}

    fig = go.Figure()

    # ---------------------------------------------------------
    # Labels
    # ---------------------------------------------------------

    labels = df["Mot"].tolist()

    hover = [
        f"{icons.get(m, '')} <b>{m}</b><br>"
        f"PC1 : {x:.2f}<br>"
        f"PC2 : {y:.2f}<br>"
        f"PC3 : {z:.2f}"
        for m, x, y, z in zip(
            df["Mot"],
            df["PC1"],
            df["PC2"],
            df["PC3"],
        )
    ]

    # ---------------------------------------------------------
    # ⭐ Étoiles 3D
    #
    # Plotly Scatter3d ne supporte pas le symbole "star".
    # On utilise donc le caractère Unicode ★ comme texte.
    # ---------------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=df["PC1"],
            y=df["PC2"],
            z=df["PC3"],
            mode="text",
            text=["★"] * len(df),
            textfont=dict(
                size=18,
                color="gold",
            ),
            hovertext=hover,
            hoverinfo="text",
            showlegend=False,
        )
    )

    # ---------------------------------------------------------
    # Noms des concepts
    # ---------------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=df["PC1"],
            y=df["PC2"],
            z=df["PC3"],
            mode="text",
            text=labels,
            textposition="middle right",
            textfont=dict(
                size=12,
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(
        title=title,
        width=900,
        height=700,
        scene=dict(
            aspectmode="cube",
            xaxis_title="PC1",
            yaxis_title="PC2",
            zaxis_title="PC3",
        ),
    )

    return fig
