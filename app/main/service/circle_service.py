from os import stat
import requests, json
from flask import current_app, session
from . import concat_url_param, save_image

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
                "photo": save_image(data_file.get("photo_input"), 4)
            }
        )

    @staticmethod
    def create_admin(pid, token, data):
        return requests.post("{}/circle/{}/admin/".format(
            current_app.config["API_DOMAIN"], 
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "public_id": data.get("ccaf-admin_input")
            }
        )
    
    @staticmethod
    def delete_admin(pid, token, data):
        return requests.delete("{}/circle/{}/admin/{}".format(
            current_app.config["API_DOMAIN"], 
            pid,
            data.get("dcaf-admin_input")),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }, json = {
                "name": data.get("dcaf-name_input")
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/circle/creator/{}".format(
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
    def get_by_preference(pagination_no):
        return requests.get("{}/circle/preference{}".format(
            current_app.config["API_DOMAIN"],
            "?pagination_no={}".format(pagination_no) if pagination_no else ""),
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
                "name": data_form.get("ecf-name_input"),
                "bio": data_form.get("ecf-bio_input"),
                "_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("ecf-type_input")
                ],
                "photo": save_image(data_file.get("ecf-photo_input"), 4)
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
    
    @staticmethod
    def join(pid):
        return requests.post("{}/circle/{}/member/".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def leave(pid, data):
        return requests.delete("{}/circle/{}/member/{}".format(
            current_app.config["API_DOMAIN"],
            pid,
            data.get("member_input")),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def get_all_members(token, pid, _type=None, search_value=None):
        return requests.get("{}/circle/{}/member/{}".format(
            current_app.config["API_DOMAIN"],
            pid,
            concat_url_param(
                [
                    ("type", _type) if _type else None,
                    ("search", search_value) if search_value else None
                ]
            )
        ),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def accept(pid, data):
        return requests.post("{}/circle/{}/member/{}".format(
            current_app.config["API_DOMAIN"],
            pid,
            data.get("member_input")),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )