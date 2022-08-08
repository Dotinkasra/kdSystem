from flask import Blueprint, render_template, request, redirect, url_for, after_this_request, send_file
from modules.process_waifu2x import Waifu2x
import os

waifu2x = Blueprint('waifu2x', __name__, url_prefix='/waifu2x')

@waifu2x.route('/', methods = ['GET', 'POST'])
def waifu2x_route():
    upload_folder = './static/waifu2x'
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
