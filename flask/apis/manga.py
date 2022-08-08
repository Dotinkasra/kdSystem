from flask import Blueprint, render_template, request, redirect, url_for
from modules.access_manga import AccessManga
import pathlib
from natsort import natsorted

manga = Blueprint('manga', __name__, url_prefix='/manga')

@manga.route('/')
def manag_route():
    am = AccessManga()
    manga = [m for m in am.fetch()]
    return render_template('mangaList.html', manga = manga)

@manga.route('/search', methods = ['GET'])
def manga_search():
    word = request.args.get('word')
    if word is None or len(word) == 0 or not word:
        print("false")
        return redirect(url_for('manga'))
    am = AccessManga()
    manga = [m for m in am.search(word)]
    return render_template('mangaList.html', manga = manga)

@manga.route('/<string:name>', methods = ['POST'])
def manga_contents(name):
    title = request.form.get('title')
    p_png = [p.name for p in pathlib.Path('static/images/' + title).glob('*.png')]
    p_jpg = [p.name for p in pathlib.Path('static/images/' + title).glob('*.jpg')]
    p_jpeg = [p.name for p in pathlib.Path('static/images/' + title).glob('*.jpeg')]
    p_webp = [p.name for p in pathlib.Path('static/images/' + title).glob('*.webp')]
    p_tmp = []
    p_tmp.extend(p_png)
    p_tmp.extend(p_jpg)
    p_tmp.extend(p_jpeg)
    p_tmp.extend(p_webp)
    return render_template('manga.html', title = title, files = ','.join(natsorted(p_tmp)), count = len(p_tmp))
