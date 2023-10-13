from os import makedirs
from pathlib import Path
from utils import load_config, render_theme


config = load_config('config.yml')

rendered = render_theme(theme_path=config['theme'], content_path='content')
makedirs('rendered', exist_ok=True)
for path, html in rendered:
    (Path('rendered') / path).write_text(html)



