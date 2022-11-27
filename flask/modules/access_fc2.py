import sqlite3, pathlib
from modules.module import DBaccess, BasicModules

class AccessFc2():
    def __init__(self) -> None:
        self.dbname = 'fc2.db'
        self.dbaccess = DBaccess(self.dbname)

    def fetch(self) -> list:
        result = self.dbaccess.select("SELECT * FROM fc2")
        return [m for m in result]

    def search(self, keyword: str) -> list:
        if BasicModules.is_empty_or_null(keyword):
            return []
        result = self.dbaccess.select("SELECT * FROM fc2 WHERE ifnull(title,'') LIKE ?", ('%' + keyword + '%',))
        return [m for m in result]

    def search_contributor(self, contributor: str) -> list:
        if BasicModules.is_empty_or_null(contributor):
            return []
        result = self.dbaccess.select("SELECT * FROM fc2 WHERE ifnull(contributor,'') LIKE ?", ('%' + contributor + '%',))
        return [m for m in result]

    def get_movie_from_id(self, id: str) -> list:
        if BasicModules.is_empty_or_null(id):
            return []
        result = self.dbaccess.select("SELECT * FROM fc2 WHERE id = ?", (id,))
        return [m for m in result]

    def get_movies(self, id: str) -> dict:
        result = self.get_movie_from_id(id)

        name = result[0][1]
        target_ext_list = ['*.mkv', '*.mp4']
        movies = []
        for ext in target_ext_list:
            movies.extend(
                [f"{name}/{f.name}" for f in pathlib.Path(f'static/movies/{name}/').glob(ext)]
            )
        return {'title': result[0][2], 'movies': movies}

