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



def get_templates(theme_path) -> dict[str, Template]:
    templates_path = Path(theme_path) / 'templates'
    env = Environment(loader=FileSystemLoader(templates_path), autoescape=select_autoescape())
    templates: dict[str, Template] = {}
    for template_path in templates_path.glob('*.html'):
        templates[template_path.stem] = env.get_template(template_path.name)
    return templates


def get_content_files(base_path) -> Iterable[ContentFile]:
    for path in Path(base_path).glob('**/*.md'):
        if path.name == 'README.md':
            continue
        base = path.stem if path.parent == Path(base_path) else path.parent.stem
        head, body = path.read_text().split('---')
        file = ContentFile(
            path=path,
            base=base,
            content=_body_renderers[path.suffix](body),
            meta = _metadata_extractors[path.suffix](head),
        )
        yield file
    


_body_renderers = {
    '.md': lambda text: markdown(text.strip()),
}

_metadata_extractors = {
    '.md': lambda text: yaml.load(text, yaml.CLoader)
}



