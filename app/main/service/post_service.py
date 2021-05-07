import requests, json
from flask import current_app, session
from . import save_image

class PostService:
    @staticmethod
    def create(data_form, data_file):
        return requests.post("{}/post/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "content": data_form.get("content_input"),
                "photo": save_image(data_file.get("photo_input"), 2)
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/post/creator/{}".format(
            current_app.config["API_DOMAIN"],
            user_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def get_by_pid(pid):
        return requests.get("{}/post/{}".format(
            current_app.config["API_DOMAIN"], pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def delete(pid):
        return requests.delete("{}/post/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def get_all_posts():
        return requests.get("{}/feed{}".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    @staticmethod
    def get_all_post(token):
        return requests.get("{}/feed{}".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )