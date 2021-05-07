import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import circle_bp
from ..util.decorator import session_required
from ..form.circle_form import CreateCircleForm, EditCircleForm, DeleteCircleForm
from ..service.pet_service import PetService
from ..service.circle_service import CircleService
from ..service.breed_service import BreedService
from ..service.circleType_service import CircleTypeService

@circle_bp.route("/<circle_pid>", methods=["GET", "POST"])
@circle_bp.route("/<circle_pid>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, circle_pid):
    get_resp = CircleService.get_by_pid(circle_pid)
    if get_resp.ok:
        this_circle = json.loads(get_resp.text)

        editCircleForm = EditCircleForm(prefix="ebf")
        editCircleForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(CircleTypeService.get_all(session["booped_in"]).text)["data"]]
        editCircleForm.type_input.data = [_type["public_id"] for _type in this_circle["_type"]]

        return render_template("circle_profile.html",
            page_title = "Circle profile",
            current_user = current_user,
            this_circle = this_circle,
            editCircleForm = editCircleForm,
            deleteCircleForm = DeleteCircleForm()
        )
    else:
        abort(404)

@circle_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createCircleForm = CreateCircleForm()
    createCircleForm.type_input.choices = [(_type, "") for _type in request.form.getlist("type_input")]
    if createCircleForm.validate_on_submit():
        create_circle = CircleService.create(request.form, request.files)

        if create_circle.ok:
            resp = json.loads(create_circle.text)
            flash(resp["message"], "success")

            return redirect(url_for("user.circles", username=resp["payload"]))
        
        flash(json.loads(create_circle.text)["message"], "danger")

    if createCircleForm.errors:
        for key in createCircleForm.errors:
            for message in createCircleForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("user.circles", username=current_user["username"]))

@circle_bp.route("/<circle_pid>/edit", methods=["POST"])
@session_required
def edit(current_user, circle_pid):
    editCircleForm = EditCircleForm(prefix="ebf")
    editCircleForm.type_input.choices = [(_type, "") for _type in request.form.getlist("ebf-type_input")]

    if editCircleForm.validate_on_submit():
        edit_circle = CircleService.edit(circle_pid, session["booped_in"], request.form, request.files)

        if edit_circle.ok:
            resp = json.loads(edit_circle.text)
            flash(resp["message"], "success")

            return redirect(url_for("circle.posts", circle_pid=circle_pid))
        
        flash(json.loads(edit_circle.text)["message"], "danger")
    
    if editCircleForm.errors:
        for key in editCircleForm.errors:
            for message in editCircleForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

@circle_bp.route("/<circle_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, circle_pid):
    deleteCircleForm = DeleteCircleForm()
    owner_username = json.loads(CircleService.get_by_pid(circle_pid).text)["admin_username"]
    if deleteCircleForm.validate_on_submit():
        delete_circle = CircleService.delete(circle_pid, request.form)

        if delete_circle.ok:
            flash(json.loads(delete_circle.text)["message"], "success")

            return redirect(url_for("user.circles", username=owner_username))
        
        flash(json.loads(delete_circle.text)["message"], "danger")

    if deleteCircleForm.errors:
        for key in deleteCircleForm.errors:
            for message in deleteCircleForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))