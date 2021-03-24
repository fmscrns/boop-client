import os
import unittest

from app import *
from flask_script import Server, Manager

from app.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(gateway_bp, url_prefix="/gateway")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(home_bp)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(pet_bp, url_prefix="/pet")
app.register_blueprint(business_bp, url_prefix="/business")
app.register_blueprint(appointment_bp, url_prefix="/appointment")
app.register_blueprint(post_bp, url_prefix="/post")

app.app_context().push()

manager = Manager(app)

manager.add_command("run", Server(host="0.0.0.0", port=8080))

if __name__ == '__main__':
    manager.run()