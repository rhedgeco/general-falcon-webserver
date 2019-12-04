from .general_manager.databases import SqliteDatabase


def get_clicks(database: SqliteDatabase):
    return database.fetchone_query('SELECT 1 FROM button_clicks WHERE ROWID = 1')


def add_click(database: SqliteDatabase):
    database.send_query('UPDATE button_clicks SET amount = (amount+1) WHERE ROWID = 1')
