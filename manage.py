import os
import unittest

from app import *
from flask_script import Server, Manager

from app.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(gateway_bp, url_prefix="/gateway")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp, url_prefix="/profile")

app.app_context().push()

manager = Manager(app)

manager.add_command("run", Server(host="0.0.0.0", port=8080))

if __name__ == '__main__':
    manager.run()