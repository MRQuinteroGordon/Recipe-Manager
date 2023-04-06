import sqlite3

'''
Generic db connection provider
'''
class DBbase:

    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self._db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    def close_db(self):
        self._conn.close()

    def reset_database(self):
        raise NotImplementedError()

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn



