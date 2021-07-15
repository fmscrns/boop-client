import requests, json
from flask import current_app, session
from . import save_image

class BusinessService:
    @staticmethod
    def create(data_form, data_file):
        return requests.post("{}/business/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data_form.get("name_input"),
                "bio": data_form.get("bio_input"),
                "_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("type_input")
                ],
                "mon_open_bool": True if data_form.get("mon_open_bool") else False,
                "mon_open_time": data_form.get("mon_open_time"),
                "mon_close_time": data_form.get("mon_close_time"),
                "tue_open_bool": True if data_form.get("tue_open_bool") else False,
                "tue_open_time": data_form.get("tue_open_time"),
                "tue_close_time": data_form.get("tue_close_time"),
                "wed_open_bool": True if data_form.get("wed_open_bool") else False,
                "wed_open_time": data_form.get("wed_open_time"),
                "wed_close_time": data_form.get("wed_close_time"),
                "thu_open_bool": True if data_form.get("thu_open_bool") else False,
                "thu_open_time": data_form.get("thu_open_time"),
                "thu_close_time": data_form.get("thu_close_time"),
                "fri_open_bool": True if data_form.get("fri_open_bool") else False,
                "fri_open_time": data_form.get("fri_open_time"),
                "fri_close_time": data_form.get("fri_close_time"),
                "sat_open_bool": True if data_form.get("sat_open_bool") else False,
                "sat_open_time": data_form.get("sat_open_time"),
                "sat_close_time": data_form.get("sat_close_time"),
                "sun_open_bool": True if data_form.get("sun_open_bool") else False,
                "sun_open_time": data_form.get("sun_open_time"),
                "sun_close_time": data_form.get("sun_close_time"),
                "photo": save_image(data_file.get("photo_input"), 3)
            }
        )
    
    @staticmethod
    def get_all_by_user(token, user_pid):
        return requests.get("{}/business/exec/{}".format(
            current_app.config["API_DOMAIN"],
            user_pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def get_by_pid(pid):
        return requests.get("{}/business/{}".format(
            current_app.config["API_DOMAIN"], pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def get_by_preference(pagination_no):
        return requests.get("{}/business/preference{}".format(
            current_app.config["API_DOMAIN"],
            "?pagination_no={}".format(pagination_no) if pagination_no else ""),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    @staticmethod
    def edit(pid, token, data_form, data_file):
        return requests.patch("{}/business/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "name": data_form.get("ebf-name_input"),
                "bio": data_form.get("ebf-bio_input"),
                "_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("ebf-type_input")
                ],
                "photo": save_image(data_file.get("ebf-photo_input"), 3)
            }
        )

    @staticmethod
    def delete(pid, data):
        return requests.delete("{}/business/{}".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "name": data.get("name_input"),
                "_type": []
            }
        )

    @staticmethod
    def get_all_businesses():
        return requests.get("{}/business/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def follow(pid):
        return requests.post("{}/business/{}/follower/".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def unfollow(pid, data):
        return requests.delete("{}/business/{}/follower/{}".format(
            current_app.config["API_DOMAIN"],
            pid,
            data.get("follower_input")),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )
    
    @staticmethod
    def get_all_followers(token, pid):
        return requests.get("{}/business/{}/follower/".format(
            current_app.config["API_DOMAIN"],
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }
        )

    @staticmethod
    def create_executive(pid, token, data):
        return requests.post("{}/business/{}/executive/".format(
            current_app.config["API_DOMAIN"], 
            pid),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            },
            json = {
                "public_id": data.get("cbef-executive_input")
            }
        )
    
    @staticmethod
    def delete_executive(pid, token, data):
        return requests.delete("{}/business/{}/executive/{}".format(
            current_app.config["API_DOMAIN"], 
            pid,
            data.get("dbef-executive_input")),
            headers = {
                "Authorization" : "Bearer {}".format(token)
            }, json = {
                "name": data.get("dbef-name_input")
            }
        )