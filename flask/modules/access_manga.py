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

    def __close(self):
        self.conn.close()

    def __connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def __select(self, sql: str, parameta: tuple = None) -> list:
        self.__connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__close()
        return result

    def __insert(self, sql: str, parameta: tuple = None, table_name: str = None) -> None|list:
        self.__connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        self.conn.commit()

        result = None
        if table_name:
            self.cur.execute(f"SELECT * FROM {table_name} WHERE rowid = last_insert_rowid();")
            result = self.cur.fetchall()
        self.__close()
        return result

    def __delete(self, sql: str, parameta: tuple = None):
        self.__connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        self.conn.commit()
        self.__close()

    def insert_single_manga(self, name: str, artists: str, series: str, original: str):
        self.__connect()
        if BasicModules.is_empty_or_null(name):
            return

        artists = None if BasicModules.is_empty_or_null(artists) else artists
        series = None if BasicModules.is_empty_or_null(series) else series
        original = None if BasicModules.is_empty_or_null(original) else original
        print(f'{name}')

        self.__insert(
            "INSERT INTO manga(name, artists, series, original) VALUES(?,?,?,?)",
            (name, artists, series, original)
        )

    def fetch_manga_all(self) -> list:
        return self.__select(f"{self.main_sql} GROUP BY manga.name")

    def get_tagid(self, tag_name: str) -> int:
        result = self.__select("SELECT id FROM tag WHERE name = ?", (tag_name,))
        return int(result[0])

    def get_tag_granted_in_manga(self, manga_id: str = None) -> list:
        return self.__select(
            "SELECT tag.* FROM tag_manga LEFT JOIN tag ON tag_manga.tag_id = tag.id WHERE tag_manga.manga_id = ?",
             (manga_id, )
        )

    def get_tag_all(self) -> list:
        return self.__select("SELECT * FROM tag")    
    
    def set_tag_to_manga(self, manga_id: str, tag_list: list[str]):
        # 漫画に付与されたタグ一覧のリスト
        current_tag = set([int(i[0]) for i in self.get_tag_granted_in_manga(manga_id = manga_id)])
        # 受け取ったタグ一覧のリスト
        tag_list_set = set([int(i) for i in tag_list])

        # 差集合
        # 受け取ったタグ - 現在のタグ = まだ付けられていない新しいタグ
        new_tag = tag_list_set - current_tag
        # 現在のタグ - 受け取ったタグ = チェックが外された削除するタグ
        delete_tag = current_tag - tag_list_set

        print("current_tag", list(current_tag), "tag_list", list(tag_list_set))
        print("new_tag", list(new_tag), "delete_tag", list(delete_tag))

        for tag in list(new_tag):
            self.__insert(
                "INSERT INTO tag_manga VALUES(?,?)",
                (tag, manga_id)                
            )
        for tag in list(delete_tag):
            self.__delete(
                "DELETE FROM tag_manga WHERE tag_id = ? AND manga_id = ?",
                (tag, manga_id)
            )
    
    def add_new_tag(self, tag_name: str):
        if BasicModules.is_empty_or_null(tag_name):
            return

        exist_tags = [i[1] for i in self.get_tag_all()]
        if tag_name in exist_tags:
            return

        return self.__insert(
            sql = "INSERT INTO tag(name) VALUES(?)",
            parameta = (tag_name, ),
            table_name = 'tag'
        )
        
    def search_manga(
        self,
        keyword: str = None,
        title: str = None,
        artists: str = None,
        series: str = None,
        original: str = None,
        tags: list[str] = None
    ) -> list:
        # キーワードがなく、他の詳細検索のパラメタもない場合
        if keyword is None and not any((title, artists, series, original, tags)):
            return []

        result = []

        sql = self.main_sql

        # キーワードが存在する場合は、全体をあいまい検索
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
            r = self.__select(sql, param)
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
        r = self.__select(sql, tuple(param))
        if not (r is None and len(r) == 0):
            result.extend(r)

        return [m for m in result]

    def get_images(self, id: str) -> dict:
        if not id: return []

        result = self.__select("SELECT * FROM manga WHERE id = ?", (id,))

        title = result[0][1]
        series = result[0][3]
        print(result)
        target_ext_list = ['*.png', '*.jpg', '*.jpeg', '*.webp', '*.avif']
        images = []
        for ext in target_ext_list:
            images.extend(
                [f.name for f in pathlib.Path(f'static/images/{title}').glob(ext)]
            )
        return {'title': title, 'images': images, 'series': series}