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
                "photo": [
                    dict(
                        filename = save_image(data_file.get("photo_input"), 2)
                    )
                ],
                "pinboard_id": data_form.get("pinboard_input"),
                "confiner_id": data_form.get("confiner_input"),
                "subject": [
                    dict(
                        public_id = subject
                    ) for subject in data_form.getlist("subject_input")
                ],
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
    def get_all_by_pet(token, pet_pid):
        return requests.get("{}/post/subject/{}".format(
            current_app.config["API_DOMAIN"],
            pet_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )
    
    @staticmethod
    def get_all_by_business(token, business_pid):
        return requests.get("{}/post/pinboard/{}".format(
            current_app.config["API_DOMAIN"],
            business_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )
    
    @staticmethod
    def get_all_by_circle(token, circle_pid):
        return requests.get("{}/post/confiner/{}".format(
            current_app.config["API_DOMAIN"],
            circle_pid),
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
        return requests.get("{}/post/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    @staticmethod
    def get_all_post(token):
        return requests.get("{}/post/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )