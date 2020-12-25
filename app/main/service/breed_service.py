import requests, json
from flask import current_app, session


class BreedService:
    @staticmethod
    def get_all(token):
        return requests.get("{}/breed/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def create(token, data):
        return requests.post("{}/breed/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input"),
                "parent_id": data.get("parent_input")
            }
        )

    @staticmethod
    def edit(pid, token, data):
        return requests.patch("{}/breed/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input"),
                "parent_id": data.get("parent_input")
            }
        )
    
    @staticmethod
    def delete(pid, token, data):
        return requests.delete("{}/breed/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input"),
                "parent_id": data.get("parent_input")
            }
        )