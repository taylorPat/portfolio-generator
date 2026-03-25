from pathlib import Path
import shutil
from importlib.resources import files

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import Portfolio

# Use files from importlib.resources because relative imports break after installation
_PACKAGE_ROOT_FOLDER_PATH = files("portfolio")  
DEFAULT_TEMPLATE_FOLDER_PATH = _PACKAGE_ROOT_FOLDER_PATH / "data" / "FE" / "templates"
DEFAULT_PROFILE_YAML_PATH = Path().cwd() / "profile.yml"
DEFAULT_HTML_TEMPLATE_FILE_NAME = "index.html.jinja"
DEFAULT_DOCS_FOLDER_PATH = Path().cwd() / "docs"
DEFAULT_STATICS_FILE_FOLDER_PATH = _PACKAGE_ROOT_FOLDER_PATH / "data" / "FE" / "static"


def create_html(
    portfolio: Portfolio,
    template_folder_path: Path | None = None,
    html_template_file_name: str | None = None,
    static_files_folder_path: str | None = None,
    docs_folder_path: Path | None = None,
):
    template_folder_path = template_folder_path or DEFAULT_TEMPLATE_FOLDER_PATH
    html_template_file_name = html_template_file_name or DEFAULT_HTML_TEMPLATE_FILE_NAME
    html = render_template(
        yaml_data=portfolio.model_dump(),
        template_folder_path=template_folder_path,
        html_template_file_name=html_template_file_name,
    )

    docs_folder_path = docs_folder_path or DEFAULT_DOCS_FOLDER_PATH
    write_output(html=html, docs_folder_path=docs_folder_path)
    static_files_folder_path = static_files_folder_path or DEFAULT_STATICS_FILE_FOLDER_PATH
    copy_static(
        docs_folder_path=docs_folder_path,
        static_file_folder_path=static_files_folder_path,
    )
    return docs_folder_path

def render_template(
    yaml_data, template_folder_path: Path, html_template_file_name: str
):
    env = Environment(
        loader=FileSystemLoader(searchpath=str(template_folder_path)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(name=html_template_file_name)
    return template.render(yaml_data)


def write_output(html: str, docs_folder_path: Path):
    _create_empty_docs_dir(output_path=docs_folder_path)
    html_file = docs_folder_path / "index.html"
    with html_file.open("w", encoding="utf-8") as file:
        file.write(html)


def _create_empty_docs_dir(output_path: Path):
    shutil.rmtree(path=output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=False)


def copy_static(docs_folder_path: Path, static_file_folder_path: Path):
    static_dst = docs_folder_path / "static"
    shutil.copytree(static_file_folder_path, static_dst)