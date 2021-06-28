import cloudinary as myCloudinary, cloudinary.uploader, json
from flask import Flask, render_template, request, session, flash, redirect, url_for
from .config import config_by_name
from .util.decorator import no_session_required
from .form.auth_form import GetAuthTokenForm
from .service.auth_service import AuthService
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)

def create_app(config_name):
    app.config.from_object(config_by_name[config_name])

    myCloudinary.config(
        cloud_name=app.config["NAME_CLOUDINARY"],
        api_key=app.config["KEY_API_CLOUDINARY"],
        api_secret=app.config["SECRET_API_CLOUDINARY"]
    )

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    @app.route("/", methods=["GET", "POST"])
    @app.route("/welcome", methods=["GET", "POST"])
    @no_session_required
    def welcome():
        getAuthTokenForm = GetAuthTokenForm()

        if request.method == "POST":
            if getAuthTokenForm.validate_on_submit():
                api_resp = AuthService.get_auth_token(request.form)

                if api_resp.ok:
                    session["booped_in"] = json.loads(api_resp.text)["Authorization"]

                    flash(json.loads(api_resp.text)["message"], "success")
                    return redirect(url_for("home.feed"))

                flash(json.loads(api_resp.text)["message"], "danger")
                return redirect(url_for("gateway.signin"))
                
            flash("Please try again.", "danger")
            
        return render_template("welcome.html",
            page_title="Welcome",
            getAuthTokenForm = getAuthTokenForm
        )
    return app, sio
