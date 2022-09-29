from flask import Blueprint, render_template, request, redirect, url_for, after_this_request, send_file, abort, jsonify, make_response
from modules.module import BasicModules
from modules.cmd_process import Waifu2x
import os, mimetypes, gc

waifu2x = Blueprint('waifu2x', __name__, url_prefix='/waifu2x')

@waifu2x.route('/', methods = ['GET', 'POST'])
def waifu2x_route():
    if not request.method == 'POST':
        return render_template('waifu2x.html')

    if 'file' not in request.files:
        return 'ファイルがありません'
    
    file = request.files['file']
    if file.filename == '' or not file:
        return 'ファイルがありません'

    upload_folder = './static/waifu2x'
    file.save(os.path.join(upload_folder, file.filename))

    waifu2x = Waifu2x()
    result = waifu2x.do(file.filename)
    BasicModules.collect_after_deleting(waifu2x)

    return redirect(url_for('waifu2x_result', filename = result))

@waifu2x.route('/<string:filename>', methods = ['GET', 'POST'])
def waifu2x_result(filename):
    file_path = "static/waifu2x/" + filename
    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            waifu2x.logger.error("Error")
        return response
    return send_file(file_path)


@waifu2x.route('/api/post', methods = ['POST'])
def waifu2x_api():
    if not (request.method == 'POST' and 'file' in request.files):
        return abort(400, 'Parameters: word \n Message: No keywords.')

    file = request.files['file']
    if file.filename == '' or not file:
        return abort(400, 'Parameters: word \n Message: No keywords.')

    upload_folder = './static/waifu2x/'
    file.save(os.path.join(upload_folder, file.filename))

    waifu2x = Waifu2x()
    result = waifu2x.do(file.filename)
    BasicModules.collect_after_deleting(waifu2x)

    upscale_file_path = upload_folder + result
    response = make_response()
    response.data = open(upscale_file_path, "rb").read()
    response.headers['Content-Disposition'] = 'attachment; filename=' + result
    response.mimetype = mimetypes.guess_type(result)[0]

    os.remove(upscale_file_path)
    
    return response