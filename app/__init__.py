from flask import Blueprint

gateway_bp = Blueprint("gateway", __name__)
home_bp = Blueprint("home", __name__)

from .main.controller import gateway_controller, home_controller