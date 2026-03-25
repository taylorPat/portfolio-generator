from pathlib import Path
from typing import Annotated

import typer
from rich import print as rprint

from portfolio.pdf import create_pdf
from portfolio.validate import load_data, validate_file
from portfolio.generate_html import build

app = typer.Typer()


def get_profile_yaml_file(value: Path):
    """Searching for default files"""
    DEFAULT_PROFILE_YML_PATH = Path().cwd() / "profile.yml"
    DEFAULT_PROFILE_YAML_PATH = Path().cwd() / "profile.yaml"
    if value is None:
        if DEFAULT_PROFILE_YAML_PATH.is_file():
            return DEFAULT_PROFILE_YAML_PATH
        elif DEFAULT_PROFILE_YML_PATH.is_file():
            return DEFAULT_PROFILE_YML_PATH
        else:
            paths = Path().cwd().glob(pattern="*.ya?ml")
            if len(paths) > 1:
                raise typer.BadParameter("More than one yaml file found.")
            return paths[0]
    elif value.is_file():
        return value
    else:
        typer.BadParameter(message="Please provide a yaml file!")


@app.command()
def create(
    profile_yaml_path: Annotated[
        Path | None, typer.Option(callback=get_profile_yaml_file)
    ] = None,
    html: Annotated[bool, typer.Option("--html", help="Generate HTML output")] = False,
    pdf: Annotated[bool, typer.Option("--pdf", help="Generate HTML output")] = False,
):
    if not html and not pdf:
        rprint("[red][SUCCESS][/red] Please provide at least one of --html or --pdf")
    else:
        portfolio = validate(profile_yaml_path=profile_yaml_path)
        if html:
            docs_folder_path = build(portfolio=portfolio)
            rprint(f"[green][SUCCESS][/green] Save portfolio as html ({docs_folder_path})")
        if pdf:
            filepath = create_pdf(portfolio=portfolio)
            rprint(f"[green][SUCCESS][/green] Save portfolio as pdf ({filepath})")


@app.command()
def validate(
    profile_yaml_path: Annotated[
        Path | None, typer.Option(callback=get_profile_yaml_file)
    ] = None,
):
    dic = load_data(file_path=profile_yaml_path)
    rprint("[green][SUCCESS][/green] Validate yaml configuration")
    return validate_file(portfolio=dic)
