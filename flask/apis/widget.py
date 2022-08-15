from flask import Blueprint, url_for, request
import json
import base64
import pathlib
import random

widget = Blueprint('widget', __name__, url_prefix='/api/widget')

@widget.route('/', methods = ['GET'])
def widget_route():
    current_character = random.choice(list(character.items()))
    current_character = current_character[1]
    send_data = {
        "img" : current_character['default_img'],
        "name" : current_character['name'],
        "sound" : f"{current_character['sound_path']}/{random.choice(login_sound)}"
    }
    print(send_data)
    return json.dumps(send_data)

@widget.route('/click', methods = ['GET', 'POST'])
def widget_click():
    if not request.method == 'POST':
        return 
    print(request.json)
    name = request.json['name']
    current_character = character[name]
    wav = [p.name for p in pathlib.Path(current_character["sound_path"]).glob('*.wav')]
    img = [p.name for p in pathlib.Path(current_character["img_path"]).glob('*.png')]
    return json.dumps(
        {
            "sound": current_character["sound_path"] + "/" + random.choice(wav),
            "img" : current_character["img_path"] + "/" + random.choice(img)
        }
    )

base_sound_path = "static/widget/sound"
base_img_path = "static/widget/img"
login_sound = ["login_1.wav", "login_ex1100.wav", "login.wav"]

character = {
    "rikka_n" : {
        "name" : "rikka_n",
        "default_img" : f"{base_img_path}/rikka_n/baoduoliuhua_wjz-1-1-trim.png",
        "img_path": f"{base_img_path}/rikka_n",
        "sound_path" : f"{base_sound_path}/rikka",
    },
    "rikka_s" : {
        "name" : "rikka_s",
        "default_img" : f"{base_img_path}/rikka_s/baoduoliuhua_2_n-1-1-trim.png",
        "img_path": f"{base_img_path}/rikka_s",
        "sound_path" : f"{base_sound_path}/rikka",
    },    
    "rikka_np" : {
        "name" : "rikka_np",
        "default_img" : f"{base_img_path}/rikka_np/baoduoliuhua_n-1-1-trim.png",
        "img_path": f"{base_img_path}/rikka_np",
        "sound_path" : f"{base_sound_path}/rikka_np",
    }
}