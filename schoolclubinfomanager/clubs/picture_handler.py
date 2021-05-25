import os
from PIL import Image
from flask import url_for, current_app

def add_photo(pic_upload, club_name):
    filename = pic_upload.filename
    #grab extension type, such as png or jpg:
    ext_type = filename.split('.')[-1]
    #set image filename as <schoolname-logo.jpg> (or png, or svg):
    storage_filename = str(club_name)+ext_type
    filepath = os.path.join(current_app.root_path, "static/img/club", storage_filename)

    #open image supplied by user and save it
    pic = Image.open(pic_upload)
    pic.save(filepath)

    return storage_filename
