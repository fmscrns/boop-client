import requests, json
from flask import current_app, session


class AuthService:
    @staticmethod
    def get_auth_token(data):
        return requests.post("{}/auth/login".format(
            current_app.config["API_DOMAIN"]),
            json = {
                "username_or_email": data.get("username_or_email_input"),
                "password": data.get("password_input")
            }
        )
    @staticmethod
    def blacklist_auth_token():
        return requests.post("{}/auth/logout".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

class AdminAuthService:
    @staticmethod
    def get_auth_token(data):
        return requests.post("{}/auth/admin/login".format(
            current_app.config["API_DOMAIN"]),
            json = {
                "username_or_email": data.get("username_or_email_input"),
                "password": data.get("password_input")
            }
        )
    @staticmethod
    def blacklist_auth_token():
        return requests.post("{}/auth/logout".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["admin_booped_in"])
            }
        )

