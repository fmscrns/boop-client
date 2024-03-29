from flask import Blueprint


gateway_bp = Blueprint("gateway", __name__)
admin_bp = Blueprint("admin", __name__)
home_bp = Blueprint("home", __name__)
user_bp = Blueprint("user", __name__)
pet_bp = Blueprint("pet", __name__)
business_bp = Blueprint("business", __name__)
appointment_bp = Blueprint("appointment", __name__)
post_bp = Blueprint("post", __name__)
circle_bp = Blueprint("circle", __name__)
comment_bp = Blueprint("comment", __name__)
notification_bp = Blueprint("notification", __name__)
preference_bp = Blueprint("preference", __name__)
settings_bp = Blueprint("settings", __name__)
breed_bp = Blueprint("breed", __name__)
search_bp = Blueprint("search", __name__)


from .main.controller import gateway_controller, admin_controller, home_controller, user_controller, pet_controller, business_controller, appointment_controller, post_controller, circle_controller, comment_controller, notification_controller, preference_controller, settings_controller, breed_controller, search_controller