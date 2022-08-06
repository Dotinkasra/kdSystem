from curses import flash
from turtle import title
import pathlib
import os
from natsort import natsorted
from flask import Flask, render_template, request, url_for, redirect, send_file, after_this_request
from modules.access_manga import AccessManga
from modules.access_fc2 import AccessFc2
from modules.waifu2x import Waifu2x
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manga')
def manga():
    am = AccessManga()
    manga = [m for m in am.fetch()]
    return render_template('mangaList.html', manga = manga)

@app.route('/manga/<string:name>', methods = ['POST'])
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

@app.route('/fc2')
def fc2():
    fc2 = AccessFc2()
    movie = [m for m in fc2.fetch()]
    return render_template('fc2List.html', movie = movie)

@app.route('/fc2/<string:id>', methods = ['POST'])
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

@app.route('/waifu2x', methods = ['GET', 'POST'])
def waifu2x():
    upload_folder = './static/waifu2x'
    allowed_extensions = set(['png', 'jpg'])
    waifu2x = Waifu2x()

    if not request.method == 'POST':
        return render_template('waifu2x.html')

    if 'file' not in request.files:
        return 'ファイルがありません'
    
    file = request.files['file']
    if file.filename == '':
        return 'ファイルがありません'

    if file:
        file.save(os.path.join(upload_folder, file.filename))
        result = waifu2x.do(file.filename)
        return redirect(url_for('waifu2x_result', filename = result))


@app.route('/waifu2x/<string:filename>', methods = ['GET', 'POST'])
def waifu2x_result(filename):
    file_path = "static/waifu2x/" + filename
    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            app.logger.error("Error")
        return response
    return send_file(file_path)

if __name__ == '__main__':
    app.debug=True
    app.run(host = '0.0.0.0', port = '5005', debug = True)