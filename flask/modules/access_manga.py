import sqlite3

class AccessManga():
    def __init__(self) -> None:
        self.dbname = 'eromanga.db'

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def fetch(self):
        self.connect()
        self.cur.execute("SELECT * FROM manga ORDER BY name ASC")
        result = self.cur.fetchall()
        self.close()
        return result

    def search(self, keyword):
        self.connect()
        self.cur.execute("SELECT * FROM manga WHERE name LIKE '%?%'", (keyword,))
        result = self.cur.fetchall()
        self.close()
        return result
