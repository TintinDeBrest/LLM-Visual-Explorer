# ===================================================================
#   scenarios.py
# ===================================================================
from pathlib import Path
from html import escape
import yaml
import ipywidgets as widgets
from IPython.display import display

from explorer.config import DEFAULT_SCENARIO, SCENARIO_LANGUAGE

SCENARIOS_DIR = Path(__file__).parent / "scenarios"
CATALOG_EXPORT_DIR = Path(__file__).parent.parent / "catalog_exports"


def load_scenario(name: str):
    """
    Charge un scénario YAML et retourne ses données sous forme de dictionnaire
    """
    filename = SCENARIOS_DIR / f"{name}.yaml"

    if not filename.exists():
        raise FileNotFoundError(filename)

    with open(filename, "r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)

    scenario["_name"] = name

    return scenario


def object_icon(obj):
    """Return the current emoji field or the legacy icon field."""

    return obj.get("emoji", obj.get("icon", ""))


def scenario_preview_html(scenario):
    """Create a compact visual preview of a scenario's concepts."""

    concepts = "<br>".join(
        f"{escape(str(object_icon(obj)))} &nbsp; {escape(str(obj['name']))}"
        for obj in scenario["objects"]
    )

    return f"""
    <div style="background: white; color: #161616; font-family: monospace;
                font-size: 16px; line-height: 1.45; padding: 14px 18px;">
        <div style="font-family: sans-serif; font-size: 18px; font-weight: 600;">
            {escape(str(scenario['title']))}
        </div>
        <div style="font-family: sans-serif; font-size: 13px; margin: 4px 0 10px;">
            {escape(str(scenario['description']))}
        </div>
        {concepts}
    </div>
    """


def scenario_catalog_html():
    """Create a responsive catalog from all available scenario files."""

    scenarios = [
        load_scenario(file.stem) for file in SCENARIOS_DIR.glob("*.yaml")
    ]
    scenarios.sort(key=lambda scenario: str(scenario["title"]).casefold())

    cards = []

    for scenario in scenarios:
        concepts = "".join(
            f"""
            <div class="llmexpl-catalog-concept">
                <span class="llmexpl-catalog-emoji">
                    {escape(str(object_icon(obj)))}
                </span>
                <span>{escape(str(obj["name"]))}</span>
            </div>
            """
            for obj in scenario["objects"]
        )

        cards.append(f"""
            <section class="llmexpl-catalog-card">
                <h3>{escape(str(scenario["title"]))}</h3>
                <p>{escape(str(scenario["description"]))}</p>
                <div class="llmexpl-catalog-concepts">
                    {concepts}
                </div>
            </section>
        """)

    return f"""
    <style>
        .llmexpl-catalog {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            align-items: start;
            font-family: sans-serif;
        }}

        .llmexpl-catalog-card {{
            box-sizing: border-box;
            background: white;
            color: #161616;
            border: 1px solid #d9d9d9;
            border-radius: 8px;
            padding: 16px 18px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }}

        .llmexpl-catalog-card h3 {{
            margin: 0 0 8px;
            font-size: 20px;
            line-height: 1.2;
        }}

        .llmexpl-catalog-card p {{
            margin: 0 0 12px;
            font-size: 14px;
            line-height: 1.45;
        }}

        .llmexpl-catalog-concepts {{
            display: grid;
            gap: 3px;
            font-family: monospace;
            font-size: 15px;
            line-height: 1.35;
        }}

        .llmexpl-catalog-concept {{
            display: grid;
            grid-template-columns: 28px 1fr;
            gap: 6px;
            align-items: start;
        }}

        .llmexpl-catalog-emoji {{
            text-align: center;
        }}

        @media (max-width: 640px) {{
            .llmexpl-catalog {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>

    <div class="llmexpl-catalog">
        {"".join(cards)}
    </div>
    """


def export_scenario_catalog_images(
    output_dir=None,
    scenarios_per_page=4,
    image_format="PNG",
):
    """Export the scenario catalog as promotional image pages."""

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:
        raise RuntimeError(
            "L'export du catalogue nécessite Pillow : pip install pillow"
        ) from error

    if scenarios_per_page != 4:
        raise ValueError("Cette première version utilise quatre scénarios par page.")

    image_format = image_format.upper()

    if image_format not in {"PNG", "JPEG"}:
        raise ValueError("image_format must be 'PNG' or 'JPEG'")

    output_dir = Path(output_dir) if output_dir else CATALOG_EXPORT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        load_scenario(file.stem) for file in SCENARIOS_DIR.glob("*.yaml")
    ]
    scenarios.sort(key=lambda scenario: str(scenario["title"]).casefold())

    def load_font(candidates, size):
        for candidate in candidates:
            if Path(candidate).exists():
                return ImageFont.truetype(candidate, size=size)

        return ImageFont.load_default(size=size)

    regular_font_candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    bold_font_candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    mono_font_candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    emoji_font_candidates = [
        "C:/Windows/Fonts/seguiemj.ttf",
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
    ]

    title_font = load_font(bold_font_candidates, 29)
    description_font = load_font(regular_font_candidates, 19)
    concept_font = load_font(mono_font_candidates, 20)
    emoji_font = load_font(emoji_font_candidates, 21)
    header_font = load_font(bold_font_candidates, 30)
    page_font = load_font(regular_font_candidates, 17)

    canvas_width = 1600
    outer_margin = 42
    column_gap = 26
    row_gap = 26
    header_height = 88
    card_width = (canvas_width - 2 * outer_margin - column_gap) // 2
    card_padding = 24
    description_line_height = 25
    concept_line_height = 27

    measurement_image = Image.new("RGB", (1, 1))
    measurement_draw = ImageDraw.Draw(measurement_image)

    def wrap_text(text, font, maximum_width):
        words = str(text).split()
        lines = []
        current_line = ""

        for word in words:
            candidate = f"{current_line} {word}".strip()
            width = measurement_draw.textbbox((0, 0), candidate, font=font)[2]

            if current_line and width > maximum_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = candidate

        if current_line:
            lines.append(current_line)

        return lines or [""]

    def prepare_card(scenario):
        description_lines = wrap_text(
            scenario["description"],
            description_font,
            card_width - 2 * card_padding,
        )
        card_height = (
            2 * card_padding
            + 36
            + 10
            + len(description_lines) * description_line_height
            + 16
            + len(scenario["objects"]) * concept_line_height
        )

        return {
            "scenario": scenario,
            "description_lines": description_lines,
            "height": card_height,
        }

    def draw_emoji(image, position, emoji):
        # Pillow does not consistently compose zero-width-joiner emoji
        # sequences. Use their first complete symbol in the static export.
        emoji_text = str(emoji).split("\u200d", maxsplit=1)[0]
        emoji_tile = Image.new(
            "RGBA",
            (34, concept_line_height),
            (255, 255, 255, 0),
        )
        emoji_draw = ImageDraw.Draw(emoji_tile)

        try:
            emoji_draw.text(
                (0, -2),
                emoji_text,
                font=emoji_font,
                fill="#161616",
                embedded_color=True,
            )
        except (OSError, ValueError):
            emoji_draw.text(
                (0, -2),
                emoji_text,
                font=concept_font,
                fill="#161616",
            )

        image.paste(emoji_tile, position, emoji_tile)

    exported_files = []
    suffix = ".png" if image_format == "PNG" else ".jpg"
    total_pages = (len(scenarios) + scenarios_per_page - 1) // scenarios_per_page

    for page_index in range(total_pages):
        page_scenarios = scenarios[
            page_index * scenarios_per_page : (page_index + 1) * scenarios_per_page
        ]
        cards = [prepare_card(scenario) for scenario in page_scenarios]

        first_row_height = max(card["height"] for card in cards[:2])
        second_row = cards[2:]
        second_row_height = (
            max(card["height"] for card in second_row) if second_row else 0
        )
        canvas_height = (
            header_height
            + outer_margin
            + first_row_height
            + (row_gap + second_row_height if second_row else 0)
            + outer_margin
        )

        image = Image.new("RGB", (canvas_width, canvas_height), "#080808")
        draw = ImageDraw.Draw(image)

        draw.text(
            (outer_margin, 30),
            "LLM VISUAL EXPLORER — Catalogue des scénarios",
            font=header_font,
            fill="#f5f7ff",
        )
        page_label = f"Page {page_index + 1}/{total_pages}"
        page_label_width = draw.textbbox((0, 0), page_label, font=page_font)[2]
        draw.text(
            (canvas_width - outer_margin - page_label_width, 39),
            page_label,
            font=page_font,
            fill="#c8cedb",
        )

        for card_index, card in enumerate(cards):
            column = card_index % 2
            row = card_index // 2
            x = outer_margin + column * (card_width + column_gap)
            y = header_height + outer_margin

            if row == 1:
                y += first_row_height + row_gap

            card_height = first_row_height if row == 0 else second_row_height

            draw.rounded_rectangle(
                (x, y, x + card_width, y + card_height),
                radius=12,
                fill="#ffffff",
                outline="#d9d9d9",
                width=2,
            )

            text_x = x + card_padding
            cursor_y = y + card_padding
            scenario = card["scenario"]

            draw.text(
                (text_x, cursor_y),
                str(scenario["title"]),
                font=title_font,
                fill="#161616",
            )
            cursor_y += 46

            for line in card["description_lines"]:
                draw.text(
                    (text_x, cursor_y),
                    line,
                    font=description_font,
                    fill="#303030",
                )
                cursor_y += description_line_height

            cursor_y += 14

            for obj in scenario["objects"]:
                draw_emoji(image, (text_x, cursor_y - 2), object_icon(obj))
                draw.text(
                    (text_x + 40, cursor_y),
                    str(obj["name"]),
                    font=concept_font,
                    fill="#161616",
                )
                cursor_y += concept_line_height

        output_path = output_dir / f"scenario_catalog_{page_index + 1:02d}{suffix}"
        image.save(output_path, format=image_format, quality=94)
        exported_files.append(output_path)

    return exported_files


