import sqlite3
from sqlite3 import Connection, Cursor
from threading import Lock


class Client_DB:
    _instance = None
    _lock = Lock()

    def __new__(cls, db_path: str):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize_connection(db_path)
        return cls._instance

    def _initialize_connection(self, db_path: str):
        self.db_path = db_path
        self.connection: Connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor: Cursor = self.connection.cursor()

    def execute(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query: str, params: tuple = ()):
        res = self.cursor.execute(query, params)
        return [dict(row) for row in res.fetchall()]

    def fetchone(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        if self.connection:
            self.connection.close()

def main():
    db = Client_DB('../transport.db')
    #db.execute('DROP TABLE DRIVERS')
    #db.execute('DROP TABLE VEHICLES')
    #db.execute('DROP TABLE ROUTES')

    #db.execute('DELETE FROM VEHICLES')
    #db.execute('DELETE FROM ROUTES')
    #db.execute('DELETE FROM DRIVERS')


    result = db.fetchall('SELECT * FROM VEHICLES')
    for row in result:
        print(row)
    print()

    result = db.fetchall('SELECT * FROM ROUTES')
    for row in result:
        print(row)
    print()

    result = db.fetchall('SELECT * FROM DRIVERS')
    for row in result:
        print(row)


    db.close()

if __name__ == '__main__':
    main()