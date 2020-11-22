import requests, json
from flask import current_app


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