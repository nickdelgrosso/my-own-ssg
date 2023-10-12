from os import makedirs, rmdir
from pathlib import Path
from yaml import load, CLoader
from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import markdown

config = load(Path("config.yml").read_text(), CLoader)
env = Environment(loader=PackageLoader(config['template']), autoescape=select_autoescape())

makedirs('rendered', exist_ok=True)

for template_path in Path(f'{config["template"]}/templates').glob('*.html'):
    stem = template_path.stem
    template = env.get_template(template_path.name)

    base = Path('content')
    content_paths = paths if (paths := list(base.glob(f'{stem}/*.md'))) else [base.joinpath(f"{stem}.md")]
    
    for path in content_paths:
        head, body = path.read_text().split('---')
        content = markdown(body.strip())
        meta = load(head, CLoader)

        rendered = template.render(content=content, **meta)
        Path(f'rendered/{path.stem}.html').write_text(rendered)


