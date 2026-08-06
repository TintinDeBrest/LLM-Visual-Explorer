# =========================================================
# plotting.py
# =========================================================

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

    categories = list(df["Catégorie"].unique())

    category_colors = {
        cat: CATEGORY_PALETTE[i % len(CATEGORY_PALETTE)]
        for i, cat in enumerate(categories)
    }

    for category in categories:

        subset = df[df["Catégorie"] == category]

        labels = build_labels(
            subset["Mot"],
            icons,
            show_labels,
            show_icons,
        )

        hover = [
            f"{icons.get(m,'')} <b>{m}</b><br>"
            f"Catégorie : {c}<br>"
            f"PC1 : {x:.2f}<br>"
            f"PC2 : {y:.2f}"
            for m, c, x, y in zip(
                subset["Mot"],
                subset["Catégorie"],
                subset["PC1"],
                subset["PC2"],
            )
        ]

        fig.add_trace(
            go.Scatter(
                x=subset["PC1"],
                y=subset["PC2"],
                mode="markers+text",
                text=labels,
                textposition="top center",
                hovertext=hover,
                hoverinfo="text",
                marker=dict(
                    size=9,
                    color=category_colors[category],
                ),
                name=category,
            )
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

    categories = list(df["Catégorie"].unique())

    category_colors = {
        cat: CATEGORY_PALETTE[i % len(CATEGORY_PALETTE)]
        for i, cat in enumerate(categories)
    }

    for category in categories:

        subset = df[df["Catégorie"] == category]

        labels = build_labels(
            subset["Mot"],
            icons,
            show_labels,
            show_icons,
        )

        hover = [
            f"{icons.get(m,'')} <b>{m}</b><br>"
            f"Catégorie : {c}<br>"
            f"PC1 : {x:.2f}<br>"
            f"PC2 : {y:.2f}<br>"
            f"PC3 : {z:.2f}"
            for m, c, x, y, z in zip(
                subset["Mot"],
                subset["Catégorie"],
                subset["PC1"],
                subset["PC2"],
                subset["PC3"],
            )
        ]

        fig.add_trace(
            go.Scatter3d(
                x=subset["PC1"],
                y=subset["PC2"],
                z=subset["PC3"],
                mode="markers+text",
                text=labels,
                textposition="top center",
                hovertext=hover,
                hoverinfo="text",
                marker=dict(
                    size=6,
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
            aspectmode="cube",
            xaxis_title="PC1",
            yaxis_title="PC2",
            zaxis_title="PC3",
        ),
    )

    return fig
