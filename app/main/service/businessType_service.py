import requests, json
from flask import current_app, session

class BusinessTypeService:
    @staticmethod
    def get_all(token):
        return requests.get("{}/business_type/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def create(token, data):
        return requests.post("{}/business_type/".format(
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
        return requests.patch("{}/business_type/{}".format(
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
        return requests.delete("{}/business_type/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name" : data.get("name_input")
            }
        )