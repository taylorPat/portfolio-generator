from pathlib import Path
from portfolio.models import Portfolio
import yaml


def load_config(file_path: Path) -> yaml.YAMLObject:
    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
    portfolio_dict = yaml.safe_load(content)
    return validate_file(portfolio_dict=portfolio_dict)


def validate_file(portfolio_dict: dict):
    return Portfolio(**portfolio_dict)
