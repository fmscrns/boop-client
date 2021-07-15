import requests, json
from flask import current_app, session
from . import concat_url_param, save_image

class UserService:
    @staticmethod
    def create(data):
        return requests.post("{}/user/".format(
            current_app.config["API_DOMAIN"]),
            json = {
                "name": data.get("name_input"),
                "username": data.get("username_input"),
                "email": data.get("email_input"),
                "password": data.get("password_input")
            }
        )
    
    @staticmethod
    def edit_photo(pid, token, file):
        return requests.patch("{}/user/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "photo": save_image(file.get("epf-photo_input"), 0)
            }
        )

    @staticmethod
    def edit_profile(pid, token, form):
        return requests.patch("{}/user/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name": form.get("euf-name_input")
            }
        )

    @staticmethod
    def edit_account(pid, token, form):
        return requests.post("{}/user/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "username": form.get("eauf-username_input") if form.get("eauf-username_input") else "",
                "email": form.get("eaef-email_input") if form.get("eaef-email_input") else "",
                "password": form.get("eapf-password_input") if form.get("eapf-password_input") else ""
            }
        )

    @staticmethod
    def get_by_email(email):
        return requests.get("{}/user/email/{}".format(
            current_app.config["API_DOMAIN"], email)
        )

    @staticmethod
    def get_by_token():
        return requests.get("{}/user/bytoken".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    @staticmethod
    def get_by_username(username):
        return requests.get("{}/user/username/{}".format(
            current_app.config["API_DOMAIN"], username),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def search(value, same_fp, same_bpref, pagination_no):
        return requests.get("{}/user/{}".format(
            current_app.config["API_DOMAIN"],
            concat_url_param(
                [
                    ("search", value) if value else None,
                    ("same_followed_pets", same_fp) if same_fp else None,
                    ("same_breed_preferences", same_bpref) if same_bpref else None,
                    ("pagination_no", pagination_no) if pagination_no else None,
                ]
            )
        ),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

class AdminService:
    @staticmethod
    def create(data):
        return requests.post("{}/user/admin".format(
            current_app.config["API_DOMAIN"]),
            json = {
                "name": data.get("name_input"),
                "username": data.get("username_input"),
                "email": data.get("email_input"),
                "password": data.get("password_input")
            }
        )
    @staticmethod
    def get_by_token():
        return requests.get("{}/user/bytoken".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["admin_booped_in"])
            }
        )