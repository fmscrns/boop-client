from flask import Blueprint

gateway_bp = Blueprint("gateway", __name__)
admin_bp = Blueprint("admin", __name__)
home_bp = Blueprint("home", __name__)
profile_bp = Blueprint("profile", __name__)

from .main.controller import gateway_controller, admin_controller, home_controller, profile_controller