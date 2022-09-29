from fileinput import filename
from posixpath import basename
import zipfile
from flask import Blueprint, request, abort, jsonify, make_response, send_file
import json, os, mimetypes, urllib, io
from modules.cmd_process import Erocool
from modules.module import BasicModules
import io
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def test():
    return "api"

@api.route('/erocool', methods = ['POST'])
def erocool_api():
    url = request.form.get('url')
    print(url)
    if BasicModules.is_empty_or_null(url):
        return 

    ec = Erocool()
    zip_path = ec.do(url)
    
    f = io.BytesIO()
    with open(zip_path, 'rb') as zip_file:
        response_data_byte = zip_file.read()
        os.remove(zip_path)
    f.seek(0)
    
    response = make_response(response_data_byte)
    response.status_code = 200
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment', filename = f"{os.path.basename(zip_path)}")
    return response
