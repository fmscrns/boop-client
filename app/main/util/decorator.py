import json
from flask import session, redirect, url_for, flash
from functools import wraps
from ..service.user_service import UserService, AdminService

def session_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "booped_in" in session:
            get_resp = UserService.get_by_token()
            if get_resp.ok:
                return f(*args, **kwargs, current_user=json.loads(get_resp.text))
            else:
                flash(json.loads(get_resp.text)["message"], "danger")
                return redirect(url_for("gateway.signin"))
        elif "admin_booped_in" in session:
            get_resp = AdminService.get_by_token()
            if get_resp.ok:
                flash("Basic user only.", "danger")
                return redirect(url_for("admin.control"))
            else:
                flash(json.loads(get_resp.text)["message"], "danger")
                return redirect(url_for("gateway.admin_signin"))
        else:
            flash("You must sign in first.", "warning")
            return redirect(url_for("gateway.signin"))
    
    return wrap

def admin_session_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "admin_booped_in" in session:
            get_resp = AdminService.get_by_token()
            if get_resp.ok:
                return f(*args, **kwargs, current_user=json.loads(get_resp.text))
            else:
                flash(json.loads(get_resp.text)["message"], "danger")
                return redirect(url_for("gateway.admin_signin"))
        elif "booped_in" in session:
            get_resp = UserService.get_by_token()
            if get_resp.ok:
                flash("Admin user only.", "warning")
                return redirect(url_for("home.feed"))
            else:
                flash(json.loads(get_resp.text)["message"], "danger")
                return redirect(url_for("gateway.signin"))
        else:
            flash("You must sign in first.", "warning")
            return redirect(url_for("gateway.admin_signin"))
    
    return wrap

def no_session_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "booped_in" in session:
            get_resp = UserService.get_by_token()
            if get_resp.ok:
                flash("You must sign out first.", "warning")
                return redirect(url_for("home.feed"))
            else:
                flash(json.loads(get_resp.text)["message"], "danger")
                return f(*args, **kwargs)
        elif "admin_booped_in" in session:
            get_resp = AdminService.get_by_token()
            if get_resp.ok:
                flash("You must sign out first.", "warning")
                return redirect(url_for("admin.control"))
            else:
                flash(json.loads(get_resp.text)["message"], "danger")
                return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return wrap