import os
from PIL import Image #Python Imaging Library
from flask import url_for, current_app

def add_avatar(upload, username):

    filename = upload.filename
    extension = filename.split('.')[-1]
    #avoid files of the same name by using username
    newname = str(username)+'.'+extension

    filepath = os.path.join(current_app.root_path, 'static\\avatars', newname)

    output_size = (200,200)
    picture = Image.open(upload)
    picture.save(filepath)

    return newname