from pathlib import Path
from enum import Enum
from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Image,
    FrameBreak,
)

from .models import Portfolio


# =========================
# TYPOGRAPHY
# =========================
TITLE_SIZE = 18
HEADER_SIZE = 13
BODY_SIZE = 9
SMALL_SIZE = 8

DEFAULT_PDF_FILE_PATH = Path().cwd() / "portfolio.pdf"


# =========================
# THEME SYSTEM
# =========================
class ThemeColor(Enum):
    BLUE = "#2E86AB"
    GREEN = "#2ECC71"
    DARK = "#2C3E50"
    RED = "#E74C3C"
    PURPLE = "#8E44AD"


class AccentMode(Enum):
    SAME = "same"
    LIGHTER = "lighter"
    DARKER = "darker"


@dataclass
class PdfTheme:
    primary: colors.Color
    accent: colors.Color
    left_bg: colors.Color
    left_text: colors.Color
    right_header: colors.Color


# =========================
# COLOR UTILITIES
# =========================
def hex_to_color(hex_str: str) -> colors.Color:
    return colors.HexColor(hex_str)


def adjust_color(col: colors.Color, factor: float) -> colors.Color:
    """
    factor > 1 => lighter
    factor < 1 => darker
    """
    r = min(max(col.red * factor, 0), 1)
    g = min(max(col.green * factor, 0), 1)
    b = min(max(col.blue * factor, 0), 1)
    return colors.Color(r, g, b)


def get_contrast_color(bg_color: colors.Color) -> colors.Color:
    luminance = 0.299 * bg_color.red + 0.587 * bg_color.green + 0.114 * bg_color.blue
    return colors.white if luminance < 0.5 else colors.black


def build_theme(color: ThemeColor, accent_mode: AccentMode) -> PdfTheme:
    primary = hex_to_color(color.value)

    if accent_mode == AccentMode.LIGHTER:
        accent = adjust_color(primary, 1.3)
    elif accent_mode == AccentMode.DARKER:
        accent = adjust_color(primary, 0.7)
    else:
        accent = primary

    return PdfTheme(
        primary=primary,
        accent=accent,
        left_bg=primary,
        left_text=get_contrast_color(primary),
        right_header=accent,
    )


# =========================
# STYLES
# =========================
def create_styles(theme: PdfTheme):
    base = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Heading1"],
            fontSize=TITLE_SIZE,
            spaceAfter=10,
            textColor=colors.black,
        ),
        "header_left": ParagraphStyle(
            "header_left",
            parent=base["Heading2"],
            fontSize=HEADER_SIZE,
            textColor=theme.left_text,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "header_right": ParagraphStyle(
            "header_right",
            parent=base["Heading2"],
            fontSize=HEADER_SIZE,
            textColor=theme.right_header,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            parent=base["Normal"],
            fontSize=BODY_SIZE,
            textColor=theme.left_text,
            spaceAfter=4,
        ),
        "body_right": ParagraphStyle(
            "body_right",
            parent=base["Normal"],
            fontSize=BODY_SIZE,
            spaceAfter=4,
        ),
        "small_left": ParagraphStyle(
            "small_left",
            parent=base["Normal"],
            fontSize=SMALL_SIZE,
            textColor=theme.left_text,
            spaceAfter=3,
        ),
        "small_right": ParagraphStyle(
            "small_right",
            parent=base["Normal"],
            fontSize=SMALL_SIZE,
            textColor=colors.grey,
            spaceAfter=3,
        ),
    }


# =========================
# BACKGROUND DRAWING
# =========================
def draw_background(theme: PdfTheme, left_width):
    def _draw(canvas, doc):
        canvas.saveState()

        # Left panel
        canvas.setFillColor(theme.left_bg)
        canvas.rect(
            doc.leftMargin,
            doc.bottomMargin,
            left_width,
            doc.height,
            stroke=0,
            fill=1,
        )

        canvas.restoreState()

    return _draw


# =========================
# MAIN FUNCTION
# =========================
def create_pdf(
    portfolio: Portfolio,
    filepath: str | None = None,
    theme_color: ThemeColor = ThemeColor.BLUE,
    accent_mode: AccentMode = AccentMode.SAME,
) -> Path:
    filepath = filepath or DEFAULT_PDF_FILE_PATH

    theme = build_theme(theme_color, accent_mode)
    S = create_styles(theme)

    # =========================
    # DOCUMENT SETUP
    # =========================
    doc = BaseDocTemplate(
        str(filepath),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    page_width, page_height = A4

    left_width = 55 * mm
    right_width = page_width - left_width - 30 * mm

    left_frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        left_width,
        page_height - doc.topMargin - doc.bottomMargin,
        id="left",
    )

    right_frame = Frame(
        doc.leftMargin + left_width + 10 * mm,
        doc.bottomMargin,
        right_width - 10 * mm,
        page_height - doc.topMargin - doc.bottomMargin,
        id="right",
    )

    template = PageTemplate(
        id="two_column",
        frames=[left_frame, right_frame],
        onPage=draw_background(theme, left_width),
    )

    doc.addPageTemplates([template])

    story = []

    # =========================
    # LEFT COLUMN
    # =========================
    if portfolio.image_url:
        try:
            story.append(Image(portfolio.image_url, width=40 * mm, height=40 * mm))
            story.append(Spacer(1, 10))
        except Exception:
            pass

    story.append(Paragraph("Contact", S["header_left"]))
    story.append(Paragraph(portfolio.contact.email, S["body_left"]))

    loc = portfolio.contact.location
    story.append(
        Paragraph(f"{loc.city}, {loc.postal_code}, {loc.country}", S["body_left"])
    )

    story.append(Spacer(1, 10))

    if portfolio.links:
        story.append(Paragraph("Links", S["header_left"]))
        for link in portfolio.links:
            story.append(Paragraph(f"{link.name}: {link.url}", S["small_left"]))

    story.append(Spacer(1, 10))

    story.append(Paragraph("Education", S["header_left"]))
    story.append(Paragraph("Add education here", S["small_left"]))

    story.append(FrameBreak())

    # =========================
    # RIGHT COLUMN
    # =========================
    story.append(Paragraph(portfolio.name, S["title"]))
    story.append(Paragraph(portfolio.job_title, S["body_right"]))

    story.append(Paragraph("About", S["header_right"]))
    story.append(Paragraph(portfolio.about, S["body_right"]))

    story.append(Paragraph("Experience", S["header_right"]))

    for company in portfolio.cv:
        story.append(Paragraph(company.name, S["body_right"]))

        for station in company.stations:
            years = f"{station.start_year}–{station.end_year or 'Present'}"

            story.append(
                Paragraph(
                    f"<b>{station.role}</b> ({years})<br/>{station.activities}",
                    S["small_right"],
                )
            )

    story.append(Spacer(1, 10))

    story.append(Paragraph("Skills", S["header_right"]))
    for skill in portfolio.skills:
        attrs = ", ".join(skill.attributes)
        story.append(Paragraph(f"<b>{skill.name}</b>", S["body_right"]))
        story.append(Paragraph(attrs, S["body_right"]))

    story.append(Paragraph("Projects", S["header_right"]))
    for project in portfolio.projects:
        attrs = ", ".join(project.attributes)
        story.append(
            Paragraph(
                f"<b>{project.name}</b><br/>{attrs}",
                S["body_right"],
            )
        )
        story.append(
            Paragraph(
                f"<link href={project.link.url}>{project.link.url}</link><br/><br/>",
                S["small_right"],
            )
        )

    doc.build(story)
    return filepath
