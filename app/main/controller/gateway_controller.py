import json
from flask import Flask, render_template, request, session, flash, redirect, url_for
from ... import gateway_bp
from ..form.user_form import CreateUserForm
from ..form.auth_form import GetAuthTokenForm
from ..service.user_service import UserService, AdminService
from ..service.auth_service import AuthService, AdminAuthService
from ..util.decorator import no_session_required


@gateway_bp.route("/signup", methods=["GET", "POST"])
@no_session_required
def signup():
    createUserForm = CreateUserForm()

    if request.method == "POST":
        if createUserForm.validate_on_submit():
            api_resp = UserService.create(request.form)

            if api_resp.ok:
                session["booped_in"] = json.loads(api_resp.text)["Authorization"]

                flash(json.loads(api_resp.text)["message"], "success")
                return redirect(url_for("home.feed"))

            flash(json.loads(api_resp.text)["message"], "danger")
            return redirect(url_for("gateway.signup"))

        flash("Please try again.", "danger")
    
    return render_template("signup.html",
        page_title = "Sign up",
        createUserForm = createUserForm
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
    createUserForm = CreateUserForm()

    if request.method == "POST":
        if createUserForm.validate_on_submit():
            api_resp = AdminService.create(request.form)

            if api_resp.ok:
                session["admin_booped_in"] = json.loads(api_resp.text)["Authorization"]

                flash(json.loads(api_resp.text)["message"], "success")
                return redirect(url_for("admin.control"))

            flash(json.loads(api_resp.text)["message"], "danger")
            return redirect(url_for("gateway.admin_signup"))

        flash("Please try again.", "danger")
    
    return render_template("signup.html",
        page_title = "Admin sign up",
        createUserForm = createUserForm
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
    
    return render_template("signin.html",
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