import requests, json
from flask import current_app, session
from . import save_image

class CircleService:
    @staticmethod
    def create(data_form, data_file):
        return requests.post("{}/circle/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data_form.get("name_input"),
                "bio": data_form.get("bio_input"),
                "_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("type_input")
                ],
                "photo": save_image(data_file.get("photo_input"), 2)
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/circle/admin/{}".format(
            current_app.config["API_DOMAIN"],
            user_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def get_by_pid(pid):
        return requests.get("{}/circle/{}".format(
            current_app.config["API_DOMAIN"], pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def edit(pid, token, data_form, data_file):
        return requests.patch("{}/circle/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name": data_form.get("ebf-name_input"),
                "bio": data_form.get("ebf-bio_input"),
                "_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("ebf-type_input")
                ],
                "photo": save_image(data_file.get("ebf-photo_input"), 2)
            }
        )

    @staticmethod
    def delete(pid, data):
        return requests.delete("{}/circle/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data.get("name_input"),
                "_type": []
            }
        )