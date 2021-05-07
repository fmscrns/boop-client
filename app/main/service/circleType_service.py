import requests, json
from flask import current_app, session

class CircleTypeService:
    @staticmethod
    def get_all(token):
        return requests.get("{}/circle_type/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def create(token, data):
        return requests.post("{}/circle_type/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input")
            }
        )

    @staticmethod
    def edit(pid, token, data):
        return requests.patch("{}/circle_type/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input")
            }
        )
    
    @staticmethod
    def delete(pid, token, data):
        return requests.delete("{}/circle_type/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input")
            }
        )