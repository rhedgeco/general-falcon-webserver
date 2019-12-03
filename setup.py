# venv is already set up in this project. Use this for setting up an extrenal environment

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
