from app.main.util.decorator import session_required
import os, json
from dateutil import parser
from flask import request, jsonify
from ... import notification_bp
from ..service.notification_service import NotificationService
from itsdangerous import URLSafeTimedSerializer
from .. import sio

@notification_bp.route("/receiver", methods=["POST"])
def dispatcher():
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))

    try:
        data = serializer.loads(request.json["token"], salt="new-notif")
        sio.emit('notif-for-{}'.format(data["recipient_username"]), data)

        return jsonify(data)
    # except Exception as e:
    #     print(e)
    except:
        return None

@notification_bp.route("/get", methods=["GET"])
@session_required
def get_all(current_user):
    return jsonify(
        json.loads(
            NotificationService.get_all_by_token(
                current_user["public_id"],
                read=request.args.get("read"),
                count=request.args.get("count")
            ).text
        )["data"]
    )
