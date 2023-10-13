from os import makedirs
from pathlib import Path
from utils import load_config, render_theme


config = load_config('config.yml')

makedirs('rendered', exist_ok=True)
for path, html in render_theme(theme_path=Path("themes") / config['theme'], content_path='content'):
    (Path('rendered') / path).write_text(html)



