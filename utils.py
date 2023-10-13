from typing import Any, Iterable
from pathlib import Path
import yaml
from jinja2 import Template
from markdown import markdown
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from tqdm import tqdm


def load_config(path: str) -> dict[str, Any]:
    return yaml.load(Path(path).read_text(), yaml.CLoader)


def render_theme(theme_path: str, content_path: str) -> Iterable[tuple[Path, str]]:
    _theme_path = Path(theme_path)
    _content_path = Path(content_path)
    env = Environment(loader=PackageLoader(_theme_path.name), autoescape=select_autoescape())
    for template_path in (Path(_theme_path) / 'templates').glob('*.html'):
        stem = template_path.stem
        template = env.get_template(template_path.name)
        content_paths = paths if (paths := list(_content_path.glob(f'{stem}/*'))) else [_content_path.joinpath(f"{stem}.md")]
        for path in tqdm(content_paths, desc=stem):
            rendered = _render(path, template=template)
            path = Path(f'{path.stem}.html')
            yield path, rendered
    


_body_renderers = {
    '.md': lambda text: markdown(text.strip()),
}

_metadata_extractors = {
    '.md': lambda text: yaml.load(text, yaml.CLoader)
}

def _render(content_path: Path, template: Template) -> str:
    head, body = content_path.read_text().split('---')
    content = _body_renderers[content_path.suffix](body)
    meta = _metadata_extractors[content_path.suffix](head)
    rendered = template.render(content=content, **meta)
    return rendered


