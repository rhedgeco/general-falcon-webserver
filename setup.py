from setuptools import setup

setup(
    name='general-falcon-webserver',
    version='1.0.0',
    install_requires=[
        "falcon",
        "falcon-cors",
        "falcon-multipart",
        "PyJWT",
        "pytest",
        "msgpack",
        "jinja2"
    ]
)
