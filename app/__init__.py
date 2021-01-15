from flask import Blueprint

gateway_bp = Blueprint("gateway", __name__)
admin_bp = Blueprint("admin", __name__)
home_bp = Blueprint("home", __name__)
user_profile_bp = Blueprint("user_profile", __name__)
pet_profile_bp = Blueprint("pet_profile", __name__)
business_profile_bp = Blueprint("business_profile", __name__)

from .main.controller import gateway_controller, admin_controller, home_controller, user_profile_controller, pet_profile_controller, business_profile_controller