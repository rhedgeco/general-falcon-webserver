import json

from backend.general_manager.databases import SqliteDatabase
from .test_database_manager import get_clicks, add_click


class TestClickApi:
    def __init__(self, database: SqliteDatabase):
        self.database = database

    # gets the number of clicks for a button
    def on_get(self, req, resp):
        obj = get_clicks(self.database)
        resp.body = json.dumps(obj, ensure_ascii=True)

    def on_put(self, req, resp):
        add_click(self.database)
