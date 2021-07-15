import requests
from flask import current_app, session
from . import concat_url_param, save_base64image

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
                        filename = save_base64image(photo)
                    ) for photo in [
                        data_form.get("photo_1_input"),
                        data_form.get("photo_2_input"),
                        data_form.get("photo_3_input"),
                        data_form.get("photo_4_input")
                    ] if photo
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
    def get_all_by_user(token, pagination_no):
        return requests.get("{}/post/bytoken{}".format(
            current_app.config["API_DOMAIN"],
            "?pagination_no={}".format(pagination_no) if pagination_no else ""),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )
    
    @staticmethod
    def get_all_by_pet(token, pet_pid, w_media_only, pagination_no):
        return requests.get("{}/post/subject/{}{}".format(
            current_app.config["API_DOMAIN"],
            pet_pid,
            concat_url_param(
                [
                    ("w_media_only", w_media_only) if w_media_only else None,
                    ("pagination_no", pagination_no) if pagination_no else None
                ]
            )
        ),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )
        
    @staticmethod
    def get_all_by_business(token, business_pid, w_media_only, pagination_no):
        return requests.get("{}/post/pinboard/{}{}".format(
            current_app.config["API_DOMAIN"],
            business_pid,
            concat_url_param(
                [
                    ("w_media_only", w_media_only) if w_media_only else None,
                    ("pagination_no", pagination_no) if pagination_no else None
                ]
            )
        ),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )
    
    @staticmethod
    def get_all_by_circle(token, circle_pid, w_media_only, pagination_no):
        return requests.get("{}/post/confiner/{}{}".format(
            current_app.config["API_DOMAIN"],
            circle_pid,
            concat_url_param(
                [
                    ("w_media_only", w_media_only) if w_media_only else None,
                    ("pagination_no", pagination_no) if pagination_no else None
                ]
            )    
        ),
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
    def like(pid):
        return requests.post("{}/post/{}".format(
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
    def get_all_posts(pagination_no):
        return requests.get("{}/post/{}".format(
            current_app.config["API_DOMAIN"],
            "?pagination_no={}".format(pagination_no) if pagination_no else ""),
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