import requests
from flask import current_app, session

class NotificationService:
    @staticmethod
    def get_all_by_token(pid, read=None, count=None):
        return requests.get("{}/notification/{}".format(
            current_app.config["API_DOMAIN"], 
            "?{}{}".format(
                "read={}".format(read) if read else "",
                "{}count={}".format("&" if read else "", count) if count else ""
            )
        ), headers = {
                "Authorization" : "Bearer {}".format(session["booped_in"])
            }
        )

    