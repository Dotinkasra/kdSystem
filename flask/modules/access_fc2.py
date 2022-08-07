import sqlite3

class AccessFc2():
    def __init__(self) -> None:
        self.dbname = 'fc2.db'

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def fetch(self):
        self.connect()
        self.cur.execute("SELECT * FROM fc2")
        result = self.cur.fetchall()
        self.close()
        return result

    def search(self, keyword: str) -> list:
        if not keyword:
            return []
        self.connect()
        self.cur.execute("SELECT * FROM fc2 WHERE ifnull(name,'') || ifnull(title,'') LIKE ?", ('%' + keyword + '%',))
        result = self.cur.fetchall()
        self.close()
        return result
