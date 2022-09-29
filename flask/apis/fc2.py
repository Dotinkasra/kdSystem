from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from modules.access_fc2 import AccessFc2
import pathlib
from modules.module import BasicModules

fc2 = Blueprint('fc2', __name__, url_prefix='/fc2')

@fc2.route('/')
def fc2_route():
    fc2 = AccessFc2()
    return render_template('fc2List.html', movie = fc2.fetch())


def get_fc2_search(word: str):
    if BasicModules.is_empty_or_null(word):
        print("false")
        return None
    fc2 = AccessFc2()
    return fc2.search(word)

@fc2.route('/search', methods = ['GET'])
def fc2_search():
    result: list = get_fc2_search(request.args.get('word'))
    if result is None:
        return redirect(url_for('fc2.fc2_route'))
    return render_template('fc2List.html', movie = result)

@fc2.route('/api/search', methods = ['POST'])
def fc2_search_api():
    result: list = get_fc2_search(request.form.get('word'))
    if result is None:
        return abort(400, 'Parameters: word \n Message: No keywords.')
    
    res_data: list = []
    for r in result:
        res_data.append(
            {
                'id': r[0],
                'name': r[1],
                'title': r[2],
                'rate': r[3]
            }
        )
    return jsonify({'result': res_data})


def post_fc2_contents(id: str):
    if BasicModules.is_empty_or_null(id):
        print("false")
        return None
    fc2 = AccessFc2()
    return fc2.get_movies(id)

@fc2.route('/<string:id>', methods = ['GET', 'POST'])
def fc2_contents(id):
    form_id: str = request.form.get('id')
    if BasicModules.is_empty_or_null(form_id):
        form_id = id
    result: dict = post_fc2_contents(str(form_id))
    if result is None:
        return redirect(url_for('fc2.fc2_route'))
    return render_template('fc2.html', video = result['movies'])

@fc2.route('/api/contents', methods = ['POST'])
def fc2_contents_api():
    id: str = request.form.get('id')
    result: list = post_fc2_contents(str(id))
    print(id)
    if result is None:
        return abort(400, 'Parameters: id \n Message: No keywords.')
    result['movies'] = ['http://192.168.11.74:5005/static/movies/' + m for m in result['movies']]
    return jsonify({'result': result})

