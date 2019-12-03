from jinja2 import Template
from .paths import STATIC_DIR


def get_template(template_name):
    path = (STATIC_DIR / template_name).absolute()
    if not path.is_file():
        raise FileNotFoundError(f'Error locating {path} on server.')
    with open(path, 'r') as f:
        return Template(f.read())


class IndexResource:
    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = get_template("../frontend/index.html")
