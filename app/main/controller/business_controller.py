import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import business_bp
from ..util.decorator import session_required
from ..form.business_form import CreateBusinessForm, EditBusinessForm, DeleteBusinessForm, FollowBusinessForm, UnfollowBusinessForm, CreateBusinessExecutiveForm, DeleteBusinessExecutiveForm
from ..form.appointment_form import CreateAppointmentForm
from ..service.pet_service import PetService
from ..service.business_service import BusinessService
from ..service.businessType_service import BusinessTypeService
from ..service.post_service import PostService
from ..form.post_form import CreatePostForm

@business_bp.route("/<business_pid>", methods=["GET", "POST"])
@business_bp.route("/<business_pid>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, business_pid):
    get_resp = BusinessService.get_by_pid(business_pid)
    if get_resp.ok:
        this_business = json.loads(get_resp.text)
        editBusinessForm = EditBusinessForm(prefix="ebf")
        editBusinessForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(BusinessTypeService.get_all(session["booped_in"]).text)["data"]]
        editBusinessForm.type_input.data = [_type["public_id"] for _type in this_business["_type"]]
        createAppointmentForm = CreateAppointmentForm()
        createAppointmentForm.pet_input.choices = [(pet["public_id"], pet["name"]) for pet in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"]).text)["data"]]
        createAppointmentForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in this_business["_type"]]
        createPostForm = CreatePostForm()
        createPostForm.subject_input.choices = [(subject["public_id"], subject["name"]) for subject in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"] + "?tag_suggestions=1").text)["data"]]
        return render_template("business_profile.html",
            page_title = "Business profile",
            current_user = current_user,
            this_business = this_business,
            editBusinessForm = editBusinessForm,
            deleteBusinessForm = DeleteBusinessForm(),
            createBusinessExecutiveForm = CreateBusinessExecutiveForm(prefix="cbef"),
            deleteBusinessExecutiveForm = DeleteBusinessExecutiveForm(prefix="dbef"),
            createAppointmentForm = createAppointmentForm,
            createPostForm = createPostForm,
            followBusinessForm = FollowBusinessForm(),
            unfollowBusinessForm = UnfollowBusinessForm(),
            post_list = json.loads(PostService.get_all_by_business(session["booped_in"], this_business["public_id"]).text)["data"]
        )
    else:
        abort(404)

@business_bp.route("/<business_pid>/followers", methods=["GET"])
@session_required
def followers(current_user, business_pid):
    get_resp = BusinessService.get_by_pid(business_pid)
    if get_resp.ok:
        this_business = json.loads(get_resp.text)
        editBusinessForm = EditBusinessForm(prefix="ebf")
        editBusinessForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(BusinessTypeService.get_all(session["booped_in"]).text)["data"]]
        editBusinessForm.type_input.data = [_type["public_id"] for _type in this_business["_type"]]
        createAppointmentForm = CreateAppointmentForm()
        createAppointmentForm.pet_input.choices = [(pet["public_id"], pet["name"]) for pet in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"]).text)["data"]]
        createAppointmentForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in this_business["_type"]]
        return render_template("business_profile.html",
            page_title = "Business profile",
            current_user = current_user,
            this_business = this_business,
            editBusinessForm = editBusinessForm,
            deleteBusinessForm = DeleteBusinessForm(),
            createBusinessExecutiveForm = CreateBusinessExecutiveForm(prefix="cbef"),
            deleteBusinessExecutiveForm = DeleteBusinessExecutiveForm(prefix="dbef"),
            createAppointmentForm = createAppointmentForm,
            inviteFollowerForm = 1,
            followBusinessForm = FollowBusinessForm(),
            unfollowBusinessForm = UnfollowBusinessForm(),
            follower_list = json.loads(BusinessService.get_all_followers(session["booped_in"], this_business["public_id"]).text)["data"]
        )
    else:
        abort(404)

@business_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createBusinessForm = CreateBusinessForm()
    createBusinessForm.type_input.choices = [(_type, "") for _type in request.form.getlist("type_input")]
    if createBusinessForm.validate_on_submit():
        create_business = BusinessService.create(request.form, request.files)

        if create_business.ok:
            resp = json.loads(create_business.text)
            flash(resp["message"], "success")

            return redirect(url_for("user.businesses", username=current_user["username"]))
        
        flash(json.loads(create_business.text)["message"], "danger")

    if createBusinessForm.errors:
        for key in createBusinessForm.errors:
            for message in createBusinessForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("user.businesses", username=current_user["username"]))

