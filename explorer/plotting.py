# =========================================================
# plotting.py
# =========================================================

import plotly.graph_objects as go


# Palette des classes spectrales stellaires, de O (bleu) à M (rouge).
# Elle ne porte aucune signification scientifique sur les concepts : elle sert
# uniquement à rendre la force sémantique déjà calculée plus lisible.
SPECTRAL_STOPS = [
    (0.00, (255, 112, 67)),   # M — rouge-orangé
    (0.20, (255, 176, 92)),   # K — orange clair
    (0.40, (255, 244, 214)),  # G/F — blanc chaud
    (0.60, (248, 250, 255)),  # A — blanc
    (0.80, (190, 218, 255)),  # B — bleu-blanc
    (1.00, (116, 174, 255)),  # O — bleu
]


def strength_to_spectral_color(value):
    """Convertit une force visuelle 0..1 en couleur stellaire O→M.

    La valeur est inchangée : seule sa représentation graphique évolue.
    """

    value = max(0, min(1, value))

    for i in range(len(SPECTRAL_STOPS) - 1):
        v1, c1 = SPECTRAL_STOPS[i]
        v2, c2 = SPECTRAL_STOPS[i + 1]

        if v1 <= value <= v2:
            t = (value - v1) / (v2 - v1)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)

            return f"rgb({r},{g},{b})"

    return "rgb(116,174,255)"


def normalize_visual_strengths(values):
    """Étale une série de forces sur 0..1 pour la couleur uniquement.

    Cette normalisation ne modifie ni les valeurs de semantic_strength ni la
    taille des étoiles. Elle assure simplement que la palette complète est
    visible pour chaque scénario.
    """

    minimum = min(values)
    maximum = max(values)

    if minimum == maximum:
        return [0.5] * len(values)

    return [(value - minimum) / (maximum - minimum) for value in values]


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
                color="rgb(255,244,214)",
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
                font=dict(color="rgb(245,247,255)"),
            )

    fig.update_layout(
        title=title,
        width=850,
        height=650,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="rgb(245,247,255)"),
        xaxis=dict(
            title="X",
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="rgba(245,247,255,0.65)",
            tickcolor="rgba(245,247,255,0.65)",
        ),
        yaxis=dict(
            title="Y",
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="rgba(245,247,255,0.65)",
            tickcolor="rgba(245,247,255,0.65)",
        ),
    )

    return fig


def plot_scene(
    df,
    title,
    icons=None,
    show_labels=False,
    show_icons=False,
    semantic_strength=None,
    strength_mode="relative",
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

        raw_strengths = [semantic_strength.get(name, 0) for name in df["Mot"]]

        if strength_mode == "relative":
            # Le mode relatif maximise le contraste à l'intérieur d'un même
            # scénario, comme dans le rendu Planetarium actuel.
            visual_strengths = normalize_visual_strengths(raw_strengths)
        elif strength_mode == "comparable":
            # Le mode comparable conserve l'échelle absolue 0..1 afin que les
            # tailles et couleurs soient comparables entre scénarios.
            visual_strengths = [max(0, min(1, value)) for value in raw_strengths]
        else:
            raise ValueError("strength_mode must be 'relative' or 'comparable'")

        star_sizes = [14 + 26 * value for value in visual_strengths]

        # Dégradé volontairement inversé : les étoiles les plus fortes sont
        # rouges, les plus faibles bleues, pour une lecture plus immédiate.
        star_colors = [
            strength_to_spectral_color(1 - value) for value in visual_strengths
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
        # Vue géométrique simple : étoiles homogènes
        # -----------------------------------------------------

        fig.add_trace(
            go.Scatter3d(
                x=df["PC1"],
                y=df["PC2"],
                z=df["PC3"],
                mode="text",
                text=["★"] * len(df),
                textfont=dict(
                    size=18,
                    color="rgb(255,244,214)",
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
                color="rgb(245,247,255)",
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
        paper_bgcolor="black",
        font=dict(color="rgb(245,247,255)"),
        scene=dict(
            aspectmode="cube",
            bgcolor="black",
            xaxis=dict(
                title="X",
                showbackground=False,
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="rgba(245,247,255,0.65)",
                tickcolor="rgba(245,247,255,0.65)",
            ),
            yaxis=dict(
                title="Y",
                showbackground=False,
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="rgba(245,247,255,0.65)",
                tickcolor="rgba(245,247,255,0.65)",
            ),
            zaxis=dict(
                title="Z",
                showbackground=False,
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="rgba(245,247,255,0.65)",
                tickcolor="rgba(245,247,255,0.65)",
            ),
        ),
    )

    return fig
