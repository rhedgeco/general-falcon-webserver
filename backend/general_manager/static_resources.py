import os
from pathlib import Path

from jinja2 import Template


class StaticResource:
    def __init__(self, path):
        self.path = str(path)

    def on_get(self, req, resp):
        suffix = os.path.splitext(self.path)[1]
        resp.content_type = resp.options.static_media_types.get(
            suffix,
            'application/octet-stream'
        )

        path = Path(self.path).absolute()
        if not path.is_file():
            raise FileNotFoundError(f'Error locating {self.path} on server.')
        with open(self.path, 'r') as f:
            resp.body = Template(f.read()).render()
