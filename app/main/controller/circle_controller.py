import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from werkzeug.datastructures import Accept
from ... import circle_bp
from ..util.decorator import session_required
from ..form.circle_form import AcceptCircleForm, CreateCircleAdminForm, CreateCircleForm, DeleteCircleAdminForm, EditCircleForm, DeleteCircleForm, JoinCircleForm, LeaveCircleForm
from ..service.pet_service import PetService
from ..service.circle_service import CircleService
from ..service.breed_service import BreedService
from ..service.circleType_service import CircleTypeService
from ..service.post_service import PostService
from ..form.post_form import CreatePostForm

@circle_bp.route("/<circle_pid>", methods=["GET", "POST"])
@circle_bp.route("/<circle_pid>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, circle_pid):
    get_resp = CircleService.get_by_pid(circle_pid)
    if get_resp.ok:
        this_circle = json.loads(get_resp.text)
        createPostForm = CreatePostForm()
        createPostForm.subject_input.choices = [(subject["public_id"], subject["name"]) for subject in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"] + "?tag_suggestions=1").text)["data"]]
        editCircleForm = EditCircleForm(prefix="ebf")
        editCircleForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(CircleTypeService.get_all(session["booped_in"]).text)["data"]]
        editCircleForm.type_input.data = [_type["public_id"] for _type in this_circle["_type"]]
        return render_template("circle_profile.html",
            page_title = "Circle profile",
            current_user = current_user,
            this_circle = this_circle,
            editCircleForm = editCircleForm,
            deleteCircleForm = DeleteCircleForm(),
            createCircleAdminForm = CreateCircleAdminForm(prefix="ccaf"),
            deleteCircleAdminForm = DeleteCircleAdminForm(prefix="dcaf"),
            createPostForm = createPostForm,
            joinCircleForm = JoinCircleForm(),
            leaveCircleForm = LeaveCircleForm(),
            post_list = json.loads(PostService.get_all_by_circle(session["booped_in"], this_circle["public_id"]).text)["data"]
        )
    else:
        abort(404)

@circle_bp.route("/<circle_pid>/members", methods=["GET", "POST"])
@circle_bp.route("/<circle_pid>/members/confirmed", methods=["GET", "POST"])
@session_required
def confirmed_members(current_user, circle_pid):
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
            deleteCircleForm = DeleteCircleForm(),
            createCircleAdminForm = CreateCircleAdminForm(prefix="ccaf"),
            deleteCircleAdminForm = DeleteCircleAdminForm(prefix="dcaf"),
            inviteMemberForm = 1,
            joinCircleForm = JoinCircleForm(),
            leaveCircleForm = LeaveCircleForm(),
            member_list = json.loads(CircleService.get_all_confirmed_circle_members(session["booped_in"], this_circle["public_id"]).text)["data"]
        )
    else:
        abort(404)

@circle_bp.route("/<circle_pid>/members/pending", methods=["GET", "POST"])
@session_required
def pending_members(current_user, circle_pid):
    get_resp = CircleService.get_by_pid(circle_pid)
    if get_resp.ok:
        this_circle = json.loads(get_resp.text)

        if this_circle["visitor_auth"] == 3:
            editCircleForm = EditCircleForm(prefix="ebf")
            editCircleForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(CircleTypeService.get_all(session["booped_in"]).text)["data"]]
            editCircleForm.type_input.data = [_type["public_id"] for _type in this_circle["_type"]]
            return render_template("circle_profile.html",
                page_title = "Circle profile",
                current_user = current_user,
                this_circle = this_circle,
                editCircleForm = editCircleForm,
                deleteCircleForm = DeleteCircleForm(),
                createCircleAdminForm = CreateCircleAdminForm(prefix="ccaf"),
                deleteCircleAdminForm = DeleteCircleAdminForm(prefix="dcaf"),
                inviteMemberForm = 1,
                joinCircleForm = JoinCircleForm(),
                leaveCircleForm = LeaveCircleForm(),
                acceptCircleForm = AcceptCircleForm(),
                member_list = json.loads(CircleService.get_all_pending_circle_members(session["booped_in"], this_circle["public_id"]).text)["data"]
            )
        else:
            abort(403)
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
                flash(message, "danger")

    return redirect(url_for("user.circles", username=current_user["username"]))

