from backend.general_manager.app_constructor import WebApp
from backend.general_manager.databases import SqliteDatabase
from backend.test_click_api import TestClickApi

app = WebApp()
database = SqliteDatabase(
    database_name='general-falcon-database',
    database_config='CREATE TABLE IF NOT EXISTS button_clicks (amount int NOT NULL);'
                    'INSERT INTO button_clicks (amount) '
                    'SELECT 0 WHERE NOT EXISTS(SELECT 1 FROM button_clicks WHERE ROWID = 1);'
)
app.add_route('test_click', TestClickApi(database))
app.launch_webserver()
