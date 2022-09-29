import sqlite3, pathlib
from unicodedata import name
from modules.module import BasicModules

class AccessManga():
    def __init__(self) -> None:
        self.dbname = 'eromanga.db'
        self.main_sql = """
            SELECT 
                manga.*, GROUP_CONCAT(tag.name) as tag_name
            FROM 
                manga
            LEFT JOIN 
                tag_manga
            ON 
                manga.id = tag_manga.manga_id
            LEFT JOIN 
                tag
            ON 
                tag_manga.tag_id = tag.id

        """

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
        self.cur.execute(
            f"{self.main_sql} GROUP BY manga.name"
        )
        result = self.cur.fetchall()
        self.close()
        return result

    def get_tag(self) -> list:
        self.connect()
        self.cur.execute("SELECT * FROM tag")
        result = self.cur.fetchall()
        self.close()
        return result

    def search(
        self,
        keyword: str = None,
        title: str = None,
        artists: str = None,
        series: str = None,
        original: str = None,
        tags: list[str] = None
    ) -> list:
        if keyword is None and not any((title, artists, series, original, tags)):
            return []

        self.connect()
        result = []
        sql = self.main_sql
        if keyword is not None:
            sql += f"""

                WHERE
                    ifnull(manga.name,'') || ifnull(manga.artists,'') || ifnull(manga.series,'') || ifnull(manga.original,'') LIKE ?
                GROUP BY
                    manga.name
                ORDER BY 
                    manga.name ASC
                """
            param = (f'%{keyword}%',)
            print(sql)
            self.cur.execute(sql, param)
            r = self.cur.fetchall()
            if not (r is None and len(r) == 0):
                result.extend(r)
            return result

        sql = self.main_sql
        param = []
        if any((title, artists, series, original)):
            sql += f""" 
            WHERE

            """

            if title is not None:
                sql += "manga.name LIKE ? AND "
                param.append(f'%{title}%')
            if artists is not None:
                sql += "manga.artists LIKE ? AND "
                param.append(f'%{artists}%')
            if series is not None:
                sql += "manga.series LIKE ? AND "
                param.append(f'%{series}%')
            if original is not None:
                sql += "manga.original LIKE ? AND "
                param.append(f'%{original}%')

        sql = f"""
            {sql[:-4]}

            GROUP BY
                manga.name

            """

        if tags is not None and not tags == '':
            sql += " HAVING "
            for t in tags:
                sql += "tag_name LIKE ? OR "
                param.append(f'%{t}%')

            sql = f"""
                {sql[:-4]}

                ORDER BY
                    manga.name ASC
            """
                    
        print(sql)
        print(param)
        self.cur.execute(sql, tuple(param))
        r = self.cur.fetchall()
        if not (r is None and len(r) == 0):
            result.extend(r)

        #self.cur.execute("SELECT * FROM manga WHERE ifnull(name,'') || ifnull(artists,'') || ifnull(series,'') || ifnull(original,'') LIKE ?", ('%' + keyword + '%',))
        #result = self.cur.fetchall()
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
        series = result[0][3]
        print(result)
        p_png = [p.name for p in pathlib.Path('static/images/' + title).glob('*.png')]
        p_jpg = [p.name for p in pathlib.Path('static/images/' + title).glob('*.jpg')]
        p_jpeg = [p.name for p in pathlib.Path('static/images/' + title).glob('*.jpeg')]
        p_webp = [p.name for p in pathlib.Path('static/images/' + title).glob('*.webp')]
        p_avif = [p.name for p in pathlib.Path('static/images/' + title).glob('*.avif')]
        p_tmp = []
        p_tmp.extend(p_png)
        p_tmp.extend(p_jpg)
        p_tmp.extend(p_jpeg)
        p_tmp.extend(p_webp)
        p_tmp.extend(p_avif)
        return {'title': title, 'images': p_tmp, 'series': series}