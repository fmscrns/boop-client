from app.main.service import concat_url_param
import requests
from flask import current_app, session

class NotificationService:
    @staticmethod
    def get_all_by_token(pid, read=None, count=None):
        return requests.get("{}/notification/{}".format(
            current_app.config["API_DOMAIN"], 
            concat_url_param(
                [
                    ("read", read) if read else None,
                    ("count", count) if count else None
                ]
            )
        ), headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    