def scenario_selector(display_function, selection):
    """
    Affiche le sélecteur de scénario et charge le scénario choisi.
    """
    # --- Réglages d'interface du sélecteur ---
    #
    #   <-------- LEFT_WIDTH -------->
    #
    #   ┌──────────────────────┐     <--- PREVIEW_MARGIN --->  ┌──────────────────────────────┐
    #   │ 1 Choisir scénario   │                               │ Aperçu du scénario           │
    #   │ ┌──────────────────┐ │                               │                              │
    #   │ │ scénario       ▼ │ │                               │ Titre                        │
    #   │ └──────────────────┘ │                               │ Description                  │
    #   │   DROPDOWN_WIDTH     │                               │ 🐱 Chat                      │
    #   │                      │                               │ 🐶 Chien                     │
    #   │ [2 Charger scénario] │                               │ 🦁 Lion                      │
    #   └──────────────────────┘                               └──────────────────────────────┘
    #                                                                  PREVIEW_WIDTH
    #
    # LEFT_WIDTH      = largeur totale de la colonne de gauche
    # DROPDOWN_WIDTH  = largeur de la liste déroulante
    # PREVIEW_WIDTH   = largeur de la zone d'aperçu à droite
    # PREVIEW_MARGIN  = marges CSS : haut droite bas gauche
    #
    # Exemple "0 0 0 15px" = aucune marge sauf 15 px à gauche
    #
    LEFT_WIDTH = "220px"
    DROPDOWN_WIDTH = "200px"
    PREVIEW_WIDTH = "320px"
    PREVIEW_MARGIN = "0 0 0 15px"

    scenario_files = sorted(SCENARIOS_DIR.glob("*.yaml"))

    label_choose = widgets.Label(value="1 Choisir le scénario")

    scenario_options = []

    for file in scenario_files:
        scenario = load_scenario(file.stem)

        # Legacy scenarios without language metadata are currently French.
        language = scenario.get("language", "fr")


        if SCENARIO_LANGUAGE != "all" and language != SCENARIO_LANGUAGE:
            continue

        title = scenario["title"]

        if SCENARIO_LANGUAGE == "all":
            display_title = f"{language.upper()} — {title}"
        else:
            display_title = title

        scenario_options.append((display_title, file.stem))

    # Sort by language prefix, then by displayed title.
    scenario_options.sort(key=lambda option: option[0].casefold())

    if not scenario_options:
        raise ValueError(
            f"No scenario is available for language filter: "
            f"{SCENARIO_LANGUAGE!r}"
        )

    available_scenarios = {
        scenario_name for _, scenario_name in scenario_options
    }

    selected_scenario = (
        DEFAULT_SCENARIO
        if DEFAULT_SCENARIO in available_scenarios
        else scenario_options[0][1]
    )

    scenario_dropdown = widgets.Dropdown(
        options=scenario_options,
        value=selected_scenario,
        description="",
        layout=widgets.Layout(width=DROPDOWN_WIDTH),
    )

    preview = widgets.HTML(
        layout=widgets.Layout(
            width=PREVIEW_WIDTH,
            margin=PREVIEW_MARGIN,
        )
    )

    def preview_selected(change=None):
        preview.value = scenario_preview_html(load_scenario(scenario_dropdown.value))

    scenario_dropdown.observe(preview_selected, names="value")
    preview_selected()

    row_choose = widgets.VBox([label_choose, scenario_dropdown])

    button_load = widgets.Button(description="2 Charger le scénario")

    button_catalog = widgets.Button(
        description="📚 Voir tous les scénarios",
        tooltip="Afficher ou masquer le catalogue des scénarios",
        layout=widgets.Layout(width="200px"),
    )

    button_export_catalog = widgets.Button(
        description="🖼️ Exporter le catalogue",
        tooltip="Créer des pages PNG de quatre scénarios",
        layout=widgets.Layout(width="200px"),
    )

    catalog = widgets.HTML(
        value=scenario_catalog_html(),
        layout=widgets.Layout(
            width="100%",
            margin="18px 0 0 0",
            display="none",
        ),
    )
    catalog_export_output = widgets.Output()

    output = widgets.Output()

    def set_selection(name):

        selection["scenario_name"] = name
        selection["scenario"] = load_scenario(name)
        selection["concepts"] = [
            obj["name"] for obj in selection["scenario"]["objects"]
        ]
        selection["objects"] = selection["scenario"]["objects"]
        selection["icons"] = {
            obj["name"]: object_icon(obj) for obj in selection["objects"]
        }

    def load_selected_scenario(b):

        set_selection(scenario_dropdown.value)

        with output:
            output.clear_output()
            display_function(selection["scenario"])

    button_load.on_click(load_selected_scenario)

    def toggle_catalog(b):
        catalog_is_visible = catalog.layout.display != "none"
        catalog.layout.display = "none" if catalog_is_visible else "block"
        b.description = (
            "📚 Voir tous les scénarios"
            if catalog_is_visible
            else "📚 Masquer le catalogue"
        )

    button_catalog.on_click(toggle_catalog)

    def export_catalog(b):
        with catalog_export_output:
            catalog_export_output.clear_output()

            try:
                exported_files = export_scenario_catalog_images()
            except Exception as error:
                print(f"⚠️ Export impossible : {error}")
                return

            b.description = "✓ Catalogue exporté"
            print(f"🖼️ {len(exported_files)} images enregistrées dans :")
            print(f"   {exported_files[0].parent}")

    button_export_catalog.on_click(export_catalog)

    set_selection(scenario_dropdown.value)

    controls = widgets.VBox(
        [button_catalog, button_export_catalog, row_choose, button_load],
        layout=widgets.Layout(width=LEFT_WIDTH),
    )

    display(
        widgets.VBox(
            [
                widgets.HBox(
                    [controls, preview],
                    layout=widgets.Layout(
                        width="100%",
                        align_items="flex-start",
                    ),
                ),
                catalog,
                catalog_export_output,
            ],
            layout=widgets.Layout(
                width="100%",
            ),
        ),
        output,
    )
