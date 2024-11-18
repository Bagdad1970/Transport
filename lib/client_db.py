import sqlite3
from sqlite3 import Connection, Cursor
from threading import Lock

class Client_DB:
    _instance = None
    _lock = Lock()  # для поточной безопасности

    def __new__(cls, db_path: str):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize_connection(db_path)
        return cls._instance

    def _initialize_connection(self, db_path: str):
        """Инициализация подключения к базе данных."""
        self.db_path = db_path
        self.connection: Connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # позволяет обращаться к колонкам по имени
        self.cursor: Cursor = self.connection.cursor()

    def execute(self, query: str, params: tuple = ()):
        """Выполнение SQL-запроса."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query: str, params: tuple = ()):
        """Получение всех результатов из SQL-запроса."""
        res = self.cursor.execute(query, params)
        return [dict(row) for row in res.fetchall()]

    def fetchone(self, query: str, params: tuple = ()):
        """Получение одного результата из SQL-запроса."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        """Закрытие подключения к базе данных."""
        if self.connection:
            self.connection.close()

def main():
    db = Client_DB('transport.db')
    """
    db.execute('DROP TABLE DRIVERS')
    db.execute('DROP TABLE VEHICLES')
    db.execute('DROP TABLE ROUTES')
    """

    result = db.fetchall('SELECT * FROM DRIVERS')
    for row in result:
        print(row)


    db.close()

if __name__ == '__main__':
    main()