import sqlite3, pathlib
from modules.module import BasicModules

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
        if BasicModules.is_empty_or_null(name):
            return

        artists = None if BasicModules.is_empty_or_null(artists) else artists
        series = None if BasicModules.is_empty_or_null(series) else series
        original = None if BasicModules.is_empty_or_null(original) else original
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
        print(keyword)
        if not keyword:
            return []
        self.connect()
        self.cur.execute("SELECT * FROM manga WHERE ifnull(name,'') || ifnull(artists,'') || ifnull(series,'') || ifnull(original,'') LIKE ?", ('%' + keyword + '%',))
        result = self.cur.fetchall()
        self.close()
        return [m for m in result]

    def get_images(self, id: str) -> dict:
        if not id:
            return []
        self.connect()
        self.cur.execute("SELECT * FROM manga WHERE id = ?", (id,))
        result = self.cur.fetchall()
        self.close()
        title = result[0][1]
        print(result)
        p_png = [p.name for p in pathlib.Path('static/images/' + title).glob('*.png')]
        p_jpg = [p.name for p in pathlib.Path('static/images/' + title).glob('*.jpg')]
        p_jpeg = [p.name for p in pathlib.Path('static/images/' + title).glob('*.jpeg')]
        p_webp = [p.name for p in pathlib.Path('static/images/' + title).glob('*.webp')]
        p_tmp = []
        p_tmp.extend(p_png)
        p_tmp.extend(p_jpg)
        p_tmp.extend(p_jpeg)
        p_tmp.extend(p_webp)
        return {'title': title, 'images': p_tmp}