import os, uuid
from flask import current_app
from PIL import Image
from app.main import myCloudinary

def save_image(form_image, _type):
    if form_image:
        filename = str(uuid.uuid4())
        _, f_ext = os.path.splitext(form_image.filename)
        picture_fn = filename + f_ext

        if current_app.config["DEBUG"] == False:
            myCloudinary.uploader.upload_image(form_image, folder="Boop/", public_id=filename)
        else:
            picture_path = os.path.join(current_app.root_path,'static/images', picture_fn)
            
            output_size=(500, 500)
            i = Image.open(form_image)
            i.thumbnail(output_size)
            i.save(picture_path)

        return picture_fn

    else:
        if _type == 0:
            return "default_user.jpg"
        elif _type == 1:
            return "default_pet.jpg"
        elif _type == 2:
            return None
        elif _type == 3:
            return "default_business.jpg"
        elif _type == 4:
            return "default_circle.jpg"