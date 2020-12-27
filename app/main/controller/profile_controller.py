import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import profile_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.user_form import EditUserForm

@profile_bp.route("/<username>", methods=["GET", "POST"])
@session_required
def pets(current_user, username):
    editUserForm = EditUserForm()
    editUserForm.name_input.data = current_user["name"]
    editUserForm.username_input.data = current_user["username"]
    editUserForm.email_input.data = current_user["email"]
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        return render_template("profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = json.loads(get_resp.text),
            editUserForm = editUserForm
        )
    else:
        abort(404)

@profile_bp.route("user/edit/<pid>", methods=["POST"])
@session_required
def edit_user(current_user, pid):
    editUserForm = EditUserForm()

    if editUserForm.validate_on_submit():
        edit_user = UserService.edit(pid, session["booped_in"], request.form, request.files)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("profile.pets", username=resp["payload"]))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editUserForm.errors:
        for key in editUserForm.errors:
            for message in editUserForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("profile.pets", username=current_user["username"]))