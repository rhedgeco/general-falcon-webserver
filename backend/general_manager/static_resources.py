from jinja2 import Template
from .paths import FRONTEND_DIR


def _get_template(template_name):
    path = (FRONTEND_DIR / template_name).absolute()
    if not path.is_file():
        raise FileNotFoundError(f'Error locating {path} on server.')
    with open(path, 'r') as f:
        return Template(f.read())


class IndexResource:
    @staticmethod
    def on_get(req, resp):
        resp.content_type = "text/html"
        resp.body = _get_template("../frontend/index.html").render()
