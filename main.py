from os import makedirs
from pprint import pprint
from pathlib import Path
from utils import load_config, get_content_files, get_templates


config = load_config('config.yml')

makedirs('rendered', exist_ok=True)
files = list(get_content_files(base_path='content'))
templates = get_templates(theme_path=Path("themes") / config['theme'])
for file in files:
    template = templates[file.base]
    rendered = template.render(content=file.content, **file.meta)
    Path(f'rendered/{file.path.stem}.html').write_text(rendered)



