from os import makedirs, rmdir
from pathlib import Path
from yaml import load, CLoader
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

content_paths = list(Path('.').glob('content/*.md'))

makedirs('rendered', exist_ok=True)

Path('rendered/index.html')
index_template = env.get_template('index.html')
rendered = index_template.render(paths=[f"{path.stem}.html" for path in content_paths])
Path('rendered/index.html').write_text(rendered)

page_template = env.get_template('page.html')
for path in content_paths:
    text = path.read_text()
    head, body = text.split('---')
    content = body.strip()
    meta = load(head, CLoader)

    rendered = page_template.render(content=content, **meta)
    Path(f'rendered/{path.stem}.html').write_text(rendered)


