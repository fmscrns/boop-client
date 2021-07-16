import os, uuid, base64
from flask import current_app
from PIL import Image
from app.main import myCloudinary
from io import BytesIO

def concat_url_param(param_list):
    url = "?"
    new_list = [x for x in param_list if x is not None]
    for count, param in enumerate(new_list):
        url += param[0] + "=" + param[1]
        if count+1 < len(new_list):
            url += "&"
    return url

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

def save_base64image(form_text):
    _split = form_text.split(",")
    encoded_image = _split[1]
    f_ext = ".{}".format(_split[0].split("/")[1].split(";")[0])
    filename = str(uuid.uuid4())
    picture_fn = filename + f_ext
    image = base64.b64decode(encoded_image)
    if current_app.config["DEBUG"] == False:
        myCloudinary.uploader.upload_image(image, folder="Boop/", public_id=picture_fn)
    else:
        image_bytes = BytesIO(image)
        _i = Image.open(image_bytes)
        picture_path = os.path.join(current_app.root_path, "static/images", picture_fn)
        _i.save(picture_path)
    return picture_fn