import falcon

from falcon_multipart.middleware import MultipartMiddleware
from wsgiref import simple_server

from .paths import STATIC_DIR
from .static_resources import IndexResource


class WebApp:

    def __init__(self):
        self._api = falcon.API(middleware=[MultipartMiddleware])

        # provide static routing for all calls to webpage frontends
        self._api.add_static_route(prefix='/', directory=str(STATIC_DIR))
        self._api.add_route('/', IndexResource)

    def add_route(self, location_name: str, resource):
        self._api.add_route(f'/api/{location_name}', resource)

    def launch_webserver(self, host: str = '0.0.0.0', port: int = 80):
        print('creating webserver...')
        server = simple_server.make_server(
            host=host,
            port=port,
            app=self._api
        )

        # construct nice print for hosting on the default host and port
        location = ('localhost' if host == '0.0.0.0' else host) + ('' if port == 80 else port)
        print(f'Launching webserver at http://{location}')
        server.serve_forever()
