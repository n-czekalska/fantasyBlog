import os
from PIL import Image #Python Imaging Library
from flask import url_for, current_app

def add_avatar(upload):

    filename = upload +'.png'

    filepath = os.path.join(current_app.root_path, 'static\\avatars', filename)

    return filename