# ====================================================================
# feedback.py
# ====================================================================

import base64

from functools import lru_cache
from html import escape
from pathlib import Path

from IPython.display import HTML, display


LOGO_PATH = (
    Path(__file__).resolve().parent.parent
    / "images"
    / "LlmExpl_logo.png"
)


@lru_cache(maxsize=1)
def load_logo_data():
    """Load and encode the LlmExpl logo only once."""

    if not LOGO_PATH.exists():
        raise FileNotFoundError(
            f"LlmExpl logo not found: {LOGO_PATH}"
        )

    return base64.b64encode(
        LOGO_PATH.read_bytes()
    ).decode()


def feedback_html(title, details=None, status="success"):
    """
    Build a compact and standardized notebook feedback message as HTML.
    """

    status_colors = {
        "success": "#287a4b",
        "warning": "#b26a00",
        "error": "#b00020",
        "info": "#2f5f98",
    }

    if status not in status_colors:
        raise ValueError(
            f"Unsupported feedback status: {status!r}"
        )

    color = status_colors[status]
    logo_data = load_logo_data()

    details_html = ""

    if details:
        details_html = f"""
            <div style="
                margin-top: 2px;
                color: #555;
                font-size: 13px;
                line-height: 1.3;
            ">
                {escape(str(details))}
            </div>
        """

    return f"""
        <div style="
            box-sizing: border-box;
            display: flex;
            align-items: center;
            gap: 11px;
            width: fit-content;
            min-width: 310px;
            margin: 6px 0;
            padding: 8px 14px 8px 10px;
            background: white;
            border: 1px solid #d9d9d9;
            border-left: 4px solid {color};
            border-radius: 7px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            font-family: sans-serif;
        ">
            <img
                src="data:image/png;base64,{logo_data}"
                width="42"
                alt="LlmExpl"
            >
            <div>
                <div style="
                    color: #222;
                    font-size: 15px;
                    font-weight: 600;
                    line-height: 1.25;
                ">
                    {escape(str(title))}
                </div>
                {details_html}
            </div>
        </div>
    """


def display_feedback(title, details=None, status="success"):
    """
    Display a compact and standardized notebook feedback message.
    """

    display(
        HTML(
            feedback_html(
                title=title,
                details=details,
                status=status,
            )
        )
    )