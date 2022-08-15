from fileinput import filename
import time
import os
from tkinter.messagebox import NO
from modules.access_fc2 import AccessFc2
from modules.access_manga import AccessManga
import threading
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

import PySimpleGUI as sg
import tkinter
class ImagesWatchHandler(RegexMatchingEventHandler):
    def __init__(self, regexes, filename) -> None:
        super().__init__(regexes= regexes)

    def on_created(self, event):
        if not event.is_directory:
            return 
        filepath = event.src_path
        filename.set(os.path.basename(filepath))

    def on_moved(self, event):
        if not event.is_directory:
            return
        filepath = event.src_path
        old_filename = os.path.basename(filepath)
        new_filename = os.path.basename(event.dest_path)

class DatabaseManager():
    def __init__(self) -> None:
        self.db = AccessManga()

    def insert(
        self, filename: str, artists: str = None, series: str = None, original: str = None
    ):
        self.db.insert(filename, artists, series, original)
    
    def __del__(self):
        del self.db
        
class CheckLogg(tkinter.Checkbutton):
    """
    フォルダ監視ON/OFF切替チェックボタン
    """
    def __init__(self, root, filename):
        self.var = tkinter.BooleanVar(root, value=False)

        super().__init__(
            root,
            text="監視 ON/OFF",
            variable=self.var,
            command=self.switch_logging,    #クリック時に実行する関数
            )
        self.pack() #チェックボタン表示

        self.event_handler = ImagesWatchHandler([r'.*'], filename)   #イベントハンドラオブジェクト生成
        self.path = './static/images'


    def switch_logging(self):           #クリック時に実行
        if self.var.get():  #ONの場合
            self.observer = Observer()  #Observerオブジェクト生成
            self.observer.schedule(     #スレッド作成
                self.event_handler,
                self.path,
                recursive=True
                )
            self.observer.start()       #スレッド開始
        else:               #OFFの場合
            self.observer.stop()        #スレッド停止
            self.observer.join()        #スレッド完了まで待機


class ShowFilename(tkinter.Label):
    """
    フォルダ・ファイル名表示用ラベル
    """
    def __init__(self, root, filename):
        super().__init__(
            root,
            width=15,
            relief="ridge",
            textvariable=filename,
            )
        self.pack() #ラベル表示

class SendButton(tkinter.Button):
    def __init__(self, root):
        super().__init__(
            root,
            text="送信",
            command=self.invoke
        )
        self.pack()

    def invoke(self):
        title = s['text']
        print(title)
        if title is None or len(title) == 0 or title == '' or title == ' ':
            return
        self['state'] = tkinter.DISABLED
        db = DatabaseManager()
        db.insert(
            filename=title,
            artists=i_artists.get(),
            series=i_series.get(),
            original=i_original.get()
        )

        BasicModules.reset_textbox(i_artists, i_series, i_original)
        s.configure(textvariable = "Text")
class BasicModules():
    @classmethod
    def reset_textbox(self, *args):
        for i in args:
            i.delete(0, tkinter.END)

if __name__ == "__main__":
    print('実行します')
    root = tkinter.Tk()

    filename = tkinter.StringVar(root)  #フォルダ・ファイル名格納用変数
    c = CheckLogg(root, filename)                 #チェックボタン生成
    s = ShowFilename(root, filename)              #ラベル生成

    l_artists = tkinter.Label(text="作者")
    i_artists = tkinter.Entry()

    l_artists.pack()
    i_artists.pack()

    l_series = tkinter.Label(text="シリーズ")
    i_series = tkinter.Entry()

    l_series.pack()
    i_series.pack()

    l_original = tkinter.Label(text="元ネタ")
    i_original = tkinter.Entry()

    l_original.pack()
    i_original.pack()

    send = SendButton(root)
    
    
    root.mainloop()

