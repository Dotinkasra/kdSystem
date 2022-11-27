import gc
import sqlite3

class BasicModules():

    @classmethod
    def is_empty_or_null(self, s: str) -> bool:
        return s is None or len(s) == 0 or not s

    @classmethod
    def collect_after_deleting(self, v: any):
        del v
        gc.collect()

class DBaccess():
    def __init__(self, dbname) -> None:
        self.dbname = dbname

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def select(self, sql: str, parameta: tuple = None) -> list:
        self.connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        result = self.cur.fetchall()
        self.close()
        return result

    def insert(self, sql: str, parameta: tuple = None, table_name: str = None) -> None|list:
        self.connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        self.conn.commit()

        result = None
        if table_name:
            self.cur.execute(f"SELECT * FROM {table_name} WHERE rowid = last_insert_rowid();")
            result = self.cur.fetchall()
        self.close()
        return result

    def delete(self, sql: str, parameta: tuple = None):
        self.connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        self.conn.commit()
        self.close()