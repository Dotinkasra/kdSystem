from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from modules.access_manga import AccessManga
from modules.module import BasicModules
from natsort import natsorted

manga = Blueprint('manga', __name__, url_prefix='/manga')

@manga.route('/')
def manag_route():
    am = AccessManga()
    manga = [m for m in am.fetch()]
    return render_template('mangaList.html', manga = manga)


def get_manga_search(word: str) -> list:
    print(word)
    if BasicModules.is_empty_or_null(word):
        return None
    am = AccessManga()
    return am.search(word)

@manga.route('/search', methods = ['GET'])
def manga_search():
    result = get_manga_search(request.args.get('word'))
    if result is None:
        return redirect(url_for('manga.manag_route'))
    return render_template('mangaList.html', manga = result)

@manga.route('/api/search', methods = ['POST'])
def manga_search_api():
    result = get_manga_search(request.form.get('word'))
    if result is None:
        return abort(400, 'Parameters: word \n Message: No keywords.')
    res_data: list = []
    for r in result:
        res_data.append(
            {
                'id': r[0],
                'name': r[1],
                'artists': r[2],
                'series': r[3],
                'original': r[4]
            }
        )
    return jsonify({'result': res_data})


def post_manga_contents(id: str) -> dict:
    if BasicModules.is_empty_or_null(id):
        return None
    am = AccessManga()
    return am.get_images(id)

@manga.route('/<string:name>', methods = ['POST'])
def manga_contents(name):
    id: str = request.form.get('id')
    result: dict = post_manga_contents(id)
    print(result)
    if result is None:
        return redirect(url_for('manga.manag_route'))
    return render_template('manga.html', title = result['title'], files = ','.join(natsorted(result['images'])), count = len(result['images']))

@manga.route('/api/contents', methods = ['POST'])
def manga_contents_api():
    id = request.form.get('id')
    result: dict = post_manga_contents(id)
    if result is None:
        return abort(400, 'Parameters: word \n Message: No keywords.')
    result['images']= natsorted(result['images'])
    return jsonify({'result': result})