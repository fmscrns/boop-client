import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import profile_bp
from ..service.user_service import UserService
from ..util.decorator import session_required


@profile_bp.route("/<username>", methods=["GET", "POST"])
@session_required
def pets(current_user, username):
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        return render_template("profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = json.loads(get_resp.text)
        )
    else:
        abort(404)