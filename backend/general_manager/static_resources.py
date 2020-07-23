import falcon
from jinja2 import Template
from pathlib import Path


def get_template(path: str):
    path = Path(path).absolute()
    if not path.is_file():
        raise FileNotFoundError(f'Error locating {path} on server.')
    with open(path, 'r') as f:
        return Template(f.read())


class IndexResource:
    def __init__(self, frontend_dir: str):
        self.frontend_dir = Path(frontend_dir).absolute()

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = get_template(self.frontend_dir / 'index.html').render()


class StaticResource:
    def __init__(self, frontend_dir, page_404: str = None):
        self.frontend_dir = Path(frontend_dir)
        self.handle_404_page = (frontend_dir/page_404).absolute() if page_404 else None

    def on_get(self, req, resp, filename):
        file = Path(filename).absolute()
        if file.is_file() and self.handle_404_page:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = get_template(self.handle_404_page).render()
            return

        resp.status = falcon.HTTP_OK
        resp.body = get_template(file).render()
