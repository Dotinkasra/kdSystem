import sqlite3

class AccessManga():
    def __init__(self) -> None:
        self.dbname = 'eromanga.db'

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def insert(self, name: str, artists: str, series: str, original: str):
        self.connect()
        if self.isEmptyOrSpace(name):
            return

        artists = None if self.isEmptyOrSpace(artists) else artists
        series = None if self.isEmptyOrSpace(series) else series
        original = None if self.isEmptyOrSpace(original) else original
        print(f'{name}')
        try:
            result = self.cur.execute(
                "INSERT INTO manga(name, artists, series, original) VALUES(?,?,?,?)",
                (name, artists, series, original)
            )
            self.conn.commit()
        except:
            result = None
        finally:
            self.close()
            return result

    def fetch(self) -> list:
        self.connect()
        self.cur.execute("SELECT * FROM manga ORDER BY name ASC")
        result = self.cur.fetchall()
        self.close()
        return result

    def search(self, keyword: str) -> list:
        if not keyword:
            return []
        self.connect()
        self.cur.execute("SELECT * FROM manga WHERE ifnull(name,'') || ifnull(artists,'') || ifnull(series,'') || ifnull(original,'') LIKE ?", ('%' + keyword + '%',))
        result = self.cur.fetchall()
        self.close()
        return result

    def isEmptyOrSpace(self, s: str) -> bool:
        if (not type(s) is str) or (s is None) or (len(s) == 0) or (s == ''):
            return True
        return False
