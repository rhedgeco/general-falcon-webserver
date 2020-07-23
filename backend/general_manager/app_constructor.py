import falcon

from falcon_multipart.middleware import MultipartMiddleware
from wsgiref import simple_server
from socketserver import ThreadingMixIn
from pathlib import Path

from .static_resources import IndexResource


class ThreadedWSGIServer(ThreadingMixIn, simple_server.WSGIServer):
    """A WSGI server that has threading enabled."""
    pass


class WebApp:

    def __init__(self, frontend_dir: str, page_404: str = None):
        self._api = falcon.API(middleware=[MultipartMiddleware()])
        self._api.req_options.auto_parse_form_urlencoded = True

        # provide static routing for all calls to webpage frontends
        frontend_dir = Path(frontend_dir).absolute()
        self._api.add_static_route(
            prefix='/',
            directory=str(frontend_dir),
            fallback_filename=str(frontend_dir / page_404) if page_404 else None
        )
        self._api.add_route('/', IndexResource(frontend_dir))

    def get_api_for_testing(self):
        return self._api

    def add_route(self, uri_template, resource, **kwargs):
        if uri_template.startswith('/'):
            uri_template = uri_template[1:]
        uri_template = f'/api/{uri_template}'
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
        location = ('localhost' if host == '0.0.0.0' else host) + ('' if port == 80 else f':{str(port)}')
        print(f'Launching webserver at http://{location}')
        server.serve_forever()