@business_bp.route("/<business_pid>/edit", methods=["POST"])
@session_required
def edit(current_user, business_pid):
    editBusinessForm = EditBusinessForm(prefix="ebf")
    editBusinessForm.type_input.choices = [(_type, "") for _type in request.form.getlist("ebf-type_input")]

    if editBusinessForm.validate_on_submit():
        edit_business = BusinessService.edit(business_pid, session["booped_in"], request.form, request.files)

        if edit_business.ok:
            resp = json.loads(edit_business.text)
            flash(resp["message"], "success")

            return redirect(url_for("business.posts", business_pid=business_pid))
        
        flash(json.loads(edit_business.text)["message"], "danger")
    
    if editBusinessForm.errors:
        for key in editBusinessForm.errors:
            for message in editBusinessForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("business.posts", business_pid=business_pid))

@business_bp.route("/<business_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, business_pid):
    deleteBusinessForm = DeleteBusinessForm()
    if deleteBusinessForm.validate_on_submit():
        delete_business = BusinessService.delete(business_pid, request.form)

        if delete_business.ok:
            flash(json.loads(delete_business.text)["message"], "success")

            return redirect(url_for("user.businesses", username=current_user["username"]))
        
        flash(json.loads(delete_business.text)["message"], "danger")

    if deleteBusinessForm.errors:
        for key in deleteBusinessForm.errors:
            for message in deleteBusinessForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("business.posts", business_pid=business_pid))

@business_bp.route("/<business_pid>/follow", methods=["POST"])
@session_required
def follow(current_user, business_pid):
    followBusinessForm = FollowBusinessForm()
    if followBusinessForm.validate_on_submit():
        follow_business = BusinessService.follow(business_pid)

        if follow_business.ok:
            resp = json.loads(follow_business.text)
            flash(resp["message"], "success")

            return redirect(url_for("business.posts", business_pid=business_pid))
        
        flash(json.loads(follow_business.text)["message"], "danger")

    if followBusinessForm.errors:
        for key in followBusinessForm.errors:
            for message in followBusinessForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("business.posts", business_pid=business_pid))

@business_bp.route("/<business_pid>/unfollow", methods=["POST"])
@session_required
def unfollow(current_user, business_pid):
    unfollowBusinessForm = UnfollowBusinessForm()
    if unfollowBusinessForm.validate_on_submit():
        unfollow_business = BusinessService.unfollow(business_pid, request.form)

        if unfollow_business.ok:
            resp = json.loads(unfollow_business.text)
            flash(resp["message"], "success")

            return redirect(url_for("business.posts", business_pid=business_pid))
        
        flash(json.loads(unfollow_business.text)["message"], "danger")

    if unfollowBusinessForm.errors:
        for key in unfollowBusinessForm.errors:
            for message in unfollowBusinessForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("business.posts", business_pid=business_pid))

@business_bp.route("/<business_pid>/executive/create", methods=["POST"])
@session_required
def create_executive(current_user, business_pid):
    createBusinessExecutiveForm = CreateBusinessExecutiveForm(prefix="cbef")
    if createBusinessExecutiveForm.validate_on_submit():
        create_business_executive = BusinessService.create_executive(business_pid, session["booped_in"], request.form)

        if create_business_executive.ok:
            flash(json.loads(create_business_executive.text)["message"], "success")

            return redirect(url_for("business.posts", business_pid=business_pid))
        
        flash(json.loads(create_business_executive.text)["message"], "danger")
    
    if createBusinessExecutiveForm.errors:
        for key in createBusinessExecutiveForm.errors:
            for message in createBusinessExecutiveForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("business.posts", business_pid=business_pid))

@business_bp.route("/<business_pid>/executive/delete", methods=["POST"])
@session_required
def delete_executive(current_user, business_pid):
    deleteBusinessExecutiveForm = DeleteBusinessExecutiveForm(prefix="dbef")
    if deleteBusinessExecutiveForm.validate_on_submit():
        delete_business_executive = BusinessService.delete_executive(business_pid, session["booped_in"], request.form)

        if delete_business_executive.ok:
            flash(json.loads(delete_business_executive.text)["message"], "success")

            return redirect(url_for("business.posts", business_pid=business_pid))
        
        flash(json.loads(delete_business_executive.text)["message"], "danger")
    
    if deleteBusinessExecutiveForm.errors:
        for key in deleteBusinessExecutiveForm.errors:
            for message in deleteBusinessExecutiveForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("business.posts", business_pid=business_pid))