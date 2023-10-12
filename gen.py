from os import makedirs, rmdir
from pathlib import Path
from yaml import load, CLoader
from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import markdown

config = load(Path("config.yml").read_text(), CLoader)
env = Environment(loader=PackageLoader(config['template']), autoescape=select_autoescape())

makedirs('rendered', exist_ok=True)

for template_path in Path('app/templates').glob('*.html'):
    stem = template_path.stem
    template = env.get_template(template_path.name)

    content_paths = Path('.').glob(f'{stem}/*.md') if Path(stem).is_dir() else [Path(f"{stem}.md")]
    
    for path in content_paths:
        head, body = path.read_text().split('---')
        content = markdown(body.strip())
        meta = load(head, CLoader)

        rendered = template.render(content=content, **meta)
        Path(f'rendered/{path.stem}.html').write_text(rendered)


