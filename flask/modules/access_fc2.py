import sqlite3, pathlib

class AccessFc2():
    def __init__(self) -> None:
        self.dbname = 'fc2.db'

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def fetch(self) -> list:
        self.connect()
        self.cur.execute("SELECT * FROM fc2")
        result = self.cur.fetchall()
        self.close()
        return [m for m in result]

    def search(self, keyword: str) -> list:
        if not keyword:
            return []
        self.connect()
        self.cur.execute("SELECT * FROM fc2 WHERE ifnull(name,'') || ifnull(title,'') LIKE ?", ('%' + keyword + '%',))
        result = self.cur.fetchall()
        self.close()
        return [m for m in result]

    def get_movies(self, id: str) -> dict:
        self.connect()
        self.cur.execute("SELECT * FROM fc2 WHERE id = ?", (id,))
        result = self.cur.fetchall()
        self.close()
        title = result[0][1]
        m_mkv = [title + "/" + m.name for m in pathlib.Path('static/movies/' + title).glob('*.mkv')]
        m_mp4 = [title + "/" + m.name for m in pathlib.Path('static/movies/' + title).glob('*.mp4')]
        m_tmp = []
        m_tmp.extend(m_mkv)
        m_tmp.extend(m_mp4)
        return {'title': result[0][2], 'movies': m_tmp}
