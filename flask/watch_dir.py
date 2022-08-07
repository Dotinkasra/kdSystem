import sys
import time
import logging
import os
import datetime
import hashlib
from tkinter.messagebox import NO
from modules.access_fc2 import AccessFc2
from modules.access_manga import AccessManga

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

class ImagesWatchHandler(RegexMatchingEventHandler):
    def __init__(self, regexes) -> None:
        super().__init__(regexes= regexes)

    def on_created(self, event):
        if not event.is_directory:
            return 
        filepath = event.src_path
        filename = os.path.basename(filepath)
        db = AccessManga()
        db.insert(filename, None, None, None)
        

    def on_moved(self, event):
        if not event.is_directory:
            return
        filepath = event.src_path
        old_filename = os.path.basename(filepath)
        new_filename = os.path.basename(event.dest_path)

if __name__ == "__main__":
    # 対象ディレクトリ
    DIR_WATCH = './static/images'
    # 対象ファイルパスのパターン
    PATTERNS = [r'.*']

    event_handler = ImagesWatchHandler(PATTERNS)
    
    observer = Observer()
    observer.schedule(event_handler, DIR_WATCH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()