from pathlib import Path
from portfolio.models import Portfolio
import yaml


def load_data(file_path: Path) -> yaml.YAMLObject:
    print(f"Size: {file_path.stat().st_size if file_path.exists() else 'N/A'}")

    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
    return yaml.safe_load(content)


def validate_file(portfolio: dict):
    return Portfolio(**portfolio)
