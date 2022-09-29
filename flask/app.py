from flask import Flask, render_template
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

from apis.api import api
app.register_blueprint(api)

from apis.manga import manga
app.register_blueprint(manga)

from apis.fc2 import fc2
app.register_blueprint(fc2)

from apis.waifu2x import waifu2x
app.register_blueprint(waifu2x)

from apis.widget import widget
app.register_blueprint(widget)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/widget')
def widget():
    return render_template('widget.html')

if __name__ == '__main__':
    app.debug=True
    app.run(host = '0.0.0.0', port = '5005', debug = True)
    #app.run()
