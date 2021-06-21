import requests, json
from flask import current_app, session
from . import save_image

class CommentService:
    @staticmethod
    def create(data_form, data_file):
        return requests.post("{}/comment/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "content": data_form.get("content_input"),
                "parent_id": data_form.get("parent_input"),
                "photo": [
                    dict(
                        filename = save_image(data_file.get("photo_input"), 2)
                    )
                ]
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/comment/creator/{}".format(
            current_app.config["API_DOMAIN"],
            user_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )
    
    @staticmethod
    def get_all_by_post(token, post_pid):
        return requests.get("{}/comment/parent/{}".format(
            current_app.config["API_DOMAIN"],
            post_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def delete(pid):
        return requests.delete("{}/comment/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )