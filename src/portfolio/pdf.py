from pathlib import Path
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
# TYPOGRAPHY (centralized)
# =========================
TITLE_SIZE = 18
HEADER_SIZE = 13
BODY_SIZE = 9
SMALL_SIZE = 8

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "title",
    parent=styles["Heading1"],
    fontSize=TITLE_SIZE,
    spaceAfter=10,
)

HEADER_STYLE = ParagraphStyle(
    "header",
    parent=styles["Heading2"],
    fontSize=HEADER_SIZE,
    textColor=colors.black,
    spaceBefore=8,
    spaceAfter=6,
)

BODY_STYLE = ParagraphStyle(
    "body",
    parent=styles["Normal"],
    fontSize=BODY_SIZE,
    spaceAfter=4,
)

SMALL_STYLE = ParagraphStyle(
    "small",
    parent=styles["Normal"],
    fontSize=SMALL_SIZE,
    textColor=colors.grey,
    spaceAfter=3,
)

DEFAULT_PDF_FILE_PATH = Path().cwd() / "portfolio.pdf"

def create_pdf(portfolio: Portfolio, filepath: str | None = None) -> Path:
    filepath = filepath or DEFAULT_PDF_FILE_PATH
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

    # Column widths
    left_width = 55 * mm
    right_width = page_width - left_width - 30 * mm  # margins included

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

    template = PageTemplate(id="two_column", frames=[left_frame, right_frame])
    doc.addPageTemplates([template])

    # =========================
    # STORY BUILDING
    # =========================
    story = []

    # =========================
    # LEFT COLUMN
    # =========================
    # Profile Image
    if portfolio.image_url:
        try:
            story.append(Image(portfolio.image_url, width=40 * mm, height=40 * mm))
            story.append(Spacer(1, 10))
        except Exception as e:
            print("ERROR when adding image to pdf")
            print(e)
            pass

    # Contact
    story.append(Paragraph("Contact", HEADER_STYLE))
    story.append(Paragraph(portfolio.contact.email, BODY_STYLE))

    loc = portfolio.contact.location
    story.append(Paragraph(f"{loc.city}, {loc.postal_code}, {loc.country}", BODY_STYLE))

    story.append(Spacer(1, 10))

    # Links
    if portfolio.links:
        story.append(Paragraph("Links", HEADER_STYLE))
        for link in portfolio.links:
            story.append(Paragraph(f"{link.name}: {link.url}", SMALL_STYLE))

    story.append(Spacer(1, 10))

    # Education placeholder
    story.append(Paragraph("Education", HEADER_STYLE))
    story.append(Paragraph("Add education here", SMALL_STYLE))

    # Move to RIGHT COLUMN
    story.append(FrameBreak())

    # =========================
    # RIGHT COLUMN
    # =========================
    # Header
    story.append(Paragraph(portfolio.name, TITLE_STYLE))
    story.append(Paragraph(portfolio.job_title, BODY_STYLE))

    # About
    story.append(Paragraph("About", HEADER_STYLE))
    story.append(Paragraph(portfolio.about, BODY_STYLE))

    # Experience
    story.append(Paragraph("Experience", HEADER_STYLE))

    for company in portfolio.cv:
        story.append(Paragraph(company.name, BODY_STYLE))

        for station in company.stations:
            years = f"{station.start_year}–{station.end_year or 'Present'}"

            story.append(
                Paragraph(
                    f"<b>{station.role}</b> ({years})<br/>{station.activities}",
                    SMALL_STYLE,
                )
            )

    story.append(Spacer(1, 10))

    # SKILLS + PROJECTS (STACKED, safer for pagination)
    story.append(Paragraph("Skills", BODY_STYLE))
    for skill in portfolio.skills:
        attrs = ", ".join(skill.attributes)
        story.append(Paragraph(f"{skill.name} – {attrs}", BODY_STYLE))

    story.append(Paragraph("Projects", BODY_STYLE))
    for project in portfolio.projects:
        attrs = ", ".join(project.attributes)
        story.append(
            Paragraph(
                f"<b>{project.name}</b><br/>{attrs}<br/>{project.link.name}: {project.link.url}",
                BODY_STYLE,
            )
        )

    story.append(Spacer(1, 8))

    doc.build(story)
    return filepath
