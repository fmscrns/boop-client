import requests, json
from flask import current_app, session
from . import save_image

class BusinessService:
    @staticmethod
    def create(data_form, data_file):
        _type = data_form.getlist("type_input")
        if len(_type) == 1:
            _type = int(_type[0])
        elif len(_type) == 2:
            if "0" in _type and "1" in _type:
                _type = 3
            elif "0" in _type and "2" in _type:
                _type = 4
            elif "1" in _type and "2" in _type:
                _type = 5
        else:
            _type = 6

        return requests.post("{}/business/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data_form.get("name_input"),
                "bio": data_form.get("bio_input"),
                "_type": _type,
                "photo": save_image(data_file.get("photo_input"), 2)
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/business/exec/{}".format(
            current_app.config["API_DOMAIN"],
            user_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def get_by_pid(pid):
        return requests.get("{}/business/{}".format(
            current_app.config["API_DOMAIN"], pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def edit(pid, token, data_form, data_file):
        _type = data_form.getlist("ebf-type_input")
        print("ASD: {}".format(_type))
        if len(_type) == 1:
            _type = int(_type[0])
        elif len(_type) == 2:
            if "0" in _type and "1" in _type:
                _type = 3
            elif "0" in _type and "2" in _type:
                _type = 4
            elif "1" in _type and "2" in _type:
                _type = 5
        else:
            _type = 6
        print("final: {}".format(_type))
        return requests.patch("{}/business/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name": data_form.get("ebf-name_input"),
                "bio": data_form.get("ebf-bio_input"),
                "_type": _type,
                "photo": save_image(data_file.get("ebf-photo_input"), 2)
            }
        )

    @staticmethod
    def delete(pid, data):
        return requests.delete("{}/business/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data.get("name_input"),
                "_type": 0
            }
        )