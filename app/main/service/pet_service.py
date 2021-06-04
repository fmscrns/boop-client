import requests, json
from flask import current_app, session
from . import save_image

class PetService:
    @staticmethod
    def create(data_form, data_file):
        return requests.post("{}/pet/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data_form.get("name_input"),
                "bio": data_form.get("bio_input"),
                "birthday": data_form.get("birthday_input"),
                "status": 0,
                "sex": int(data_form.get("sex_input")),
                "is_private": int(data_form.get("private_input")),
                "photo": save_image(data_file.get("photo_input"), 1),
                "group_id": data_form.get("group_input"),
                "subgroup_id": data_form.get("subgroup_input")
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/pet/owner/{}".format(
            current_app.config["API_DOMAIN"],
            user_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def get_by_pid(pid):
        return requests.get("{}/pet/{}".format(
            current_app.config["API_DOMAIN"], pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def edit(pid, token, data_form, data_file):
        return requests.patch("{}/pet/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name": data_form.get("epf-name_input"),
                "bio": data_form.get("epf-bio_input"),
                "birthday": data_form.get("epf-birthday_input"),
                "sex": int(data_form.get("epf-sex_input")),
                "is_private": int(data_form.get("epf-private_input")),
                "status": int(data_form.get("epf-status_input")),
                "photo": save_image(data_file.get("epf-photo_input"), 1),
                "group_id": "",
                "subgroup_id": ""
            }
        )

    @staticmethod
    def delete(pid, data):
        return requests.delete("{}/pet/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name" : data.get("name_input"),
                "bio": "",
                "birthday": "",
                "sex": -1,
                "status": -1,
                "photo": "",
                "group_id": "",
                "subgroup_id": ""
            }
        )

    @staticmethod
    def follow(pid):
        return requests.post("{}/pet/{}/follower/".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def unfollow(pid, data):
        return requests.delete("{}/pet/{}/follower/{}".format(
            current_app.config["API_DOMAIN"],
            pid,
            data.get("follower_input")),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def get_all_pending_pet_followers(token, pid):
        return requests.get("{}/pet/{}/follower/?type=0".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def get_all_confirmed_pet_followers(token, pid):
        return requests.get("{}/pet/{}/follower/?type=1".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def accept(pid, data):
        return requests.post("{}/pet/{}/follower/{}".format(
            current_app.config["API_DOMAIN"],
            pid,
            data.get("follower_input")),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )