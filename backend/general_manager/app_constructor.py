import falcon

from falcon_multipart.middleware import MultipartMiddleware
from wsgiref import simple_server
from pathlib import Path

from .static_resources import IndexResource

class WebApp:

    def __init__(self, frontend_dir: str, page_404: str = None):
        self._api = falcon.API(middleware=[MultipartMiddleware()])

        # provide static routing for all calls to webpage frontends
        frontend_dir = Path(frontend_dir).absolute()
        self._api.add_static_route(
            prefix='/',
            directory=str(frontend_dir),
            fallback_filename=str(frontend_dir/page_404) if page_404 else None
        )
        self._api.add_route('/', IndexResource(frontend_dir))

    def add_route(self, location_name: str, resource):
        if location_name.startswith('/'):
            location_name = location_name[1:]
        location_name = f'/api/{location_name}'
        print(f'Added api location {location_name}')
        self._api.add_route(location_name, resource)

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
