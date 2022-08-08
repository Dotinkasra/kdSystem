from flask import Blueprint, render_template, request, redirect, url_for
from modules.access_fc2 import AccessFc2
import pathlib

fc2 = Blueprint('fc2', __name__, url_prefix='/fc2')

@fc2.route('/')
def fc2_route():
    fc2 = AccessFc2()
    movie = [m for m in fc2.fetch()]
    return render_template('fc2List.html', movie = movie)

@fc2.route('/search', methods = ['GET'])
def fc2_search():
    word = request.args.get('word')
    if word is None or len(word) == 0 or not word:
        print("false")
        return redirect(url_for('fc2'))
    fc2 = AccessFc2()
    movie = [f for f in fc2.search(word)]
    return render_template('fc2List.html', movie = movie)

@fc2.route('/<string:id>', methods = ['POST'])
def fc2_contents(id):
    title = request.form.get('title')
    m_mkv = [title + "/" + m.name for m in pathlib.Path('static/movies/' + title).glob('*.mkv')]
    m_mp4 = [title + "/" + m.name for m in pathlib.Path('static/movies/' + title).glob('*.mp4')]
    m_tmp = []
    m_tmp.extend(m_mkv)
    m_tmp.extend(m_mp4)
    html = ""
    for movie in m_tmp:
        html += '''<video src="static/movies/{title}/{movie}"></video>'''.format(title=title, movie=movie)
    return render_template('fc2.html', video = m_tmp)
