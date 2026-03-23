from pathlib import Path
from typing import Annotated
import typer

from portfolio.generate_html import (
    DEFAULT_DOCS_FOLDER_PATH,
    DEFAULT_HTML_TEMPLATE_FILE_NAME,
    DEFAULT_PROFILE_YAML_PATH,
    DEFAULT_STATICS_FILE_FOLDER_PATH,
    DEFAULT_TEMPLATE_FOLDER_PATH,
    build,
)

app = typer.Typer()


@app.command()
def create(
    profile_yaml_path: Annotated[Path, typer.Option()] = DEFAULT_PROFILE_YAML_PATH,
    template_folder_path: Annotated[
        Path, typer.Option()
    ] = DEFAULT_TEMPLATE_FOLDER_PATH,
    html_template_file_name: Annotated[
        str, typer.Option()
    ] = DEFAULT_HTML_TEMPLATE_FILE_NAME,
    static_files_folder_path: Annotated[
        Path, typer.Option()
    ] = DEFAULT_STATICS_FILE_FOLDER_PATH,
    docs_folder_path: Annotated[Path, typer.Option()] = DEFAULT_DOCS_FOLDER_PATH,
):
    print(f"Profile yaml path: {profile_yaml_path}")
    print(f"Template folder path: {template_folder_path}")
    print(f"Html template file: {html_template_file_name}")
    build(
        profile_yaml_path=profile_yaml_path,
        template_folder_path=template_folder_path,
        html_template_file_name=html_template_file_name,
        static_files_folder_path=static_files_folder_path,
        docs_folder_path=docs_folder_path,
    )
    print("DONE")
