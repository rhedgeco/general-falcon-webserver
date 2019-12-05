from jinja2 import Template
from pathlib import Path


def _get_template(path):
    if not path.is_file():
        raise FileNotFoundError(f'Error locating {path} on server.')
    with open(path, 'r') as f:
        return Template(f.read())


class IndexResource:
    def __init__(self, frontend_dir):
        self.frontend_dir = Path(frontend_dir).absolute()

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = _get_template((self.frontend_dir / 'index.html').absolute()).render()
