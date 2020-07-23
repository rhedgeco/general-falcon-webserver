import os
from pathlib import Path

import falcon

from falcon_multipart.middleware import MultipartMiddleware
from wsgiref import simple_server
from socketserver import ThreadingMixIn
from pathlib import Path

from backend.general_manager.web_paths import WebPathStructure
from backend.general_manager.static_resources import StaticResource


class ThreadedWSGIServer(ThreadingMixIn, simple_server.WSGIServer):
    """A WSGI server that has threading enabled."""
    pass


class WebApp:

    def __init__(self, web_path: WebPathStructure = WebPathStructure()):
        self._api = falcon.API(middleware=[MultipartMiddleware()])
        self._api.req_options.auto_parse_form_urlencoded = True
        self.web_path = web_path

        # add static routing functionality
        self._api.add_static_route(prefix='/', directory=str(web_path.frontend_dir_absolute), downloadable=True)
        self._api.add_route('/', StaticResource(Path(web_path.frontend_dir_absolute) / 'index.html'))

        self._populate_frontend()

    def get_api_for_testing(self):
        return self._api

    def add_route(self, uri_template, resource, **kwargs):
        if not uri_template.startswith('/'):
            uri_template = f'/{uri_template}'
        uri_template = f'/api{uri_template}'
        print(f'Added api location {uri_template}')
        self._api.add_route(uri_template, resource, **kwargs)

    def launch_webserver(self, host: str = '0.0.0.0', port: int = 80):
        print('creating webserver...')
        server = simple_server.make_server(
            host=host,
            port=port,
            app=self._api,
            server_class=ThreadedWSGIServer
        )

        # construct nice print for hosting on the default host and port
        location = f'{"localhost" if host == "0.0.0.0" else host}{"" if port == 80 else f":{port}"}'
        print(f'Launching webserver at http://{location}')
        server.serve_forever()

    def _populate_frontend(self):
        self._step_and_add_frontend(self.web_path.frontend_dir_absolute)

    def _step_and_add_frontend(self, path):
        for f in os.listdir(path):
            full_path = Path(path) / f
            if full_path.is_dir() and not full_path.is_symlink():
                self._step_and_add_frontend(full_path)
            elif full_path.suffix.lower() == '.html':
                relative_path = full_path.relative_to(self.web_path.frontend_dir_absolute)
                api_route = relative_path.with_suffix('')
                self._api.add_route(
                    f'/{api_route}',
                    StaticResource(Path(self.web_path.frontend_dir_absolute) / relative_path)
                )
