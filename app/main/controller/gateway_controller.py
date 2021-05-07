import json, os
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, session, flash, redirect, url_for
from ... import gateway_bp
from ..form.user_form import CreateUserOneForm, CreateUserTwoForm
from ..form.auth_form import GetAuthTokenForm
from ..service.user_service import UserService, AdminService
from ..service.auth_service import AuthService, AdminAuthService
from ..util.decorator import no_session_required

@gateway_bp.route("/signup/1", methods=["GET", "POST"])
@no_session_required
def signup_one():
    createUserOneForm = CreateUserOneForm()

    if request.method == "POST":
        if createUserOneForm.validate_on_submit():
            # send data wrapped in token to signup part two
            serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
            token = serializer.dumps({
                "name_input": createUserOneForm.name_input.data, 
                "email_input": createUserOneForm.email_input.data}, salt="signup_two")
            
            return redirect(url_for("gateway.signup_two", token=token))

        flash("Please try again.", "danger")
    
    return render_template("signup_one.html",
        page_title = "Sign up",
        createUserOneForm = createUserOneForm
    )

@gateway_bp.route("/signup/2/token=<token>", methods=["GET", "POST"])
@no_session_required
def signup_two(token):
    createUserTwoForm = CreateUserTwoForm()

    # receive data from signup part one and if this page is called and no data, return error
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    try:
        partial_user_data = serializer.loads(token, salt="signup_two")
        createUserTwoForm.name_input.data = partial_user_data.pop("name_input")
        createUserTwoForm.email_input.data = partial_user_data.pop("email_input")

    except Exception:
        flash("Invalid token.", "danger")
        return redirect(url_for("gateway.signup_one"))
    
    return render_template("signup_two.html",
        page_title = "Sign up",
        createUserTwoForm = createUserTwoForm
    )

@gateway_bp.route("/signin", methods=["GET", "POST"])
@no_session_required
def signin():
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
    
    return render_template("signin.html",
        page_title = "Sign in",
        getAuthTokenForm = getAuthTokenForm
    )

@gateway_bp.route("/signout", methods=["POST"])
def signout():
    api_resp = AuthService.blacklist_auth_token()

    if api_resp.ok:
        session.pop("booped_in")
        flash(json.loads(api_resp.text)["message"], "success")
        return redirect(url_for("welcome"))

    flash(json.loads(api_resp.text)["message"], "danger")
    return redirect(url_for("home.feed"))

@gateway_bp.route("/admin/signup", methods=["GET", "POST"])
@no_session_required
def admin_signup():
    createUserTwoForm = CreateUserTwoForm()

    if request.method == "POST":
        if createUserTwoForm.validate_on_submit():
            api_resp = AdminService.create(request.form)

            if api_resp.ok:
                session["admin_booped_in"] = json.loads(api_resp.text)["Authorization"]

                flash(json.loads(api_resp.text)["message"], "success")
                return redirect(url_for("admin.control"))

            flash(json.loads(api_resp.text)["message"], "danger")
            return redirect(url_for("gateway.admin_signup"))

        flash("Please try again.", "danger")
    
    return render_template("admin_signup.html",
        page_title = "Admin sign up",
        createUserTwoForm = createUserTwoForm
    )

@gateway_bp.route("/admin/signin", methods=["GET", "POST"])
@no_session_required
def admin_signin():
    getAuthTokenForm = GetAuthTokenForm()

    if request.method == "POST":
        if getAuthTokenForm.validate_on_submit():
            api_resp = AdminAuthService.get_auth_token(request.form)

            if api_resp.ok:
                session["admin_booped_in"] = json.loads(api_resp.text)["Authorization"]

                flash(json.loads(api_resp.text)["message"], "success")
                return redirect(url_for("admin.control"))

            flash(json.loads(api_resp.text)["message"], "danger")
            return redirect(url_for("gateway.admin_signin"))
            
        flash("Please try again.", "danger")
    
    return render_template("admin_signin.html",
        page_title = "Admin sign in",
        getAuthTokenForm = getAuthTokenForm
    )

@gateway_bp.route("/admin/signout", methods=["POST"])
def admin_signout():
    api_resp = AdminAuthService.blacklist_auth_token()

    if api_resp.ok:
        session.pop("admin_booped_in")
        flash(json.loads(api_resp.text)["message"], "success")
        return redirect(url_for("welcome"))

    flash(json.loads(api_resp.text)["message"], "danger")
    return redirect(url_for("home.feed"))