from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from .models import Portfolio


# ---------------------------
# PDF generation
# ---------------------------


def build_portfolio_pdf(portfolio: Portfolio, filename: str):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin = 2 * cm
    y = height - margin

    # Header
    c.setFont("Helvetica-Bold", 22)
    c.drawString(margin, y, portfolio.name)
    y -= 25
    c.setFont("Helvetica", 16)
    c.drawString(margin, y, portfolio.job_title)
    y -= 30

    # About
    if portfolio.about:
        c.setFont("Helvetica", 12)
        c.drawString(margin, y, portfolio.about)
        y -= 40

    # Contact
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Contact")
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawString(margin, y, f"Email: {portfolio.contact.email}")
    y -= 15
    loc = portfolio.contact.location
    c.drawString(margin, y, f"Location: {loc.city}, {loc.postal_code}, {loc.country}")
    y -= 25

    # Links
    if portfolio.links:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "Links")
        y -= 18
        c.setFont("Helvetica", 11)
        for link in portfolio.links:
            c.drawString(margin, y, f"{link.name}: {link.url}")
            y -= 15
        y -= 10

    # Skills
    if portfolio.skills:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "Skills")
        c.setFont("Helvetica", 11)
        for skill in portfolio.skills:
            y -= 18
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin + 10, y, skill.name)
            y -= 15
            c.setFont("Helvetica", 11)
            c.drawString(margin + 20, y, ", ".join(skill.attributes))
            y -= 5
        y -= 10

    # Projects
    if portfolio.projects:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "Projects")
        y -= 18
        c.setFont("Helvetica", 11)
        for project in portfolio.projects:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin + 10, y, project.name)
            y -= 15
            c.setFont("Helvetica", 11)
            for section in project.sections:
                c.drawString(
                    margin + 20, y, f"{section.name}: {', '.join(section.attributes)}"
                )
                c.drawString(
                    margin + 20,
                    y - 12,
                    f"Link: {section.link.name} ({section.link.url})",
                )
                y -= 28
            y -= 5
        y -= 10

    # CV / Work history
    if portfolio.cv:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "Work Experience")
        y -= 18
        c.setFont("Helvetica", 11)
        for company in portfolio.cv:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin + 10, y, company.name)
            y -= 15
            c.setFont("Helvetica", 11)
            for station in company.stations:
                c.drawString(
                    margin + 20,
                    y,
                    f"{station.role} ({station.start_year} - {station.end_year})",
                )
                y -= 12
                c.drawString(margin + 25, y, f"{station.activities}")
                y -= 20
            y -= 5

    c.save()
