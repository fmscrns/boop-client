import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import business_profile_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.business_form import CreateBusinessForm, EditBusinessForm, DeleteBusinessForm
from ..service.business_service import BusinessService
from ..service.breed_service import BreedService
from ..service.business_service import BusinessService
from dateutil import parser

@business_profile_bp.route("/<business_pid>", methods=["GET", "POST"])
@business_profile_bp.route("/<business_pid>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, business_pid):
    get_resp = BusinessService.get_by_pid(business_pid)
    if get_resp.ok:
        this_business = json.loads(get_resp.text)
        print(this_business)
        editBusinessForm = EditBusinessForm(prefix="ebf")
        
        if this_business["_type"] <= 2:
            editBusinessForm.type_input.data = [this_business["_type"]]
        elif this_business["_type"] == 3:
            editBusinessForm.type_input.data = [0, 1]
        elif this_business["_type"] == 4:
            editBusinessForm.type_input.data = [0, 2]
        elif this_business["_type"] == 5:
            editBusinessForm.type_input.data = [1, 2]
        elif this_business["_type"] == 6:
            editBusinessForm.type_input.data = [0, 1, 2]

        return render_template("business_profile.html",
            page_title = "Business profile",
            current_user = current_user,
            this_business = this_business,
            editBusinessForm = editBusinessForm,
            deleteBusinessForm = DeleteBusinessForm()
        )
    else:
        abort(404)

@business_profile_bp.route("business/edit/<pid>", methods=["POST"])
@session_required
def edit_business(current_user, pid):
    editBusinessForm = EditBusinessForm(prefix="ebf")

    if editBusinessForm.validate_on_submit():
        edit_business = BusinessService.edit(pid, session["booped_in"], request.form, request.files)

        if edit_business.ok:
            resp = json.loads(edit_business.text)
            flash(resp["message"], "success")

            return redirect(url_for("business_profile.posts", business_pid=pid))
        
        flash(json.loads(edit_business.text), "danger")
    
    if editBusinessForm.errors:
        for key in editBusinessForm.errors:
            for message in editBusinessForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("business_profile.posts", business_pid=pid))

@business_profile_bp.route("business/delete/<pid>", methods=["POST"])
@session_required
def delete_business(current_user, pid):
    deleteBusinessForm = DeleteBusinessForm()
    owner_username = json.loads(BusinessService.get_by_pid(pid).text)["exec_username"]
    if deleteBusinessForm.validate_on_submit():
        delete_business = BusinessService.delete(pid, request.form)

        if delete_business.ok:
            flash(json.loads(delete_business.text)["message"], "success")

            return redirect(url_for("user_profile.businesses", username=owner_username))
        
        flash(json.loads(delete_business.text), "danger")

    if deleteBusinessForm.errors:
        for key in deleteBusinessForm.errors:
            for message in deleteBusinessForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("business_profile.posts", business_pid=pid))