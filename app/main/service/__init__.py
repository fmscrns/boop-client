import os, uuid
from flask import current_app
from PIL import Image

def save_image(form_image):
    if form_image:
        filename = str(uuid.uuid4())
        _, f_ext = os.path.splitext(form_image.filename)
        picture_fn = filename + f_ext

        if current_app.config["DEBUG"] == False:
            _cloud.uploader.upload_image(form_image, folder="Boop/", public_id=filename)
        else:
            picture_path = os.path.join(current_app.root_path,'static/images', picture_fn)
            
            output_size=(500, 500)
            i = Image.open(form_image)
            i.thumbnail(output_size)
            i.save(picture_path)

        return picture_fn

    else:
        return "default.jpg"