import os
import unittest

from app import *
from flask_script import Server, Manager

from app.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'prod')
app.register_blueprint(gateway_bp, url_prefix="/gateway")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(home_bp)
app.register_blueprint(user_profile_bp, url_prefix="/user/profile")
app.register_blueprint(pet_profile_bp, url_prefix="/pet/profile")
app.register_blueprint(business_profile_bp, url_prefix="/business/profile")

app.app_context().push()

manager = Manager(app)

manager.add_command("run", Server(host="0.0.0.0", port=8080))

if __name__ == '__main__':
    manager.run()