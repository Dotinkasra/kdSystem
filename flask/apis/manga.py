from tokenize import group
from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify, Response
from modules.access_manga import AccessManga
from modules.module import BasicModules
from natsort import natsorted

manga = Blueprint('manga', __name__, url_prefix='/manga')

@manga.route('/')
def manag_route():
    am = AccessManga()
    manga = [m for m in am.fetch_manga_all()]
    tags = am.get_tag_all()
    return render_template('mangaList.html', manga = manga, tags = tags)


def get_manga_search(
    **args
) -> list:
    am = AccessManga()
    return am.search_manga(**args)

@manga.route('/search', methods = ['GET'])
def manga_search():
    keyword = request.args.get('word')

    result = get_manga_search(keyword = keyword)

    am = AccessManga()
    tags = am.get_tag_all()

    if result is None:
        return redirect(url_for('manga.manag_route'))
    return render_template('mangaList.html', manga = result, tags = tags)

@manga.route('/search', methods = ['POST'])
def manga_extream_search():
    title = request.form.get('title')
    artists = request.form.get('artists')
    original = request.form.get('original')
    form_tags = request.form.get('tag')
    series = request.form.get('series')
    print(title, artists, original, form_tags, series)

    if form_tags is not None:
        form_tags = form_tags.split(",")
        form_tags = list(filter(lambda t: not t == '', form_tags))
        form_tags = None if len(form_tags) == 0 else form_tags

    am = AccessManga()
    tags = am.get_tag_all()
    print("title", title, "aritsts", artists, "original", original, "tag", form_tags, "series", series)

    result = get_manga_search(
        title = None if title == '' else title,
        artists = None if artists == '' else artists,
        original = None if original == '' else original,
        series = None if series == '' else series,
        tags = None if form_tags == '' else form_tags
    )
    if result is None:
        return redirect(url_for('manga.manag_route'))
    return render_template('mangaList.html', manga = result, tags = tags)

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

@manga.route('/tag', methods = ['POST'])
def add_tag():
    tag = request.form.getlist('tag')
    manga_id = request.form.get('manga_id')
    new_tag = request.form.getlist('new_tag')
    am = AccessManga()
    new_tag_ids = []
    for t in new_tag:
        if BasicModules.is_empty_or_null(t):
            continue
        new_tag_ids.append(am.add_new_tag(t)[0][0])

    print("tag共", manga_id, new_tag, tag, tag + new_tag_ids)
    
    am.set_tag_to_manga(manga_id = manga_id, tag_list = tag + new_tag_ids)
    return redirect(url_for('manga.manag_route'))


def post_manga_contents(id: str) -> dict:
    if BasicModules.is_empty_or_null(id):
        return None
    am = AccessManga()
    return am.get_images(id)

@manga.route('/<string:name>', methods = ['GET', 'POST'])
def manga_contents(name):
    id: str = request.form.get('id')
    if BasicModules.is_empty_or_null(id):
        id = name
    result: dict = post_manga_contents(id)
    if result is None:
        return redirect(url_for('manga.manag_route'))
    return render_template('manga.html', title = result['title'], files = ','.join(natsorted(result['images'])), count = len(result['images']), series = result['series'])

@manga.route('/api/contents', methods = ['POST'])
def manga_contents_api():
    id = request.form.get('id')
    result: dict = post_manga_contents(id)
    if result is None:
        return abort(400, 'Parameters: word \n Message: No keywords.')
    result['images'] = natsorted(result['images'])
    result['link'] = "http://192.168.11.74:5005/manga/" + str(id)
    return jsonify({'result': result})

def add_manga_contents(name: str, artists: str = None, series: str = None, original: str = None) -> bool:
    am = AccessManga()
    result = am.insert_single_manga(name, artists, series, original)
    if result is None:
        return False
    return True

@manga.route('/api/add', methods = ['POST'])
def add_manga_contents_api():
    name = request.form.get('name')
    if BasicModules.is_empty_or_null(name):
        abort(400, 'Parameters: name \n Message: No keywords.')
    artists = request.form.get('artists')
    series = request.form.get('series')
    original = request.form.get('original')
    result = add_manga_contents(name, artists, series, original)
    if result:
        return jsonify({'result': 'succese'})
    return abort(500, 'Error')