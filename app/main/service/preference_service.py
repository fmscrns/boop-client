import requests
from flask import current_app, session
class PreferenceService:
    @staticmethod
    def create(data_form):
        return requests.post("{}/preference/".format(
            current_app.config["API_DOMAIN"]),
            headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            },
            json = {
                "breed_subgroup": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("cppf-breed_subgroup_input")
                ],
                "business_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("cbpf-business_type_input")
                ],
                "circle_type": [
                    dict(
                        public_id = _type
                    ) for _type in data_form.getlist("ccpf-circle_type_input")
                ]
            }
        )