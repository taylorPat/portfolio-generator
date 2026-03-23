from portfolio import Portfolio, Contact, Location, Link, Section, Skill
from portfolio.pdf import build_portfolio_pdf


portfolio = Portfolio(
    name="Alice Example",
    job_title="Software Engineer",
    about="Experienced in Python and full-stack development.",
    contact=Contact(
        email="alice@example.com",
        location=Location(city="Berlin", postal_code="10115", country="Germany"),
    ),
    links=[Link(name="GitHub", url="https://github.com/alice")],
    image_url=None,
    skills=[
        Skill(name="Programming Languages", attributes=["Python", "SQL", "bash"]),
        Skill(
            name="Frameworks",
            attributes=["FastAPI", "SQLAlchemy", "Alembic", "uv", "ruff", "mypy"],
        ),
    ],
    projects=[],
    cv=[],
)

if __name__ == "__main__":
    build_portfolio_pdf(portfolio, "portfolio.pdf")
