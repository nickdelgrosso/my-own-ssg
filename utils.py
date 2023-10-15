from dataclasses import dataclass, field
import sys
from typing import Any, Iterable, NamedTuple
from pathlib import Path
import yaml
from jinja2 import Template
from markdown import markdown
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from tqdm import tqdm

# FileSystemLoader()

def load_config(path: str) -> dict[str, Any]:
    return yaml.load(Path(path).read_text(), yaml.CLoader)

@dataclass
class ContentFile:
    path: Path
    base: str
    content: str = field(repr=False)
    meta: list | dict = field(repr=False)

def render_theme(theme_path: str, content_path: str) -> Iterable[tuple[Path, str]]:
    files = []
    for path in Path(content_path).glob('**/*.md'):
        if path.name == 'README.md':
            continue
        base = path.stem if path.parent == Path(content_path) else path.parent.stem
        head, body = path.read_text().split('---')
        file = ContentFile(
            path=path,
            base=base,
            content=_body_renderers[path.suffix](body),
            meta = _metadata_extractors[path.suffix](head),
        )
        files.append(file)

    
    templates_path = Path(theme_path) / 'templates'
    env = Environment(loader=FileSystemLoader(templates_path), autoescape=select_autoescape())
    templates: dict[str, Template] = {}
    for template_path in templates_path.glob('*.html'):
        templates[template_path.stem] = env.get_template(template_path.name)

    for file in files:
        template = templates[file.base]
        rendered = template.render(content=file.content, **file.meta)
        yield Path(f'{file.path.stem}.html'), rendered
    


_body_renderers = {
    '.md': lambda text: markdown(text.strip()),
}

_metadata_extractors = {
    '.md': lambda text: yaml.load(text, yaml.CLoader)
}



