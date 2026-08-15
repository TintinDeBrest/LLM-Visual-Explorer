# =========================================================
# plotting.py
# =========================================================

import plotly.graph_objects as go
from explorer.config import CLUSTER_C1


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
    semantic_strength=None,
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
    # Étoiles 3D
    # ---------------------------------------------------------

    if semantic_strength is not None:

        # -----------------------------------------------------
        # Nouvelle visualisation :
        # taille et couleur = force sémantique
        # -----------------------------------------------------

        star_sizes = [20 + 16 * semantic_strength.get(name, 0) for name in df["Mot"]]

        def strength_to_color(value):
            """Convertit une force 0..1 en couleur,
            du bleu sombre au rouge vif en passant par
            bleu, jaune et rouge.
            """

            # Points de contrôle :
            # force 0.00 → bleu sombre
            # force 0.25 → bleu
            # force 0.50 → jaune
            # force 0.75 → rouge
            # force 1.00 → rouge vif

            stops = [
                (0.00, (20, 45, 100)),
                (0.25, (30, 90, 200)),
                (0.50, (255, 220, 40)),
                (0.75, (220, 50, 30)),
                (1.00, (255, 0, 0)),
            ]

            # Sécurité
            value = max(0, min(1, value))

            # Recherche du segment
            for i in range(len(stops) - 1):

                v1, c1 = stops[i]
                v2, c2 = stops[i + 1]

                if v1 <= value <= v2:

                    # Position relative dans le segment
                    t = (value - v1) / (v2 - v1)

                    r = int(c1[0] + (c2[0] - c1[0]) * t)
                    g = int(c1[1] + (c2[1] - c1[1]) * t)
                    b = int(c1[2] + (c2[2] - c1[2]) * t)

                    return f"rgb({r},{g},{b})"

            return "rgb(255,0,0)"

        star_colors = [
            strength_to_color(semantic_strength.get(name, 0)) for name in df["Mot"]
        ]

        fig.add_trace(
            go.Scatter3d(
                x=df["PC1"],
                y=df["PC2"],
                z=df["PC3"],
                mode="text",
                text=["★"] * len(df),
                textfont=dict(
                    size=star_sizes,
                    color=star_colors,
                ),
                hovertext=hover,
                hoverinfo="text",
                showlegend=False,
            )
        )

    else:

        # -----------------------------------------------------
        # Ancien comportement :
        # cluster C1
        # -----------------------------------------------------

        cluster_sizes = [28 if name in CLUSTER_C1 else 18 for name in df["Mot"]]

        cluster_colors = ["red" if name in CLUSTER_C1 else "gold" for name in df["Mot"]]

        fig.add_trace(
            go.Scatter3d(
                x=df["PC1"],
                y=df["PC2"],
                z=df["PC3"],
                mode="text",
                text=["★"] * len(df),
                textfont=dict(
                    size=cluster_sizes,
                    color=cluster_colors,
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
            textposition="top center",
            textfont=dict(
                size=12,
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # ---------------------------------------------------------
    # Mise en page
    # ---------------------------------------------------------

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
