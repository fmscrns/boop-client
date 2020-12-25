import requests, json
from flask import current_app, session


class SpecieService:
    @staticmethod
    def get_all(token):
        return requests.get("{}/specie/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def create(token, data):
        return requests.post("{}/specie/".format(
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
        return requests.patch("{}/specie/{}".format(
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
        return requests.delete("{}/specie/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input")
            }
        )