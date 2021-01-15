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
    def get_by_specie(token, specie_id):
        return requests.get("{}/breed/parent/{}".format(
            current_app.config["API_DOMAIN"],
            specie_id),
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
                "name" : data.get("cbf-name_input"),
                "parent_id": data.get("cbf-parent_input")
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
                "name" : data.get("ebf-name_input"),
                "parent_id": data.get("ebf-parent_input")
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
                "name" : data.get("dbf-name_input"),
                "parent_id": data.get("dbf-parent_input")
            }
        )