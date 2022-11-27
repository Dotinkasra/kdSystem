import gc

class BasicModules():

    @classmethod
    def is_empty_or_null(self, s: str) -> bool:
        return s is None or len(s) == 0 or not s

    @classmethod
    def collect_after_deleting(self, v: any):
        del v
        gc.collect()