@circle_bp.route("/<circle_pid>/admin/create", methods=["POST"])
@session_required
def create_admin(current_user, circle_pid):
    createCircleAdminForm = CreateCircleAdminForm(prefix="ccaf")
    if createCircleAdminForm.validate_on_submit():
        create_circle_admin = CircleService.create_admin(circle_pid, session["booped_in"], request.form)

        if create_circle_admin.ok:
            flash(json.loads(create_circle_admin.text)["message"], "success")

            return redirect(url_for("circle.posts", circle_pid=circle_pid))
        
        flash(json.loads(create_circle_admin.text)["message"], "danger")
    
    if createCircleAdminForm.errors:
        for key in createCircleAdminForm.errors:
            for message in createCircleAdminForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

@circle_bp.route("/<circle_pid>/admin/delete", methods=["POST"])
@session_required
def delete_admin(current_user, circle_pid):
    deleteCircleAdminForm = DeleteCircleAdminForm(prefix="dcaf")
    if deleteCircleAdminForm.validate_on_submit():
        delete_circle_admin = CircleService.delete_admin(circle_pid, session["booped_in"], request.form)

        if delete_circle_admin.ok:
            flash(json.loads(delete_circle_admin.text)["message"], "success")

            return redirect(url_for("circle.posts", circle_pid=circle_pid))
        
        flash(json.loads(delete_circle_admin.text)["message"], "danger")
    
    if deleteCircleAdminForm.errors:
        for key in deleteCircleAdminForm.errors:
            for message in deleteCircleAdminForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

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
                flash(message, "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

@circle_bp.route("/<circle_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, circle_pid):
    deleteCircleForm = DeleteCircleForm()
    if deleteCircleForm.validate_on_submit():
        delete_circle = CircleService.delete(circle_pid, request.form)

        if delete_circle.ok:
            flash(json.loads(delete_circle.text)["message"], "success")

            return redirect(url_for("user.circles", username=current_user["username"]))
        
        flash(json.loads(delete_circle.text)["message"], "danger")

    if deleteCircleForm.errors:
        for key in deleteCircleForm.errors:
            for message in deleteCircleForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

@circle_bp.route("/<circle_pid>/join", methods=["POST"])
@session_required
def join(current_user, circle_pid):
    joinCircleForm = JoinCircleForm()
    if joinCircleForm.validate_on_submit():
        join_circle = CircleService.join(circle_pid)

        if join_circle.ok:
            resp = json.loads(join_circle.text)
            flash(resp["message"], "success")

            return redirect(url_for("circle.posts", circle_pid=circle_pid))
        
        flash(json.loads(join_circle.text)["message"], "danger")

    if joinCircleForm.errors:
        for key in joinCircleForm.errors:
            for message in joinCircleForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

@circle_bp.route("/<circle_pid>/leave", methods=["POST"])
@session_required
def leave(current_user, circle_pid):
    leaveCircleForm = LeaveCircleForm()
    if leaveCircleForm.validate_on_submit():
        leave_circle = CircleService.leave(circle_pid, request.form)

        if leave_circle.ok:
            resp = json.loads(leave_circle.text)
            flash(resp["message"], "success")

            return redirect(url_for("circle.posts", circle_pid=circle_pid))
        
        flash(json.loads(leave_circle.text)["message"], "danger")

    if leaveCircleForm.errors:
        for key in leaveCircleForm.errors:
            for message in leaveCircleForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("circle.posts", circle_pid=circle_pid))

@circle_bp.route("/<circle_pid>/accept", methods=["POST"])
@session_required
def accept(current_user, circle_pid):
    acceptCircleForm = AcceptCircleForm()
    if acceptCircleForm.validate_on_submit():
        accept_circle = CircleService.accept(circle_pid, request.form)

        if accept_circle.ok:
            resp = json.loads(accept_circle.text)
            flash(resp["message"], "success")

            return redirect(url_for("circle.pending_members", circle_pid=circle_pid))
        
        flash(json.loads(accept_circle.text)["message"], "danger")

    if acceptCircleForm.errors:
        for key in acceptCircleForm.errors:
            for message in acceptCircleForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("circle.pending_members", circle_pid=circle_pid))